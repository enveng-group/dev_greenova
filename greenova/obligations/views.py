import logging

import django_tables2 as tables
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_control, require_http_methods
from django.views.decorators.vary import vary_on_headers
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
    UpdateView,
)
from mechanisms.models import EnvironmentalMechanism
from projects.models import Project
from responsibility.models import ResponsibilityAssignment

from .filters import ObligationFilter
from .forms import EvidenceUploadForm, ObligationForm, ResponsibilityAssignmentFormSet
from .models import Obligation, ObligationEvidence
from .serializers import (
    ObligationCollectionProtoSerializer,
    ObligationProtoSerializer,
)
from .tables import get_obligation_table
from .utils import (
    is_obligation_overdue,
)

# Create a logger for this module
logger = logging.getLogger(__name__)


@method_decorator(cache_control(max_age=300), name="dispatch")
@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
class ObligationSummaryView(LoginRequiredMixin, TemplateView):
    template_name = "obligations/components/_obligations_summary.html"

    def get_template_names(self):
        """Return appropriate template based on request type."""
        return [self.template_name]

    def get_context_data(self, **kwargs):
        """Get context data for the template."""
        context = super().get_context_data(**kwargs)
        mechanism_id = self.request.GET.get("mechanism_id")
        try:
            project = get_object_or_404(EnvironmentalMechanism, id=mechanism_id)
            queryset = Obligation.objects.filter(
                primary_environmental_mechanism=mechanism_id,
            )
            filterset = ObligationFilter(self.request.GET, queryset=queryset)
            page_number = self.request.GET.get("page", 1)
            paginator = Paginator(filterset.qs, 15)
            page_obj = paginator.get_page(page_number)
            context.update(
                {
                    "obligations": page_obj,
                    "page_obj": page_obj,
                    "project": project,
                    "mechanism_id": mechanism_id,
                    "filter": filterset,
                    "total_count": paginator.count,
                },
            )
            phases = (
                Obligation.objects.filter(primary_environmental_mechanism=mechanism_id)
                .exclude(project_phase__isnull=True)
                .exclude(project_phase="")
                .values_list("project_phase", flat=True)
                .distinct()
            )
            phases_cleaned = {phase.strip() for phase in phases}
            context["phases"] = list(phases_cleaned)

            def user_can_edit_obligation(obligation, user):
                return ResponsibilityAssignment.objects.filter(
                    obligation=obligation,
                    user=user,
                    role__in=["Owner", "Editor"],
                ).exists()

            context["user_can_edit"] = user_can_edit_obligation
        except Exception as e:
            logger.exception(f"Error in ObligationSummaryView: {e!s}")
            context["error"] = f"Error loading obligations: {e!s}"
        return context


class TotalOverdueObligationsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        project_id = request.GET.get("project_id")

        if not project_id:
            return JsonResponse({"error": "Project ID is required"}, status=400)

        obligations = Obligation.objects.filter(project_id=project_id)

        overdue_count = sum(
            1 for obligation in obligations if is_obligation_overdue(obligation)
        )

        return JsonResponse(overdue_count, safe=False)


