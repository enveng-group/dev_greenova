"""Copyright (C) 2025 Adrian Gallo.

This file is part of Greenova.

Greenova is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Greenova is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Greenova. If not, see <https://www.gnu.org/licenses/>.

Author: Adrian Gallo <agallo@enveng-group.com.au>
"""

"""Views for managing environmental obligations.

This module provides views for creating, reading, updating, deleting,
and listing environmental obligations. It also includes views for
handling related functionalities like evidence uploads.
"""

from utils import is_obligation_overdue
from projects.models import Project, ProjectMembership
from obligations.models import Obligation, ObligationEvidence
from mechanisms.models import EnvironmentalMechanism
from forms import EvidenceUploadForm, ObligationForm
from django_htmx.http import trigger_client_event
from django.views.generic.edit import DeleteView
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.decorators.vary import vary_on_headers
from django.views.decorators.cache import cache_control
from django.views import View
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.urls import reverse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.db.models import Q, QuerySet
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from company.models import CompanyMembership
from beartype import beartype
from typing import TYPE_CHECKING, Any, TypeVar, cast
from datetime import date, timedelta
import logging
import os


if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser

# Ensure the Django settings module is correctly configured.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greenova.settings")

logger = logging.getLogger(__name__)

MAX_EVIDENCE_FILES = 5

# Type variable for models
T = TypeVar("T")


