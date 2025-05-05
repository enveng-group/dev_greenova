import logging
import os
from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q, QuerySet
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView
from django.views.generic.edit import DeleteView
from mechanisms.models import EnvironmentalMechanism
from projects.models import Project

from .forms import EvidenceUploadForm, ObligationForm
from .models import Obligation, ObligationEvidence
from .utils import is_obligation_overdue

# Ensure the Django settings module is correctly configured.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greenova.settings")


logger = logging.getLogger(__name__)

# Add type hints or mock objects for Obligation and EnvironmentalMechanism to resolve the missing `objects` and `DoesNotExist` members.
Obligation.objects = Obligation.objects if hasattr(Obligation, "objects") else None
Obligation.DoesNotExist = (
    Obligation.DoesNotExist if hasattr(Obligation, "DoesNotExist") else None
)
EnvironmentalMechanism.objects = (
    EnvironmentalMechanism.objects
    if hasattr(EnvironmentalMechanism, "objects")
    else None
)
EnvironmentalMechanism.DoesNotExist = (
    EnvironmentalMechanism.DoesNotExist
    if hasattr(EnvironmentalMechanism, "DoesNotExist")
    else None
)


@method_decorator(cache_control(max_age=300), name="dispatch")
@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
class ObligationSummaryView(LoginRequiredMixin, TemplateView):
    template_name = "obligations/components/_obligations_summary.html"

    def get_template_names(self):
        if self.request.htmx:
            return ["obligations/components/_obligations_summary.html"]
        return [self.template_name]

    def _filter_by_status(self, queryset: QuerySet, status_values: list) -> QuerySet:
        """Filter queryset by status values including overdue check."""
        if "overdue" not in status_values:
            return queryset.filter(status__in=status_values)

        filtered_ids = [
            obligation.obligation_number
            for obligation in queryset
            if is_obligation_overdue(obligation)
        ]
        status_filter = Q(status__in=status_values)
        id_filter = Q(obligation_number__in=filtered_ids)
        return queryset.filter(status_filter | id_filter)

    def apply_filters(self, queryset: QuerySet, filters: dict[str, Any]) -> QuerySet:
        if filters["status"]:
            queryset = self._filter_by_status(queryset, filters["status"])

        if filters["mechanism"]:
            queryset = queryset.filter(
                primary_environmental_mechanism__id__in=filters["mechanism"]
            )

        if filters["phase"]:
            queryset = queryset.filter(project_phase__in=filters["phase"])

        # Fixing search filter to avoid Q object binary operation issues
        if filters["search"]:
            search_query = Q()
            searchable_fields = [
                "obligation_number",
                "obligation",
                "supporting_information",
            ]
            for field in searchable_fields:
                search_query |= Q(**{f"{field}__icontains": filters["search"]})
            queryset = queryset.filter(search_query)

        return queryset

    def get_filters(self) -> dict[str, Any]:
        return {
            "status": self.request.GET.getlist("status"),
            "mechanism": self.request.GET.getlist("mechanism"),
            "phase": self.request.GET.getlist("phase"),
            "search": self.request.GET.get("search", ""),
            "sort": self.request.GET.get("sort", "action_due_date"),
            "order": self.request.GET.get("order", "asc"),
            "date_filter": self.request.GET.get("date_filter", ""),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mechanism_id = self.request.GET.get("mechanism_id")

        try:
            project = get_object_or_404(EnvironmentalMechanism, id=mechanism_id)
            filters = self.get_filters()
            base_queryset = Obligation.objects.filter(
                primary_environmental_mechanism=mechanism_id
            )
            queryset = self.apply_filters(base_queryset, filters)

            sort_field = filters["sort"]
            if filters["order"] == "desc":
                sort_field = f"-{sort_field}"
            queryset = queryset.order_by(sort_field)

            paginator = Paginator(queryset, 15)
            page_number = self.request.GET.get("page", 1)
            page_obj = paginator.get_page(page_number)

            context.update(
                {
                    "obligations": page_obj,
                    "page_obj": page_obj,
                    "project": project,
                    "mechanism_id": mechanism_id,
                    "filters": filters,
                    "total_count": paginator.count,
                }
            )

            # Get unique project phases
            phases_queryset = (
                Obligation.objects.filter(primary_environmental_mechanism=mechanism_id)
                .exclude(project_phase__isnull=True)
                .exclude(project_phase="")
                .values_list("project_phase", flat=True)
                .distinct()
            )
            context["phases"] = list({phase.strip() for phase in phases_queryset})
            context["user_can_edit"] = self.request.user.has_perm(
                "obligations.change_obligation"
            )

        except EnvironmentalMechanism.DoesNotExist as exc:
            logger.error("EnvironmentalMechanism not found: %s", str(exc))
            context["error"] = "Error loading obligations: Mechanism not found."

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
        return context

    # Proper exception handling and logging in form_valid
    def form_valid(self, form):
        try:
            obligation = form.save()
            messages.success(
                self.request, f"Obligation {obligation.obligation_number} created."
            )
            return redirect("dashboard:home")
        except ValidationError as exc:
            logger.error("Validation error in ObligationCreateView: %s", str(exc))
            messages.error(self.request, f"Validation failed: {exc}")
            return self.form_invalid(form)

        except OSError as exc:
            logger.error("IO error updating obligation: %s", str(exc))
            messages.error(self.request, "System error occurred")
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add project_id to context for back navigation
        context["project_id"] = self.object.project_id
        return context


class ObligationUpdateView(LoginRequiredMixin, UpdateView):
    """Update an existing obligation."""

    model = Obligation
    form_class = ObligationForm
    template_name = "obligations/form/update_obligation.html"
    slug_field = "obligation_number"
    slug_url_kwarg = "obligation_number"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def get_template_names(self):
        if self.request.htmx:
            return ["obligations/form/partial_update_obligation.html"]
        return [self.template_name]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["project"] = self.get_object().project
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project_id"] = self.get_object().project_id
        return context

    def _update_mechanism_counts(
        self, old_mechanism: EnvironmentalMechanism, updated_obligation: Obligation
    ):
        """Update obligation counts for mechanisms."""
        if (
            old_mechanism
            and old_mechanism != updated_obligation.primary_environmental_mechanism
        ):
            old_mechanism.update_obligation_counts()
            if updated_obligation.primary_environmental_mechanism:
                mech = updated_obligation.primary_environmental_mechanism
                mech.update_obligation_counts()
        elif updated_obligation.primary_environmental_mechanism:
            updated_obligation.primary_environmental_mechanism.update_obligation_counts()  # pylint: disable=no-member

    def form_valid(self, form):
        try:
            self.object = self.get_object()
            old_mechanism = self.object.primary_environmental_mechanism

            # Save the updated obligation
            updated_obligation = form.save()
            self._update_mechanism_counts(old_mechanism, updated_obligation)

            messages.success(
                self.request,
                f"Obligation {updated_obligation.obligation_number} updated.",
            )

            # Build redirect URL
            if "project_id" in self.request.GET:
                base_url = reverse("dashboard:home")
                proj_id = self.request.GET["project_id"]
                return redirect(f"{base_url}?project_id={proj_id}")
            return redirect("dashboard:home")

        except ValidationError as exc:
            logger.error("Validation error updating obligation: %s", str(exc))
            messages.error(self.request, f"Validation failed: {exc}")
            return self.form_invalid(form)

        except OSError as exc:
            logger.error("IO error updating obligation: %s", str(exc))
            messages.error(self.request, "System error occurred")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class ObligationDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting an obligation."""

    model = Obligation
    pk_url_kwarg = "obligation_number"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            project_id = self.object.project_id
            mechanism = self.object.primary_environmental_mechanism
            obl_number = kwargs.get("obligation_number")

            # Delete the obligation
            self.object.delete()
            logger.info("Obligation %s deleted successfully", obl_number)

            # Update mechanism counts
            if mechanism:
                mechanism.update_obligation_counts()

            base_url = reverse("dashboard:home")
            return JsonResponse(
                {
                    "status": "success",
                    "message": f"Obligation {obl_number} deleted successfully",
                    "redirect_url": f"{base_url}?project_id={project_id}",
                }
            )

        except (Obligation.DoesNotExist, ValidationError) as exc:
            logger.error("Error deleting obligation: %s", str(exc))
            msg = f"Delete failed: {exc}"
            return JsonResponse({"status": "error", "message": msg}, status=400)


@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
class ToggleCustomAspectView(View):
    """View for toggling custom aspect field visibility."""

    def get(self, request):
        aspect = request.GET.get("environmental_aspect")
        show_field = aspect == "Other"
        return render(
            request,
            "obligations/partials/custom_aspect_field.html",
            {"show_field": show_field},
        )


def upload_evidence(request, obligation_id):
    """Handle evidence file uploads for an obligation."""
    obligation = get_object_or_404(Obligation, pk=obligation_id)
    evidence_count = ObligationEvidence.objects.filter(obligation=obligation).count()

    # Check if obligation already has 5 files
    if evidence_count >= 5:
        messages.error(
            request, "This obligation already has the maximum of 5 evidence files"
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

    form = EvidenceUploadForm()
    return render(
        request,
        "upload_evidence.html",
        {
            "obligation": obligation,
            "form": form,
        },
    )