class ObligationCreateView(LoginRequiredMixin, CreateView):
    """View for creating a new obligation."""

    model = Obligation
    form_class = ObligationForm
    template_name = "obligations/form/new_obligation.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        project_id = self.request.GET.get("project_id")
        if project_id:
            try:
                project = Project.objects.get(id=project_id)
                kwargs["project"] = project
            except Project.DoesNotExist:
                pass
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.request.GET.get("project_id")
        if project_id:
            context["project_id"] = project_id
        if self.request.POST:
            context["formset"] = ResponsibilityAssignmentFormSet(self.request.POST)
        else:
            context["formset"] = ResponsibilityAssignmentFormSet()
        return context

    def form_valid(self, form):
        try:
            super().form_valid(form)
            formset = ResponsibilityAssignmentFormSet(
                self.request.POST,
                instance=self.object,
            )
            if formset.is_valid():
                formset.save()
            else:
                return self.form_invalid(form)

            # Add success message
            messages.success(
                self.request,
                f"Obligation {self.object.obligation_number} created successfully.",
            )

            # Redirect to appropriate page
            if "project_id" in self.request.GET:
                return redirect(
                    f"{reverse('dashboard:home')}?project_id={self.request.GET['project_id']}",
                )
            return redirect("dashboard:home")

        except Exception as e:
            logger.exception(f"Error in ObligationCreateView: {e}")
            messages.error(self.request, f"Failed to create obligation: {e!s}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class ObligationDetailView(LoginRequiredMixin, DetailView):
    """View for viewing a single obligation."""

    model = Obligation
    template_name = "obligations/form/view_obligation.html"
    context_object_name = "obligation"
    pk_url_kwarg = "obligation_number"

    def user_has_role(self, roles: list[str]) -> bool:
        """Check if the current user has any of the specified roles for the obligation."""
        return self.object.responsibility_assignments.filter(
            user=self.request.user,
            role__in=roles,
        ).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add project_id to context for back navigation
        context["project_id"] = self.object.project_id
        context["user_can_edit"] = self.user_has_role(["Editor", "Owner", "Manager"])
        return context


class ObligationUpdateView(LoginRequiredMixin, UpdateView):
    """Update an existing obligation."""

    model = Obligation
    form_class = ObligationForm
    template_name = "obligations/form/update_obligation.html"
    slug_field = "obligation_number"
    slug_url_kwarg = "obligation_number"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Only allow users with edit rights (Owner/Editor) to update
        if not ResponsibilityAssignment.objects.filter(
            obligation=self.object,
            user=request.user,
            role__in=["Owner", "Editor"],  # Adjust as needed
        ).exists():
            messages.error(
                request,
                "You do not have permission to edit this obligation.",
            )
            return redirect("dashboard:home")
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        return [self.template_name]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["project"] = self.object.project
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add project_id to context for back navigation
        context["project_id"] = self.object.project_id
        if self.request.POST:
            context["formset"] = ResponsibilityAssignmentFormSet(
                self.request.POST,
                instance=self.object,
            )
        else:
            context["formset"] = ResponsibilityAssignmentFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        try:
            old_mechanism = None
            if self.object.primary_environmental_mechanism:
                old_mechanism = self.object.primary_environmental_mechanism

            super().form_valid(form)
            formset = ResponsibilityAssignmentFormSet(
                self.request.POST,
                instance=self.object,
            )
            if formset.is_valid():
                formset.save()
            else:
                return self.form_invalid(form)

            # Update mechanism counts
            if (
                old_mechanism
                and old_mechanism != self.object.primary_environmental_mechanism
            ):
                if old_mechanism:
                    old_mechanism.update_obligation_counts()
                if self.object.primary_environmental_mechanism:
                    self.object.primary_environmental_mechanism.update_obligation_counts()
            elif self.object.primary_environmental_mechanism:
                self.object.primary_environmental_mechanism.update_obligation_counts()

            # Add success message
            messages.success(
                self.request,
                f"Obligation {self.object.obligation_number} updated successfully.",
            )

            # Redirect back to the appropriate page
            if "project_id" in self.request.GET:
                return redirect(
                    f"{reverse('dashboard:home')}?project_id={self.request.GET['project_id']}",
                )
            return redirect("dashboard:home")

        except Exception as e:
            logger.exception(f"Error in ObligationUpdateView: {e}")
            messages.error(self.request, f"Failed to update obligation: {e!s}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class ObligationDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting an obligation."""

    model = Obligation
    pk_url_kwarg = "obligation_number"

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            # Only allow users with delete rights (Owner/Editor) to delete
            if not ResponsibilityAssignment.objects.filter(
                obligation=self.object,
                user=request.user,
                role__in=["Owner", "Editor"],  # Adjust as needed
            ).exists():
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "You do not have permission to delete this obligation.",
                    },
                    status=403,
                )

            project_id = self.object.project_id
            mechanism = self.object.primary_environmental_mechanism

            # Delete the obligation
            self.object.delete()
            logger.info(
                f"Obligation {kwargs.get('obligation_number')} deleted successfully",
            )

            # Update mechanism counts
            if mechanism:
                mechanism.update_obligation_counts()

            # Return JSON response for AJAX calls
            return JsonResponse(
                {
                    "status": "success",
                    "message": f"Obligation {
                        kwargs.get('obligation_number')
                    } deleted successfully",
                    "redirect_url": f"{reverse('dashboard:home')}?project_id={
                        project_id
                    }",
                },
            )

        except Exception as e:
            logger.exception(f"Error deleting obligation: {e!s}")
            return JsonResponse(
                {
                    "status": "error",
                    "message": f"Error deleting obligation: {e!s}",
                },
                status=400,
            )


