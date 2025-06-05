"""Views for the obligations app.

This module provides views for displaying, exporting, importing, and managing
obligation data, including summary, detail, create, update, and delete views.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

import logging
from typing import Any

import django_tables2 as tables
from beartype import beartype
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_http_methods
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
from .mixins import ObligationContextMixin, ObligationPermissionRequiredMixin
from .models import Obligation, ObligationEvidence
from .serializers import (
    ObligationCollectionProtoSerializer,
    ObligationProtoSerializer,
)
from .tables import get_obligation_table
from .utils import (
    is_obligation_overdue,
)

logger = logging.getLogger(__name__)


@method_decorator(cache_control(max_age=300), name="dispatch")
@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
class ObligationSummaryView(LoginRequiredMixin, ObligationContextMixin, TemplateView):
    """View for displaying a summary of obligations."""

    template_name = "obligations/components/_obligations_summary.html"

    @beartype
    def get_template_names(self) -> list[str]:
        """Return appropriate template based on request type.

        Returns:
            List of template names.

        """
        return [self.template_name]

    @beartype
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Get context data for the template.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Context dictionary for the template.

        """
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

            def user_can_edit_obligation(obligation: Obligation, user: Any) -> bool:
                """Check if user can edit the given obligation.

                Args:
                    obligation: The obligation instance.
                    user: The user instance.

                Returns:
                    True if user can edit, False otherwise.

                """
                return ResponsibilityAssignment.objects.filter(
                    obligation=obligation,
                    user=user,
                    role__in=["Owner", "Editor"],
                ).exists()

            context["user_can_edit"] = user_can_edit_obligation
        except Exception as e:
            logger.exception("Error in ObligationSummaryView: %s", str(e))
            context["error"] = f"Error loading obligations: {e!s}"
        return context


class TotalOverdueObligationsView(
    LoginRequiredMixin,
    ObligationPermissionRequiredMixin,
    View,
):
    """View for returning the total number of overdue obligations."""

    @beartype
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        """Handle GET request to return overdue obligations count.

        Args:
            request: The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            JsonResponse with overdue obligations count.

        """
        project_id = request.GET.get("project_id")

        if not project_id:
            return JsonResponse({"error": "Project ID is required"}, status=400)

        obligations = Obligation.objects.filter(project_id=project_id)

        overdue_count = sum(
            1 for obligation in obligations if is_obligation_overdue(obligation)
        )

        return JsonResponse(overdue_count, safe=False)


