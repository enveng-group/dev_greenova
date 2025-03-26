from datetime import datetime
import logging
from typing import Any, Dict, Optional, TypedDict, cast

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractUser
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView
from django_htmx.http import HttpResponseClientRefresh, push_url, trigger_client_event
from obligations.models import Obligation
from projects.models import Project

# Constants for system information
SYSTEM_STATUS = "operational"  # or fetch from settings/environment
APP_VERSION = "0.0.4"  # or fetch from settings/environment
LAST_UPDATED = datetime.now().date()  # or fetch from settings/environment

logger = logging.getLogger(__name__)


class DashboardContext(TypedDict):
    """Type definition for dashboard context dictionary."""

    projects: QuerySet[Project]
    selected_project_id: Optional[str]
    system_status: str
    app_version: str
    last_updated: datetime
    user: AbstractUser
    debug: bool
    error: Optional[str]
    user_roles: Dict[str, str]


@method_decorator(cache_control(max_age=60), name="dispatch")
@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
class DashboardHomeView(LoginRequiredMixin, TemplateView):
    """Dashboard home view with enhanced HTMX support."""

    template_name = "dashboard/dashboard.html"
    login_url = "account_login"
    redirect_field_name = "next"

    def get(self, request, *args, **kwargs):
        """Handle GET request with HTMX enhancements."""
        response = super().get(request, *args, **kwargs)

        # If this is an HTMX request, handle history and URL management
        if request.htmx:
            # Push the URL to browser history for navigation
            current_url = request.build_absolute_uri()
            push_url(response, current_url)

            # Trigger dashboard refresh events
            trigger_client_event(response, "dashboardLoaded")

            # Also trigger project selection if project_id is in the request
            project_id = request.GET.get("project_id")
            if project_id:
                trigger_client_event(
                    response, "projectSelected", {"projectId": project_id}
                )

            # If the dashboard data is stale, force a refresh
            if self._is_data_stale():
                return HttpResponseClientRefresh()

        return response

    def _is_data_stale(self) -> bool:
        """Check if dashboard data is stale and needs refresh."""
        # Implement your staleness check logic here
        return False

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Get the context data for template rendering."""
        context = super().get_context_data(**kwargs)

        try:
            user = cast(AbstractUser, self.request.user)
            logger.debug("Getting projects for user: %s", user.username)

            # Use prefetch_related for ManyToMany relationships
            user_projects = (
                Project.objects.filter(memberships__user=user)
                .prefetch_related("memberships", "obligations")
                .distinct()
            )

            # Log project count for debugging
            project_count = user_projects.count()
            logger.info("Found %d projects for user %s", project_count, user.username)

            if project_count == 0:
                logger.warning(
                    "No projects found for user %s. Check project memberships.",
                    user.username,
                )

            # Get the selected project ID from query parameters
            selected_project_id = self.request.GET.get("project_id")

            # Add projects to the context
            context["projects"] = user_projects
            context["selected_project_id"] = selected_project_id

            # Add user roles for each project
            user_roles = {}
            for project in user_projects:
                user_roles[str(project.id)] = project.get_user_role(user)

            context["user_roles"] = user_roles
            context["system_status"] = SYSTEM_STATUS
            context["app_version"] = APP_VERSION
            context["last_updated"] = datetime.combine(
                LAST_UPDATED, datetime.min.time()
            )
            context["debug"] = self.request.GET.get("debug") == "1"
            context["error"] = None

            logger.debug(f"Found {user_projects.count()} projects for user {user}")

            # If a specific project is selected, add it to context
            if selected_project_id:
                try:
                    project = user_projects.get(pk=selected_project_id)
                    # Add project directly instead of projects field
                    context["project"] = project  # Changed from projects=project
                except Project.DoesNotExist:
                    logger.warning(
                        "Selected project not found: %s", selected_project_id
                    )
                    context["error"] = "Selected project not found"

        except Project.DoesNotExist as e:
            logger.warning("Selected project not found: %s", selected_project_id)
            context["error"] = "Selected project not found"
        except Exception as e:
            logger.error("Error preparing dashboard context: %s", str(e), exc_info=True)
            context["error"] = "Could not load dashboard data"
            # Ensure projects exists in context even on error
            context.setdefault("projects", Project.objects.none())
            context.setdefault("user_roles", {})

        return context

    def get_template_names(self):
        if self.request.htmx:
            return ["dashboard/partials/dashboard_content.html"]
        return [self.template_name]

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        """Initialize view setup."""
        super().setup(request, *args, **kwargs)
        self.request = request

    def get_projects(self) -> QuerySet[Project]:
        """Get projects for the current user."""
        try:
            return Project.objects.prefetch_related("obligations", "memberships").all()
        except Exception as e:
            logger.error(f"Error fetching projects: {str(e)}")
            return Project.objects.none()

    @classmethod
    @method_decorator(cache_control(max_age=30))
    def overdue_count(cls, request):
        """
        Returns the count of overdue obligations as plain text for HTMX to swap into the page.
        This endpoint is designed to be called via hx-get and refreshed periodically.
        """
        try:
            count = Obligation.objects.filter(recurring_status="overdue").count()

            if request.htmx:
                response = render(
                    request, "dashboard/partials/overdue_count.html", {"count": count}
                )
            else:
                response = HttpResponse(str(count))

            # When the count is over a threshold, highlight it by triggering a CSS change
            if count > 5:
                trigger_client_event(
                    response, "highOverdueCount", params={"count": count}
                )

            return response

        except Obligation.DoesNotExist:
            logger.error("No overdue obligations found.")
            return HttpResponse("0")
        except Exception as e:
            logger.error("Error counting overdue items: %s", str(e))
            return HttpResponse("0")


class DashboardProfileView(TemplateView):
    """Profile view."""

    template_name = "dashboard/profile.html"
    login_url = "account_login"
    redirect_field_name = "next"