@method_decorator(cache_control(max_age=300), name="dispatch")
@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
class ObligationSummaryView(LoginRequiredMixin, View):
    """View for displaying obligation summary with filtering capabilities.

    This view handles both standard requests and HTMX requests for
    dynamically loading filtered obligations.
    """

    @beartype
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        """Handle GET requests for obligation summary.

        When accessed via HTMX from procedure charts, this returns filtered obligations.
        Otherwise, it provides the full obligation summary view.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Rendered template with appropriate context.

        """
        # Check if this is a filtered request from procedure charts
        status = request.GET.get("status")
        procedure = request.GET.get("procedure")
        project_id = request.GET.get("project_id")

        if status and procedure and project_id:
            try:
                # Fix for attr-defined error
                obligations = Obligation.objects.filter(
                    project_id=project_id,
                )

                # Apply status filter (handle overdue special case)
                if status:
                    # Always treat status as a list
                    status_list = [status] if isinstance(status, str) else list(status)
                    # Map normalized status to canonical model value
                    status_map = {
                        "not_started": "not started",
                        "not started": "not started",
                        "in_progress": "in progress",
                        "in progress": "in progress",
                        "completed": "completed",
                        "overdue": "overdue",
                    }
                    canonical_statuses = [
                        status_map.get(
                            s.replace("_", " ").lower(),
                            s.replace("_", " ").lower(),
                        )
                        for s in status_list
                    ]
                    obligations = self._filter_by_status(
                        obligations, canonical_statuses,
                    )

                # Apply procedure filter (adjusted for TextField)
                if procedure:
                    obligations = obligations.filter(procedure__icontains=procedure)

                return render(
                    request,
                    "obligations/partials/obligation_list.html",
                    {"obligations": obligations},
                )
            except Exception as exc:
                logger.exception("Error filtering obligations: %s", str(exc))
                return render(
                    request,
                    "obligations/partials/obligation_list.html",
                    {
                        "error": f"Error loading obligations: {exc!s}",
                        "obligations": [],
                    },
                )

        # For regular requests, proceed with full view
        context = self.get_context_data(**kwargs)

        if self.request.htmx:  # type: ignore[attr-defined]
            return render(
                request, "obligations/components/_obligations_summary.html", context,
            )

        return render(
            request, "obligations/components/_obligations_summary.html", context,
        )

    @beartype
    def _filter_by_status(
        self, queryset: QuerySet[Obligation], status_values: list[str],
    ) -> QuerySet[Obligation]:
        """Filter obligations by status, handling 'overdue' as a special case.

        Args:
            queryset: Base queryset.
            status_values: List of status values to filter by.

        Returns:
            Filtered queryset.

        """
        # Normalize all status values to canonical model values
        status_map = {
            "not_started": "not started",
            "not started": "not started",
            "in_progress": "in progress",
            "in progress": "in progress",
            "completed": "completed",
            "overdue": "overdue",
        }
        canonical_statuses = [
            status_map.get(s.replace("_", " ").lower(), s.replace("_", " ").lower())
            for s in status_values
        ]
        # Handle the special case of 'overdue' which isn't a database field
        if "overdue" in canonical_statuses:
            # Remove overdue to handle separately
            standard_statuses = [s for s in canonical_statuses if s != "overdue"]

            # Get obligations that match standard statuses
            if standard_statuses:
                filtered_by_status = queryset.filter(status__in=standard_statuses)
            else:
                filtered_by_status = queryset.none()

            # Find overdue obligations: action_due_date < today and status != completed
            today = timezone.now().date()
            overdue_queryset = queryset.filter(action_due_date__lt=today).exclude(
                status="completed",
            )

            # Combine with standard status filter
            if overdue_queryset.exists():
                return filtered_by_status.union(overdue_queryset)
            return filtered_by_status

        # Standard status filtering
        if canonical_statuses:
            return queryset.filter(status__in=canonical_statuses)
        return queryset

    @beartype
    def apply_filters(
        self, queryset: QuerySet[Obligation], filters: dict[str, Any],
    ) -> QuerySet[Obligation]:
        """Apply all filters to the queryset.

        Args:
            queryset: Base queryset.
            filters: Dictionary of filter values.

        Returns:
            Filtered queryset.

        """
        if not queryset:
            return queryset
        if filters.get("status"):
            queryset = self._filter_by_status(queryset, filters["status"])
        if filters.get("phase"):
            queryset = queryset.filter(project_phase__in=filters["phase"])
        if filters.get("search"):
            search_term = filters["search"]
            queryset = queryset.filter(
                Q(obligation_number__icontains=search_term)
                | Q(obligation__icontains=search_term),
            )
        if filters.get("date_filter"):
            date_filter = filters["date_filter"]
            today = date.today()
            if date_filter == "past_due":
                queryset = queryset.filter(
                    action_due_date__lt=today, status__ne="completed",
                )
            elif date_filter == "14days":
                future_date = today + timedelta(days=14)
                queryset = queryset.filter(
                    action_due_date__gte=today, action_due_date__lte=future_date,
                )
            elif date_filter == "30days":
                future_date = today + timedelta(days=30)
                queryset = queryset.filter(
                    action_due_date__gte=today, action_due_date__lte=future_date,
                )
        return queryset

    @beartype
    def get_filters(self) -> dict[str, Any]:
        """Extract and normalize filter parameters from request.

        Returns:
            Dictionary of filter parameters.

        """
        filters: dict[str, Any] = {}

        # Get query parameters
        status = self.request.GET.getlist("status") or self.request.GET.getlist(
            "status[]",
        )
        phase = self.request.GET.getlist("phase") or self.request.GET.getlist("phase[]")
        search = self.request.GET.get("search", "")
        date_filter = self.request.GET.get("date_filter", "")

        # Add sort parameters with defaults
        sort = self.request.GET.get("sort", "obligation_number")
        order = self.request.GET.get("order", "asc")

        # Build filters dict
        if status:
            filters["status"] = [s.strip().lower() for s in status]
        if phase:
            filters["phase"] = [p.strip() for p in phase if p.strip()]
        if search:
            filters["search"] = search
        if date_filter:
            filters["date_filter"] = date_filter

        # Add sort parameters
        filters["sort"] = sort
        filters["order"] = order

        return filters

    @beartype
    def get_context_data(self, **kwargs: dict) -> dict[str, object]:
        """Get context data for the template.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Context dictionary for rendering template.

        """
        context: dict[str, Any] = {}
        mechanism_id = self.request.GET.get("mechanism_id")

        try:
            if not mechanism_id:
                return self._get_overdue_data_for_user(context)

            # Process mechanism-specific data
            mechanism = EnvironmentalMechanism.objects.get(id=mechanism_id)
            # Fix for attr-defined error
            obligations = Obligation.objects.filter(
                primary_environmental_mechanism=mechanism,
            )

            context.update(
                {
                    "obligations": obligations,
                    "total_count": obligations.count(),
                    "mechanism": mechanism,
                    "filters": {"mechanism_id": mechanism_id},
                },
            )

            # Add edit permission - fix for union-attr error
            user = cast("AbstractUser", self.request.user)
            context["user_can_edit"] = user.has_perm("obligations.change_obligation")
            return context

        except Exception as e:
            context["error"] = str(e)
            return context

    def _get_overdue_data_for_user(self, context: dict[str, Any]) -> dict[str, Any]:
        """Get overdue obligations data for the current user.

        Args:
            context: The existing context dictionary.

        Returns:
            Updated context dictionary.

        """
        user = self.request.user

        # Get company memberships and roles
        company_memberships = CompanyMembership.objects.filter(user=user)
        user_roles = list(company_memberships.values_list("role", flat=True).distinct())

        # Get project memberships and IDs
        project_memberships = ProjectMembership.objects.filter(user=user)
        project_ids = list(project_memberships.values_list("project_id", flat=True))

        # If user has neither company roles nor project memberships, show error
        if not (user_roles or project_ids):
            context["error"] = "You don't have any company roles or project memberships"
            return context

        # If user has project memberships, show overdue obligations for those projects
        if project_ids:
            queryset = Obligation.objects.filter(
                project_id__in=project_ids,
            )
            # Optionally filter by responsibility if user_roles exist
            if user_roles:
                queryset = queryset.filter(responsibility__in=user_roles)
            overdue_obligations = [
                obligation.obligation_number
                for obligation in queryset
                if is_obligation_overdue(obligation)
            ]
            if not overdue_obligations:
                context["error"] = "No overdue obligations found for your projects"
                return context
            queryset = queryset.filter(obligation_number__in=overdue_obligations)
        # If only company roles, show overdue obligations for those roles
        elif user_roles:
            queryset = Obligation.objects.filter(
                responsibility__in=user_roles,
            )
            overdue_obligations = [
                obligation.obligation_number
                for obligation in queryset
                if is_obligation_overdue(obligation)
            ]
            if not overdue_obligations:
                context["error"] = "No overdue obligations found for your role"
                return context
            queryset = queryset.filter(obligation_number__in=overdue_obligations)
        else:
            context["error"] = "No overdue obligations found."
            return context

        context.update(
            {
                "obligations": queryset,
                "total_count": len(queryset),
                "filters": {"status": ["overdue"]},
                "show_overdue_only": True,
            },
        )
        # Fix for user permission check
        user = cast("AbstractUser", self.request.user)
        context["user_can_edit"] = user.has_perm("obligations.change_obligation")
        return context