class ObligationCreateView(
    LoginRequiredMixin,
    ObligationPermissionRequiredMixin,
    ObligationContextMixin,
    CreateView,
):
    """View for creating a new obligation."""

    model = Obligation
    form_class = ObligationForm
    template_name = "obligations/form/new_obligation.html"

    @beartype
    def get_form_kwargs(self) -> dict[str, Any]:
        """Get form keyword arguments.

        Returns:
            Dictionary of form kwargs.

        """
        kwargs = super().get_form_kwargs()
        project_id = self.request.GET.get("project_id")
        if project_id:
            try:
                project = Project.objects.get(id=project_id)
                kwargs["project"] = project
            except Project.DoesNotExist:
                pass
        return kwargs

    @beartype
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Get context data for the template.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Context dictionary for the template.

        """
        context = super().get_context_data(**kwargs)
        project_id = self.request.GET.get("project_id")
        if project_id:
            context["project_id"] = project_id
        if self.request.POST:
            context["formset"] = ResponsibilityAssignmentFormSet(self.request.POST)
        else:
            context["formset"] = ResponsibilityAssignmentFormSet()
        return context

    @beartype
    def form_valid(self, form: Any) -> HttpResponse:
        """Handle valid form submission.

        Args:
            form: The valid form instance.

        Returns:
            HttpResponse redirecting to the appropriate page.

        """
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

            messages.success(
                self.request,
                f"Obligation {self.object.obligation_number} created successfully.",
            )

            if "project_id" in self.request.GET:
                return redirect(
                    f"{reverse('dashboard:home')}?project_id={self.request.GET['project_id']}",
                )
            return redirect("dashboard:home")

        except Exception as e:
            logger.exception("Error in ObligationCreateView: %s", str(e))
            messages.error(self.request, f"Failed to create obligation: {e!s}")
            return self.form_invalid(form)

    @beartype
    def form_invalid(self, form: Any) -> HttpResponse:
        """Handle invalid form submission.

        Args:
            form: The invalid form instance.

        Returns:
            HttpResponse with form errors.

        """
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class ObligationDetailView(
    LoginRequiredMixin,
    ObligationPermissionRequiredMixin,
    ObligationContextMixin,
    DetailView,
):
    """View for viewing a single obligation."""

    model = Obligation
    template_name = "obligations/form/view_obligation.html"
    context_object_name = "obligation"
    pk_url_kwarg = "obligation_number"

    @beartype
    def user_has_role(self, roles: list[str]) -> bool:
        """Check if the current user has any of the specified roles for the obligation.

        Args:
            roles: List of role names.

        Returns:
            True if user has any of the roles, False otherwise.

        """
        return self.object.responsibility_assignments.filter(
            user=self.request.user,
            role__in=roles,
        ).exists()

    @beartype
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Get context data for the template.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Context dictionary for the template.

        """
        context = super().get_context_data(**kwargs)
        context["project_id"] = self.object.project_id
        context["user_can_edit"] = self.user_has_role(["Editor", "Owner", "Manager"])
        return context