@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
class ToggleCustomAspectView(View):
    def get(self, request):
        aspect = request.GET.get("environmental_aspect")
        if aspect == "Other":
            return render(
                request,
                "obligations/partials/custom_aspect_field.html",
                {
                    "show_field": True,
                },
            )
        return render(
            request,
            "obligations/partials/custom_aspect_field.html",
            {
                "show_field": False,
            },
        )


def upload_evidence(request, obligation_id):
    obligation = get_object_or_404(Obligation, pk=obligation_id)

    # Check if obligation already has 5 files
    if ObligationEvidence.objects.filter(obligation=obligation).count() >= 5:
        messages.error(
            request,
            "This obligation already has the maximum of 5 evidence files",
        )
        return redirect("obligation_detail", obligation_id=obligation_id)

    if request.method == "POST":
        form = EvidenceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            evidence = form.save(commit=False)
            evidence.obligation = obligation
            evidence.save()
            messages.success(request, "Evidence file uploaded successfully")
            return redirect("obligation_detail", obligation_id=obligation_id)
    else:
        form = EvidenceUploadForm()
        return render(
            request,
            "upload_evidence.html",
            {
                "obligation": obligation,
                "form": form,
            },
        )
    return None


@login_required
def export_obligation(request, obligation_number: str) -> HttpResponse:
    """Export a single obligation as Protocol Buffer binary data."""
    if request.user.is_staff:
        obligation = get_object_or_404(Obligation, obligation_number=obligation_number)
    else:
        obligation = get_object_or_404(
            Obligation,
            obligation_number=obligation_number,
            responsibility_assignments__user=request.user,
        )
    serializer = ObligationProtoSerializer(instance=obligation)
    data = serializer.data()
    if not data:
        messages.error(request, "Failed to export obligation.")
        return redirect("dashboard:home")
    response = HttpResponse(data, content_type="application/octet-stream")
    response["Content-Disposition"] = (
        f'attachment; filename="obligation_{obligation_number}.pb"'
    )
    return response


@login_required
def export_all_obligations(request) -> HttpResponse:
    """Export all obligations as a Protocol Buffer collection."""
    if request.user.is_staff:
        obligations = list(Obligation.objects.all())
    else:
        obligations = list(
            Obligation.objects.filter(responsibility_assignments__user=request.user),
        )
    serializer = ObligationCollectionProtoSerializer(instances=obligations)
    data = serializer.data()
    if not data:
        messages.error(request, "Failed to export obligations.")
        return redirect("dashboard:home")
    response = HttpResponse(data, content_type="application/octet-stream")
    response["Content-Disposition"] = 'attachment; filename="obligations.pb"'
    return response


@login_required
@require_http_methods(["GET", "POST"])
def import_obligation(request) -> HttpResponse:
    """Import an obligation from Protocol Buffer binary data."""
    if request.method == "POST":
        if "file" not in request.FILES:
            messages.error(request, "No file was provided.")
            return redirect("obligations:import_obligation")
        uploaded_file = request.FILES["file"]
        try:
            data = uploaded_file.read()
            serializer = ObligationProtoSerializer(data=data)
            if not serializer.is_valid():
                messages.error(
                    request,
                    "Could not deserialize the file. Invalid format.",
                )
                return redirect("obligations:import_obligation")
            obligation = serializer.validated_data
            # Set the creator to the current user if applicable
            # obligation.created_by = request.user  # Uncomment if model supports
            obligation.obligation_number = None  # Ensure a new record is created
            obligation.save()
            messages.success(request, "Obligation imported successfully.")
            return redirect("dashboard:home")
        except (ValueError, OSError, AttributeError, TypeError) as e:
            logger.exception("Error importing obligation: %s", str(e))
            messages.error(request, "An error occurred while importing the obligation.")
            return redirect("obligations:import_obligation")
    # GET request - show import form
    return render(
        request,
        "obligations/import_obligation.html",
        {
            "page_title": "Import Obligation",
        },
    )


class ObligationListView(LoginRequiredMixin, TemplateView):
    template_name = "obligations/obligation_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Obligation.objects.all()
        # Filtering logic can be added here as needed
        ObligationTable = get_obligation_table()
        table = ObligationTable(queryset)
        tables.RequestConfig(self.request, paginate={"per_page": 15}).configure(table)
        context["table"] = table
        return context