class TotalOverdueObligationsView(LoginRequiredMixin, View):
    """View to get the count of overdue obligations for a project."""

    @beartype
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> JsonResponse:
        """Handle GET request to count overdue obligations.

        Args:
            request: HTTP request with project_id parameter.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            JsonResponse with count or error.

        """
        project_id = request.GET.get("project_id")

        if not project_id:
            return JsonResponse({"error": "Project ID is required"}, status=400)

        # Fix for attr-defined error
        obligations = Obligation.objects.filter(
            project_id=project_id,
        )
        overdue_count = sum(
            1 for obligation in obligations if is_obligation_overdue(obligation)
        )

        return JsonResponse(overdue_count, safe=False)


class ObligationCreateView(LoginRequiredMixin, CreateView):
    """View for creating a new obligation."""

    model = Obligation
    form_class = ObligationForm
    template_name = "obligations/form/new_obligation.html"

    @beartype
    def get_form_kwargs(self) -> dict[str, Any]:
        """Return the keyword arguments for instantiating the form.

        Adds the project to the form kwargs if a project_id is present
        in the request's GET parameters.

        Returns:
            A dictionary of keyword arguments.

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
    def get_context_data(self, **kwargs: dict) -> dict[str, object]:
        """Insert the project_id into the context dict.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            A dictionary containing the context data.

        """
        context = super().get_context_data(**kwargs)
        project_id = self.request.GET.get("project_id")
        if project_id:
            context["project_id"] = project_id
        return context

    @beartype
    def form_valid(self, form: ObligationForm) -> HttpResponse:
        """Process valid form submission with error handling.

        Args:
            form: The validated form.

        Returns:
            Redirect to appropriate page on success.

        """
        try:
            # Save the form
            obligation = form.save()

            # Add success message
            messages.success(
                self.request,
                f"Obligation {obligation.obligation_number} created successfully.",
            )

            # Redirect to appropriate page
            if "project_id" in self.request.GET:
                project_id = self.request.GET["project_id"]
                return redirect(f"{reverse('dashboard:home')}?project_id={project_id}")
            return redirect("dashboard:home")

        except ValidationError as exc:
            logger.exception("Validation error in ObligationCreateView: %s", str(exc))
            messages.error(self.request, f"Validation failed: {exc}")
            # Rely on type inference from get_context_data's return type
            context = self.get_context_data(form=form)
            return self.render_to_response(context)

        except Exception as exc:
            logger.exception("Error creating obligation: %s", str(exc))
            messages.error(self.request, f"Failed to create obligation: {exc!s}")
            # Rely on type inference from get_context_data's return type
            context = self.get_context_data(form=form)
            return self.render_to_response(context)

    @beartype
    def form_invalid(self, form: ObligationForm) -> HttpResponse:
        """Handle invalid form submissions.

        Adds an error message and re-renders the form with errors.

        Args:
            form: The invalid form.

        Returns:
            An HttpResponse rendering the form with errors.

        """
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class ObligationDetailView(LoginRequiredMixin, DetailView):
    """View for viewing a single obligation."""

    model = Obligation
    template_name = "obligations/form/view_obligation.html"
    context_object_name = "obligation"
    pk_url_kwarg = "obligation_number"

    @beartype
    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        """Initialize the view with object attribute to avoid mypy errors.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """
        super().__init__(*args, **kwargs)
        self.object = None  # Keep mypy happy

    @beartype
    def get_context_data(self, **kwargs: dict) -> dict[str, object]:
        """Insert the project_id into the context dict.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            A dictionary containing the context data.

        """
        context = super().get_context_data(**kwargs)
        # Add project_id to context for back navigation
        if self.object:
            context["project_id"] = self.object.project_id
        return context

    @beartype
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        """Handle GET requests for obligation details.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response with rendered template or JSON data.

        """
        self.object = self.get_object()

        # Check if this is an AJAX request for modal content
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            # Get available mechanisms for the form
            available_mechanisms = EnvironmentalMechanism.objects.all()

            # Render the editable modal content template
            modal_content = render_to_string(
                "obligations/components/_obligation_editable_modal_content.html",
                {
                    "obligation": self.object,
                    "available_mechanisms": available_mechanisms,
                },
                request=request,
            )

            # Format long values for obligation dates to avoid line length issues
            obl_number = self.object.obligation_number
            proj_name = self.object.project.name
            status_disp = self.object.get_status_display()

            return JsonResponse(
                {
                    "obligation_number": obl_number,
                    "project_name": proj_name,
                    "status_display": status_disp,
                    "content": modal_content,
                },
            )

        # Regular request - return the full page
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    @beartype
    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        """Handle POST requests for updating obligations via AJAX.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            JsonResponse with success/error data or standard response.

        """
        self.object = self.get_object()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            form = ObligationForm(request.POST, instance=self.object)

            if form.is_valid():
                obligation = form.save()

                # Extract and format values to avoid long lines
                action_date = None
                if obligation.action_due_date:
                    action_date = obligation.action_due_date.isoformat()

                close_date = None
                if obligation.close_out_date:
                    close_date = obligation.close_out_date.isoformat()

                return JsonResponse(
                    {
                        "success": True,
                        "message": "Obligation updated successfully",
                        "obligation": {
                            "obligation_number": obligation.obligation_number,
                            "environmental_aspect": obligation.environmental_aspect,
                            "obligation": obligation.obligation,
                            "procedure": obligation.procedure,
                            "responsibility": obligation.responsibility,
                            "action_due_date": action_date,
                            "close_out_date": close_date,
                            "general_comments": obligation.general_comments,
                            "supporting_information": obligation.supporting_information,
                            "compliance_comments": obligation.compliance_comments,
                            "status_display": obligation.get_status_display(),
                        },
                    },
                )
            return JsonResponse({"success": False, "errors": form.errors})

        # Fall back to regular form handling for non-AJAX requests
        return self.render_to_response(self.get_context_data())


class ObligationUpdateView(LoginRequiredMixin, UpdateView):
    """Update an existing obligation."""

    model = Obligation
    form_class = ObligationForm
    template_name = "obligations/form/update_obligation.html"
    slug_field = "obligation_number"
    slug_url_kwarg = "obligation_number"

    @beartype
    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        """Initialize the view with object attribute to avoid mypy errors.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """
        super().__init__(*args, **kwargs)
        self.object = None  # Keep mypy happy

    @beartype
    def get_template_names(self) -> list[str]:
        """Return a list of template names to be used for the request.

        Uses a partial template if the request is an HTMX request.

        Returns:
            A list of template names.

        """
        if hasattr(self.request, "htmx") and self.request.htmx:
            return ["obligations/form/partial_update_obligation.html"]
        return [self.template_name]

    @beartype
    def get_form_kwargs(self) -> dict[str, Any]:
        """Return the keyword arguments for instantiating the form.

        Adds the project associated with the obligation to the form kwargs.

        Returns:
            A dictionary of keyword arguments.

        """
        kwargs = super().get_form_kwargs()
        if self.object:
            kwargs["project"] = self.object.project
        return kwargs

    @beartype
    def get_context_data(self, **kwargs: dict) -> dict[str, object]:
        """Insert the project_id into the context dict.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            A dictionary containing the context data.

        """
        context = super().get_context_data(**kwargs)
        if self.object:
            context["project_id"] = self.object.project_id
        return context

    @beartype
    def _update_mechanism_counts(
        self,
        old_mechanism: EnvironmentalMechanism | None,
        updated_obligation: Obligation,
    ) -> None:
        """Update obligation counts for mechanisms.

        Args:
            old_mechanism: Previous mechanism (if any).
            updated_obligation: The updated obligation.

        """
        # Get the new mechanism from the updated obligation
        new_mech = getattr(updated_obligation, "primary_environmental_mechanism", None)
        updated_new_mech_flag = False

        # If there was an old mechanism and it's different from the new one
        if old_mechanism and old_mechanism != new_mech:
            # Update old mechanism counts first
            if hasattr(old_mechanism, "update_obligation_counts"):
                old_mechanism.update_obligation_counts()
            # Then update new mechanism if it exists
            if new_mech and hasattr(new_mech, "update_obligation_counts"):
                new_mech.update_obligation_counts()
                updated_new_mech_flag = True

        # If new_mech hasn't been updated yet, and it's valid, update it.
        # This covers cases where old_mechanism was None or same as new_mech.
        if (
            not updated_new_mech_flag
            and new_mech
            and hasattr(new_mech, "update_obligation_counts")
        ):
            new_mech.update_obligation_counts()

    @beartype
    def form_valid(self, form: ObligationForm) -> HttpResponse:
        """Process the form submission with HTMX support.

        Args:
            form: The validated form.

        Returns:
            Appropriate response based on request type.

        """
        try:
            old_mechanism = None
            if self.object and hasattr(self.object, "primary_environmental_mechanism"):
                old_mechanism = self.object.primary_environmental_mechanism

            # Save the updated obligation
            obligation = form.save()
            self._update_mechanism_counts(old_mechanism, obligation)

            messages.success(
                self.request,
                f"Obligation {obligation.obligation_number} updated successfully.",
            )

            # If this is an HTMX request, return appropriate headers
            if hasattr(self.request, "htmx") and self.request.htmx:
                response = HttpResponse("Obligation updated successfully")
                # Explicitly trigger a refresh for dependent components
                trigger_client_event(
                    response, "path-deps-refresh", {"path": "/obligations/"},
                )
                return response

            # Standard response for regular requests
            if "project_id" in self.request.GET:
                base_url = reverse("dashboard:home")
                proj_id = self.request.GET["project_id"]
                return redirect(f"{base_url}?project_id={proj_id}")
            return redirect("dashboard:home")

        except ValidationError as exc:
            logger.exception("Validation error updating obligation: %s", str(exc))
            messages.error(self.request, f"Validation failed: {exc}")
            error_response: HttpResponse = self.form_invalid(form)
            return error_response

        except Exception as exc:
            logger.exception("Error updating obligation: %s", str(exc))
            messages.error(self.request, f"Failed to update obligation: {exc!s}")
            exception_response: HttpResponse = self.form_invalid(form)
            return exception_response

    @beartype
    def form_invalid(self, form: ObligationForm) -> HttpResponse:
        """Handle invalid form submissions.

        Adds an error message and re-renders the form with errors.

        Args:
            form: The invalid form.

        Returns:
            An HttpResponse rendering the form with errors.

        """
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class ObligationDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting an obligation."""

    model = Obligation
    pk_url_kwarg = "obligation_number"

    @beartype
    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> JsonResponse:
        """Handle POST request for obligation deletion.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments containing 'obligation_number'.

        Returns:
            JsonResponse with success or error status.

        """
        try:
            obj = self.get_object()
            project_id = obj.project_id
            mechanism = getattr(obj, "primary_environmental_mechanism", None)
            obl_number = kwargs.get("obligation_number")

            # Delete the obligation
            obj.delete()
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
                },
            )

        except Exception as exc:
            logger.exception("Error deleting obligation: %s", str(exc))
            return JsonResponse(
                {
                    "status": "error",
                    "message": f"Error deleting obligation: {exc!s}",
                },
                status=400,
            )