class ObligationUpdateView(
    LoginRequiredMixin,
    ObligationPermissionRequiredMixin,
    ObligationContextMixin,
    UpdateView,
):
    """Update an existing obligation."""

    model = Obligation
    form_class = ObligationForm
    template_name = "obligations/form/update_obligation.html"
    slug_field = "obligation_number"
    slug_url_kwarg = "obligation_number"

    @beartype
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Dispatch the request, enforcing edit permissions.

        Args:
            request: The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse for the next step in the dispatch chain.

        """
        self.object = self.get_object()
        if not ResponsibilityAssignment.objects.filter(
            obligation=self.object,
            user=request.user,
            role__in=["Owner", "Editor"],
        ).exists():
            messages.error(
                request,
                "You do not have permission to edit this obligation.",
            )
            return redirect("dashboard:home")
        return super().dispatch(request, *args, **kwargs)

    @beartype
    def get_template_names(self) -> list[str]:
        """Return template names for the update view.

        Returns:
            List of template names.

        """
        return [self.template_name]

    @beartype
    def get_form_kwargs(self) -> dict[str, Any]:
        """Get form keyword arguments.

        Returns:
            Dictionary of form kwargs.

        """
        kwargs = super().get_form_kwargs()
        kwargs["project"] = self.object.project
        return kwargs

    @beartype
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Get context data for the template.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Context dictionary for the template.

        """
        context = super().get_context_data(**kwargs)
        context["project_id"] = self.object.project_id
        if self.request.POST:
            context["formset"] = ResponsibilityAssignmentFormSet(
                self.request.POST,
                instance=self.object,
            )
        else:
            context["formset"] = ResponsibilityAssignmentFormSet(instance=self.object)
        return context

    @beartype
    def form_valid(self, form: Any) -> HttpResponse:
        """Handle valid form submission for update.

        Args:
            form: The valid form instance.

        Returns:
            HttpResponse redirecting to the appropriate page.

        """
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

            messages.success(
                self.request,
                f"Obligation {self.object.obligation_number} updated successfully.",
            )

            if "project_id" in self.request.GET:
                return redirect(
                    f"{reverse('dashboard:home')}?project_id={self.request.GET['project_id']}",
                )
            return redirect("dashboard:home")

        except Exception as e:
            logger.exception("Error in ObligationUpdateView: %s", str(e))
            messages.error(self.request, f"Failed to update obligation: {e!s}")
            return self.form_invalid(form)

    @beartype
    def form_invalid(self, form: Any) -> HttpResponse:
        """Handle invalid form submission for update.

        Args:
            form: The invalid form instance.

        Returns:
            HttpResponse with form errors.

        """
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class ObligationDeleteView(
    LoginRequiredMixin,
    ObligationPermissionRequiredMixin,
    DeleteView,
):
    """View for deleting an obligation."""

    model = Obligation
    pk_url_kwarg = "obligation_number"

    @beartype
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        """Handle POST request to delete an obligation.

        Args:
            request: The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            JsonResponse indicating success or failure.

        """
        try:
            self.object = self.get_object()
            if not ResponsibilityAssignment.objects.filter(
                obligation=self.object,
                user=request.user,
                role__in=["Owner", "Editor"],
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

            self.object.delete()
            logger.info(
                "Obligation %s deleted successfully",
                kwargs.get("obligation_number"),
            )

            if mechanism:
                mechanism.update_obligation_counts()

            return JsonResponse(
                {
                    "status": "success",
                    "message": (
                        f"Obligation {kwargs.get('obligation_number')} deleted successfully"
                    ),
                    "redirect_url": (
                        f"{reverse('dashboard:home')}?project_id={project_id}"
                    ),
                },
            )

        except Exception as e:
            logger.exception("Error deleting obligation: %s", str(e))
            return JsonResponse(
                {
                    "status": "error",
                    "message": f"Error deleting obligation: {e!s}",
                },
                status=400,
            )


@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
class ToggleCustomAspectView(View):
    """View for toggling the custom aspect field."""

    @beartype
    def get(self, request: HttpRequest) -> HttpResponse:
        """Handle GET request to toggle custom aspect field.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse with rendered partial template.

        """
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


@beartype
def upload_evidence(request: HttpRequest, obligation_id: int) -> HttpResponse | None:
    """Upload evidence file for an obligation.

    Args:
        request: The HTTP request object.
        obligation_id: The ID of the obligation.

    Returns:
        HttpResponse for the upload page or redirect, or None.

    """
    obligation = get_object_or_404(Obligation, pk=obligation_id)

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


@beartype
@login_required
def export_obligation(request: HttpRequest, obligation_number: str) -> HttpResponse:
    """Export a single obligation as Protocol Buffer binary data.

    Args:
        request: The HTTP request object.
        obligation_number: The obligation number.

    Returns:
        HttpResponse with the exported data.

    """
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


@beartype
@login_required
def export_all_obligations(request: HttpRequest) -> HttpResponse:
    """Export all obligations as a Protocol Buffer collection.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse with the exported data.

    """
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


@beartype
@login_required
@require_http_methods(["GET", "POST"])
def import_obligation(request: HttpRequest) -> HttpResponse:
    """Import an obligation from Protocol Buffer binary data.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse for the import page or redirect.

    """
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
            # obligation.created_by = request.user  # Uncomment if model supports
            obligation.obligation_number = None  # Ensure a new record is created
            obligation.save()
            messages.success(request, "Obligation imported successfully.")
            return redirect("dashboard:home")
        except (ValueError, OSError, AttributeError, TypeError) as e:
            logger.exception("Error importing obligation: %s", str(e))
            messages.error(request, "An error occurred while importing the obligation.")
            return redirect("obligations:import_obligation")
    return render(
        request,
        "obligations/import_obligation.html",
        {
            "page_title": "Import Obligation",
        },
    )


class ObligationListView(LoginRequiredMixin, ObligationContextMixin, TemplateView):
    """View for listing all obligations."""

    template_name = "obligations/obligation_list.html"

    @beartype
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Get context data for the obligation list view.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Context dictionary for the template.

        """
        context = super().get_context_data(**kwargs)
        queryset = Obligation.objects.all()
        ObligationTable = get_obligation_table()
        table = ObligationTable(queryset)
        tables.RequestConfig(self.request, paginate={"per_page": 15}).configure(table)
        context["table"] = table
        return context
