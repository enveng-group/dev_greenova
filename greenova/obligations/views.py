import logging
import os
from datetime import date, timedelta
from typing import Any

from company.models import CompanyMembership
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q, QuerySet
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.edit import DeleteView
from django_htmx.http import trigger_client_event
from mechanisms.models import EnvironmentalMechanism
from projects.models import Project, ProjectMembership
from responsibility.models import Responsibility, ResponsibilityAssignment
from django.http import HttpRequest, HttpResponse

from .forms import EvidenceUploadForm, ObligationForm
from .models import Obligation, ObligationEvidence
from .utils import is_obligation_overdue

# Ensure the Django settings module is correctly configured.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greenova.settings")


logger = logging.getLogger(__name__)

# Add type hints or mock objects for Obligation and EnvironmentalMechanism to
# resolve the missing `objects` and `DoesNotExist` members.
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
class ObligationSummaryView(LoginRequiredMixin, View):
    """View for displaying obligation summary with filtering capabilities.

    This view handles both standard requests and HTMX requests for
    dynamically loading filtered obligations.
    """

    def get(self, request, *args, **kwargs):
        """Handle GET requests for obligation summary.

        When accessed via HTMX from procedure charts, this returns filtered obligations.
        Otherwise, it provides the full obligation summary view.

        Args:
            request: The HTTP request

        Returns:
            Rendered template with appropriate context
        """
        # Check if this is a filtered request from procedure charts
        status = request.GET.get("status")
        procedure = request.GET.get("procedure")
        project_id = request.GET.get("project_id")

        if status and procedure and project_id:
            try:
                # Filter obligations based on parameters
                obligations = Obligation.objects.filter(project_id=project_id)

                # Apply status filter (handle overdue special case)
                if status == "overdue":
                    # Find obligations that are overdue
                    filtered_ids = []
                    for obligation in obligations:
                        if is_obligation_overdue(obligation):
                            filtered_ids.append(obligation.obligation_number)
                    obligations = obligations.filter(obligation_number__in=filtered_ids)
                else:
                    obligations = obligations.filter(status=status)

                # Apply procedure filter (adjusted for TextField)
                if procedure:
                    obligations = obligations.filter(procedure__icontains=procedure)

                return render(
                    request,
                    "obligations/partials/obligation_list.html",
                    {"obligations": obligations},
                )
            except Exception as exc:
                logger.error("Error filtering obligations: %s", str(exc))
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

        if self.request.htmx:
            return render(
                request, "obligations/components/_obligations_summary.html", context
            )

        return render(
            request, "obligations/components/_obligations_summary.html", context
        )

    def _filter_by_status(self, queryset: QuerySet, status_values: list) -> QuerySet:
        """Filter obligations by status, handling 'overdue' as a special case.

        Args:
            queryset: Base queryset
            status_values: List of status values to filter by

        Returns:
            Filtered queryset
        """
        # Handle the special case of 'overdue' which isn't a database field
        if "overdue" in status_values:
            # Remove overdue to handle separately
            standard_statuses = [s for s in status_values if s != "overdue"]

            # Get obligations that match standard statuses
            if standard_statuses:
                filtered_by_status = queryset.filter(status__in=standard_statuses)
            else:
                filtered_by_status = queryset.none()

            # Find overdue obligations
            overdue_ids = []
            for obligation in queryset:
                if is_obligation_overdue(obligation):
                    overdue_ids.append(obligation.obligation_number)

            if overdue_ids:
                # Combine with standard status filter
                overdue_queryset = queryset.filter(obligation_number__in=overdue_ids)
                return filtered_by_status.union(overdue_queryset)
            return filtered_by_status

        # Standard status filtering
        if status_values:
            return queryset.filter(status__in=status_values)
        return queryset

    def apply_filters(self, queryset: QuerySet, filters: dict[str, Any]) -> QuerySet:
        """Apply all filters to the queryset.

        Args:
            queryset: Base queryset
            filters: Dictionary of filter values

        Returns:
            Filtered queryset
        """
        if not queryset:
            return queryset

        # Apply status filter
        if filters.get("status"):
            queryset = self._filter_by_status(queryset, filters["status"])

        # Apply phase filter
        if filters.get("phase"):
            queryset = queryset.filter(project_phase__in=filters["phase"])

        # Apply search filter
        if filters.get("search"):
            search_term = filters["search"]
            queryset = queryset.filter(
                Q(obligation_number__icontains=search_term)
                | Q(obligation__icontains=search_term)
            )

        # Apply date filter
        if filters.get("date_filter"):
            date_filter = filters["date_filter"]
            today = date.today()

            if date_filter == "past_due":
                # Past due - action_due_date is in the past and status isn't completed
                queryset = queryset.filter(
                    action_due_date__lt=today, status__ne="completed"
                )
            elif date_filter == "14days":
                # Due in next 14 days
                future_date = today + timedelta(days=14)
                queryset = queryset.filter(
                    action_due_date__gte=today, action_due_date__lte=future_date
                )
            elif date_filter == "30days":
                # Due in next 30 days
                future_date = today + timedelta(days=30)
                queryset = queryset.filter(
                    action_due_date__gte=today, action_due_date__lte=future_date
                )
            # Add more date filters as needed

        return queryset

    def get_filters(self) -> dict[str, Any]:
        """Extract and normalize filter parameters from request.

        Returns:
            Dictionary of filter parameters
        """
        filters = {}

        # Get query parameters
        status = self.request.GET.getlist("status") or self.request.GET.getlist(
            "status[]"
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

    def get_context_data(self, **kwargs):
        """Get context data for the template.

        Returns:
            Context dictionary for rendering template
        """
        context = {}
        mechanism_id = self.request.GET.get("mechanism_id")

        try:
            # Check if we're coming from user profile (without mechanism_id)
            if not mechanism_id:
                # Get overdue obligations for the current user
                user = self.request.user
                user_roles = []

                # Get user's company roles using the CompanyMembership model directly
                company_memberships = CompanyMembership.objects.filter(user=user)
                if company_memberships:
                    user_roles = list(
                        company_memberships.values_list("role", flat=True).distinct()
                    )

                # Get projects where user is a member using the ProjectMembership model directly
                project_ids = []
                project_memberships = ProjectMembership.objects.filter(user=user)
                if project_memberships:
                    project_ids = list(
                        project_memberships.values_list("project_id", flat=True)
                    )

                # Find obligations that match user's roles and are in their projects
                if user_roles and project_ids:
                    queryset = Obligation.objects.filter(
                        responsibility__in=user_roles, project_id__in=project_ids
                    )

                    # Find overdue obligations
                    overdue_obligations = []
                    for obligation in queryset:
                        if is_obligation_overdue(obligation):
                            overdue_obligations.append(obligation.obligation_number)

                    if overdue_obligations:
                        queryset = queryset.filter(
                            obligation_number__in=overdue_obligations
                        )
                        # Create simple context for displaying just overdue obligations
                        context.update(
                            {
                                "obligations": queryset,
                                "total_count": len(queryset),
                                "filters": {"status": ["overdue"]},
                                "show_overdue_only": True,
                            }
                        )

                        # Add user permissions
                        context["user_can_edit"] = self.request.user.has_perm(
                            "obligations.change_obligation"
                        )

                        return context
                    else:
                        context["error"] = "No overdue obligations found for your role"
                        return context
                else:
                    context["error"] = (
                        "You don't have any company roles or project memberships"
                    )
                    return context

            # Regular mechanism-based view (existing code)
            mechanism = get_object_or_404(EnvironmentalMechanism, id=mechanism_id)

            # Get filters and base queryset
            filters = self.get_filters()
            queryset = Obligation.objects.filter(
                primary_environmental_mechanism=mechanism_id
            )

            # Apply filters and sorting
            queryset = self.apply_filters(queryset, filters)

            sort_field = filters["sort"]
            if filters["order"] == "desc":
                sort_field = f"-{sort_field}"

            queryset = queryset.order_by(sort_field)

            # Paginate results
            paginator = Paginator(queryset, 15)
            page_number = self.request.GET.get("page", 1)
            page_obj = paginator.get_page(page_number)

            # Update context
            context.update(
                {
                    "obligations": page_obj,
                    "page_obj": page_obj,
                    "project": mechanism,
                    "mechanism_id": mechanism_id,
                    "filters": filters,
                    "total_count": paginator.count,
                }
            )

            # Get unique project phases
            phases = (
                Obligation.objects.filter(primary_environmental_mechanism=mechanism_id)
                .exclude(project_phase__isnull=True)
                .exclude(project_phase="")
                .values_list("project_phase", flat=True)
                .distinct()
            )
            context["phases"] = list({phase.strip() for phase in phases})

            # Add user permissions
            context["user_can_edit"] = self.request.user.has_perm(
                "obligations.change_obligation"
            )

        except Exception as exc:
            logger.error("Error in ObligationSummaryView: %s", str(exc))
            context["error"] = f"Error loading obligations: {exc!s}"

        return context


class TotalOverdueObligationsView(LoginRequiredMixin, View):
    """View to get the count of overdue obligations for a project."""

    def get(self, request, *args, **kwargs):
        """Handle GET request to count overdue obligations.

        Args:
            request: HTTP request with project_id parameter

        Returns:
            JsonResponse with count or error
        """
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
        kwargs["responsibilities"] = Responsibility.objects.all()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.request.GET.get("project_id")
        if project_id:
            context["project_id"] = project_id
            try:
                project = Project.objects.get(id=project_id)
                context["project_name"] = project.name
            except Project.DoesNotExist:
                context["project_name"] = "Unknown Project"

        #for current user info
        context["user_id"] = self.request.user.id
        context["user_name"] = self.request.user.get_full_name() or self.request.user.username

        return context

    def form_valid(self, form):
        """Process valid form submission with error handling.

        Args:
            form: The validated form

        Returns:
            Redirect to appropriate page on success
        """
        try:
            # Save the form
            obligation = form.save()

            # Handle primary responsibility
            primary_responsibility = None
            responsibility_str = form.cleaned_data.get("responsibility")
            try:
                primary_responsibility = Responsibility.objects.get(name=responsibility_str)
            except Responsibility.DoesNotExist:
                pass

            if primary_responsibility:
                assignment, created = ResponsibilityAssignment.objects.get_or_create(
                    user=self.request.user,
                    obligation=obligation,
                    role=primary_responsibility,
                    defaults={
                        "responsibility": primary_responsibility,
                        "created_by": self.request.user,
                    }
                )


            # Handle additional responsibilities
            responsibilities = form.cleaned_data.get("responsibilities")
            if responsibilities:
                for responsibility_obj in responsibilities:

                    if not responsibility_obj:
                        continue
                    ResponsibilityAssignment.objects.get_or_create(
                        user=self.request.user,
                        obligation=obligation,
                        responsibility=responsibility_obj,
                        role=primary_responsibility or responsibility_obj,  # fallback to itself
                        created_by=self.request.user,
                    )


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
            logger.error("Validation error in ObligationCreateView: %s", str(exc))
            messages.error(self.request, f"Validation failed: {exc}")
            return self.form_invalid(form)

        except Exception as exc:
            logger.exception("Error creating obligation: %s", str(exc))
            messages.error(self.request, f"Failed to create obligation: {exc!s}")
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

    def get_template_names(self):
        if self.request.htmx:
            return ["obligations/form/partial_update_obligation.html"]
        return [self.template_name]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["project"] = self.object.project
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project_id"] = self.object.project_id
        return context

    def _update_mechanism_counts(
        self, old_mechanism: EnvironmentalMechanism, updated_obligation: Obligation
    ):
        """Update obligation counts for mechanisms.

        Args:
            old_mechanism: Previous mechanism (if any)
            updated_obligation: The updated obligation
        """
        if (
            old_mechanism
            and old_mechanism != updated_obligation.primary_environmental_mechanism
        ):
            old_mechanism.update_obligation_counts()
            if updated_obligation.primary_environmental_mechanism:
                mech = updated_obligation.primary_environmental_mechanism
                mech.update_obligation_counts()
        elif updated_obligation.primary_environmental_mechanism:
            updated_obligation.primary_environmental_mechanism.update_obligation_counts()

    def form_valid(self, form):
        """Process the form submission with HTMX support.

        Args:
            form: The validated form

        Returns:
            Appropriate response based on request type
        """
        try:
            old_mechanism = None
            if self.object.primary_environmental_mechanism:
                old_mechanism = self.object.primary_environmental_mechanism

            # Save the updated obligation
            obligation = form.save()
            self._update_mechanism_counts(old_mechanism, obligation)

            messages.success(
                self.request,
                f"Obligation {obligation.obligation_number} updated successfully.",
            )

            # If this is an HTMX request, return appropriate headers
            if self.request.htmx:
                response = HttpResponse("Obligation updated successfully")
                # Explicitly trigger a refresh for dependent components
                trigger_client_event(
                    response, "path-deps-refresh", {"path": "/obligations/"}
                )
                return response

            # Standard response for regular requests
            if "project_id" in self.request.GET:
                base_url = reverse("dashboard:home")
                proj_id = self.request.GET["project_id"]
                return redirect(f"{base_url}?project_id={proj_id}")
            return redirect("dashboard:home")

        except ValidationError as exc:
            logger.error("Validation error updating obligation: %s", str(exc))
            messages.error(self.request, f"Validation failed: {exc}")
            return self.form_invalid(form)

        except Exception as exc:
            logger.exception("Error updating obligation: %s", str(exc))
            messages.error(self.request, f"Failed to update obligation: {exc!s}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class ObligationDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting an obligation."""

    model = Obligation
    pk_url_kwarg = "obligation_number"

    def post(self, request, *args, **kwargs):
        """Handle POST request for obligation deletion.

        Args:
            request: The HTTP request

        Returns:
            JsonResponse with success or error status
        """
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

        except Exception as exc:
            logger.error("Error deleting obligation: %s", str(exc))
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

    def get(self, request):
        """Handle GET request for toggling custom aspect field.

        Args:
            request: HTTP request with environmental_aspect parameter

        Returns:
            Rendered partial template
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
    paginate_by = 10

    def get_queryset(self):
        project_id = self.request.GET.get("project_id")
        if not project_id:
            return Obligation.objects.none()

        queryset = Obligation.objects.filter(
            project_id=project_id,
        ).order_by("-action_due_date")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project_id"] = self.request.GET.get("project_id")
        return context



def upload_evidence(request, obligation_id):
    """Handle evidence file uploads for an obligation.

    Args:
        request: HTTP request
        obligation_id: ID of the obligation to attach evidence to

    Returns:
        Redirect to appropriate page
    """
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