@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
class ToggleCustomAspectView(View):
    """View for toggling custom aspect field visibility."""

    @beartype
    def get(self, request: HttpRequest) -> HttpResponse:
        """Handle GET request for toggling custom aspect field.

        Args:
            request: HTTP request with environmental_aspect parameter.

        Returns:
            Rendered partial template.

        """
        aspect = request.GET.get("environmental_aspect")
        show_field = aspect == "Other"
        return render(
            request,
            "obligations/partials/custom_aspect_field.html",
            {"show_field": show_field},
        )


class ObligationListView(LoginRequiredMixin, ListView):
    """List all obligations."""

    model = Obligation
    template_name = "obligations/obligations_list.html"
    context_object_name = "obligations"

    @beartype
    def get_queryset(self) -> QuerySet[Obligation]:
        """Return the queryset for listing obligations.

        Returns:
            A queryset of all Obligation objects.

        """
        return Obligation.objects.all()


@beartype
def upload_evidence(request: HttpRequest, obligation_id: int) -> HttpResponse:
    """Handle evidence file uploads for an obligation.

    Args:
        request: HTTP request.
        obligation_id: ID of the obligation to attach evidence to.

    Returns:
        Redirect to appropriate page.

    """
    obligation = get_object_or_404(Obligation, pk=obligation_id)

    # Check how many evidence files already exist
    evidence_count = ObligationEvidence.objects.filter(obligation=obligation).count()

    # Check if obligation already has MAX_EVIDENCE_FILES files
    if evidence_count >= MAX_EVIDENCE_FILES:
        messages.error(
            request,
            f"This obligation already has the maximum of {MAX_EVIDENCE_FILES} "
            f"evidence files",
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

# API classes have been moved to api_views.py
