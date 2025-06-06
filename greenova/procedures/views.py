"""Views for the procedures app.

This module provides views for displaying, exporting, and importing
procedure data, including chart rendering and API endpoints.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

# Standard library imports
import logging
from datetime import timedelta
from typing import Any

# Third-party library imports
import matplotlib as mpl
from beartype import beartype
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView, ListView
from guardian.shortcuts import assign_perm
from mechanisms.models import EnvironmentalMechanism
from obligations.models import Obligation
from responsibility.figures import figure_to_svg, get_responsibility_chart

# Local application imports
from .figures import get_procedure_charts_svg as get_all_procedure_charts_svg
from .models import Procedure
from .serializers import ProcedureCollectionProtoSerializer, ProcedureProtoSerializer

mpl.use("Agg")  # Use Agg backend for non-interactive plotting
logger = logging.getLogger(__name__)


class ProcedureListView(LoginRequiredMixin, ListView):
    """List view for all procedures.

    Displays all procedures in the system, ordered by name.
    """
    model = Procedure
    template_name = "procedures/procedures_list.html"
    context_object_name = "procedures"

    def get_queryset(self):
        """Return all procedures ordered by name."""
        return Procedure.objects.all().order_by("name")
"""Views for the procedures app.

This module provides views for displaying, exporting, and importing
procedure data, including chart rendering and API endpoints.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

# Standard library imports
import logging
from datetime import timedelta
from typing import Any

# Third-party library imports
import matplotlib as mpl
from beartype import beartype
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView
from guardian.shortcuts import assign_perm
from mechanisms.models import EnvironmentalMechanism
from obligations.models import Obligation
from responsibility.figures import figure_to_svg, get_responsibility_chart

# Local application imports
from .figures import get_procedure_charts_svg as get_all_procedure_charts_svg
from .models import Procedure
from .serializers import ProcedureCollectionProtoSerializer, ProcedureProtoSerializer

mpl.use("Agg")  # Use Agg backend for non-interactive plotting
logger = logging.getLogger(__name__)


@method_decorator(cache_control(max_age=300), name="dispatch")
@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
class ProcedureChartsView(LoginRequiredMixin, TemplateView):
    """View for displaying procedure charts filtered by environmental mechanism."""

    template_name = "procedures/procedure_charts.html"

    @beartype
    def _get_mechanism_and_obligations(
        self,
        mechanism_id: Any,
    ) -> tuple[EnvironmentalMechanism, Any]:
        """Get mechanism and obligations for the given mechanism ID.

        Args:
            mechanism_id: The ID of the environmental mechanism.

        Returns:
            A tuple containing the EnvironmentalMechanism instance and obligations queryset.

        """
        mechanism = get_object_or_404(EnvironmentalMechanism, id=mechanism_id)
        query = Obligation.objects
        query = query.filter(primary_environmental_mechanism_id=mechanism_id)
        all_obligations = query
        return mechanism, all_obligations

    @beartype
    def _apply_filters(
        self,
        obligations: Any,
        request_params: Any,
    ) -> tuple[Any, dict[str, Any]]:
        """Apply filters to obligations based on request parameters.

        Args:
            obligations: The queryset of obligations.
            request_params: The request GET parameters.

        Returns:
            A tuple of (filtered obligations queryset, filter parameters dict).

        """
        filtered_obligations = obligations
        phase_filter = request_params.get("phase", "")
        responsibility_filter = request_params.get("responsibility", "")
        status_filter = request_params.get("status", "")
        look_ahead = request_params.get("lookahead", "") == "14days"
        overdue_only = request_params.get("overdue", "") == "true"

        if phase_filter:
            filtered_obligations = filtered_obligations.filter(
                project_phase=phase_filter,
            )

        if responsibility_filter:
            filtered_obligations = filtered_obligations.filter(
                responsibility=responsibility_filter,
            )

        if status_filter:
            filtered_obligations = filtered_obligations.filter(
                status=status_filter,
            )

        if look_ahead:
            today = timezone.now().date()
            future_date = today + timedelta(days=14)
            filtered_obligations = filtered_obligations.filter(
                action_due_date__gte=today,
                action_due_date__lte=future_date,
            )

        if overdue_only:
            today = timezone.now().date()
            filtered_obligations = filtered_obligations.filter(
                action_due_date__lt=today,
            ).exclude(status="completed")

        filters_applied = any(
            [
                phase_filter,
                responsibility_filter,
                status_filter,
                look_ahead,
                overdue_only,
            ],
        )

        filter_params = {
            "phase_filter": phase_filter,
            "responsibility_filter": responsibility_filter,
            "status_filter": status_filter,
            "look_ahead": look_ahead,
            "overdue_only": overdue_only,
            "filters_applied": filters_applied,
        }

        return filtered_obligations, filter_params

    @beartype
    def _calculate_statistics(self, all_obligations: Any) -> dict[str, int]:
        """Calculate statistics based on all obligations.

        Args:
            all_obligations: The queryset of all obligations.

        Returns:
            A dictionary with total, completed, remaining, and percentage.

        """
        total = all_obligations.count()
        completed = all_obligations.filter(status="completed").count()
        remaining = total - completed

        completion_percentage = int(completed / total * 100) if total > 0 else 0

        return {
            "total": total,
            "completed": completed,
            "remaining": remaining,
            "percentage": completion_percentage,
        }

    @beartype
    def _get_available_filters(self, all_obligations: Any) -> dict[str, Any]:
        """Get available filter options from obligations.

        Args:
            all_obligations: The queryset of all obligations.

        Returns:
            A dictionary with available phases, responsibilities, and status options.

        """
        phases = (
            all_obligations.values_list(
                "project_phase",
                flat=True,
            )
            .distinct()
            .order_by("project_phase")
        )

        responsibilities = (
            all_obligations.values_list(
                "responsibility",
                flat=True,
            )
            .distinct()
            .order_by("responsibility")
        )

        status_options = [
            ("not started", "Not Started"),
            ("in progress", "In Progress"),
            ("completed", "Completed"),
        ]

        return {
            "phases": phases,
            "responsibilities": responsibilities,
            "status_options": status_options,
        }

    @beartype
    def _generate_responsibility_chart(
        self,
        mechanism_id: Any,
        filtered_obligations: Any = None,
        filters_applied: bool = False,
    ) -> str:
        """Generate responsibility chart as SVG based on filtered obligations.

        Args:
            mechanism_id: The ID of the environmental mechanism.
            filtered_obligations: The filtered obligations queryset.
            filters_applied: Whether filters are applied.

        Returns:
            SVG string of the responsibility chart.

        """
        if filters_applied and filtered_obligations is not None:
            filtered_ids = filtered_obligations.values_list("id", flat=True)
            fig = get_responsibility_chart(
                mechanism_id,
                filtered_ids=filtered_ids,
            )
        else:
            fig = get_responsibility_chart(mechanism_id)
        return figure_to_svg(fig)

    @beartype
    def _generate_procedure_charts(
        self,
        mechanism_id: Any,
        filtered_obligations: Any,
        all_obligations: Any,
        filters_applied: bool,
    ) -> list[dict[str, Any]]:
        """Generate SVG charts for each procedure.

        Args:
            mechanism_id: The ID of the environmental mechanism.
            filtered_obligations: The filtered obligations queryset.
            all_obligations: The queryset of all obligations.
            filters_applied: Whether filters are applied.

        Returns:
            A list of dictionaries with procedure chart data.

        """
        procedure_charts = []

        # Get filtered IDs if filters are applied
        filtered_ids = None
        if filters_applied:
            filtered_ids = filtered_obligations.values_list("id", flat=True)

        # Generate charts for each procedure
        charts_dict = get_all_procedure_charts_svg(
            mechanism_id,
            filtered_ids=filtered_ids,
        )

        for procedure_name, svg in charts_dict.items():
            # Create procedure chart data
            procedure_data = self._create_procedure_chart_data(
                procedure_name,
                svg,
                filtered_obligations if filters_applied else all_obligations,
            )
            procedure_charts.append(procedure_data)

        return procedure_charts

    @beartype
    def _create_procedure_chart_data(
        self,
        procedure_name: Any,
        svg: str,
        obligations: Any,
    ) -> dict[str, Any]:
        """Create data for a specific procedure chart as SVG.

        Args:
            procedure_name: The name of the procedure.
            svg: The SVG string for the chart.
            obligations: The queryset of obligations.

        Returns:
            A dictionary with procedure chart data.

        """
        # Get obligations for this procedure
        proc_obligations = obligations.filter(procedure=procedure_name)

        # Count status types
        status_counts = {
            "not_started": sum(
                1 for o in proc_obligations if o.status == "not started"
            ),
            "in_progress": sum(
                1 for o in proc_obligations if o.status == "in progress"
            ),
            "completed": sum(1 for o in proc_obligations if o.status == "completed"),
            "overdue": sum(1 for o in proc_obligations if o.is_overdue),
        }
        status_counts["total"] = (
            status_counts["not_started"]
            + status_counts["in_progress"]
            + status_counts["completed"]
        )
        return {
            "name": procedure_name,
            "chart": svg,
            "stats": status_counts,
        }

    @beartype
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Get context data for rendering the template.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            A dictionary with context data for the template.

        """
        context = super().get_context_data(**kwargs)

        # Get mechanism ID from kwargs or request
        mechanism_id = self.kwargs.get("mechanism_id")
        if not mechanism_id:
            mechanism_id = self.request.GET.get("mechanism_id")

        if not mechanism_id:
            context["error"] = "No mechanism selected"
            return context

        try:
            # Get mechanism and obligations
            mechanism, all_obligations = self._get_mechanism_and_obligations(
                mechanism_id,
            )
            context["mechanism"] = mechanism

            # Apply filters from request
            filtered_obligations, filter_params = self._apply_filters(
                all_obligations,
                self.request.GET,
            )

            # Calculate statistics
            stats = self._calculate_statistics(all_obligations)

            # Get available filter options
            filter_options = self._get_available_filters(all_obligations)

            # Update context with basic data
            context.update(
                {
                    "total_obligations": stats["total"],
                    "completed_obligations": stats["completed"],
                    "remaining_obligations": stats["remaining"],
                    "completion_percentage": stats["percentage"],
                    # Save filter state for template
                    "filter_phase": filter_params["phase_filter"],
                    "filter_responsibility": filter_params["responsibility_filter"],
                    "filter_status": filter_params["status_filter"],
                    "filter_lookahead": filter_params["look_ahead"],
                    "filter_overdue": filter_params["overdue_only"],
                    # Add available filter options
                    "available_phases": filter_options["phases"],
                    "available_responsibilities": filter_options["responsibilities"],
                    "status_options": filter_options["status_options"],
                },
            )

            # Generate responsibility chart
            responsibility_chart_img = self._generate_responsibility_chart(
                mechanism_id,
                filtered_obligations,
                filter_params["filters_applied"],
            )
            context["responsibility_chart"] = responsibility_chart_img

            # Generate procedure charts
            procedure_charts = self._generate_procedure_charts(
                mechanism_id,
                filtered_obligations,
                all_obligations,
                filter_params["filters_applied"],
            )
            context["procedure_charts"] = procedure_charts

            # Add table data for all procedures
            context["table_data"] = [
                {
                    "name": chart["name"],
                    "not_started": chart["stats"]["not_started"],
                    "in_progress": chart["stats"]["in_progress"],
                    "completed": chart["stats"]["completed"],
                    "overdue": chart["stats"]["overdue"],
                    "total": chart["stats"]["total"],
                }
                for chart in procedure_charts
            ]

        except (
            EnvironmentalMechanism.DoesNotExist,
            Obligation.DoesNotExist,
            ValueError,
            TypeError,
        ) as exc:
            logger.exception("Error generating procedure charts: %s", str(exc))
            context["error"] = f"Error generating charts: {exc!s}"

        return context


@beartype
def create_procedure_with_permissions(user: Any, form: Any) -> Procedure:
    """Create a procedure and assign object-level permissions to the creator.

    Args:
        user: The user creating the procedure.
        form: The validated ProcedureForm instance.

    Returns:
        The created Procedure instance.

    """
    procedure = form.save(commit=False)
    procedure.save()
    form.save_m2m()
    # Assign object-level permissions to creator
    assign_perm("view_procedure", user, procedure)
    assign_perm("change_procedure", user, procedure)
    assign_perm("delete_procedure", user, procedure)
    return procedure


@beartype
@login_required
@require_http_methods(["GET"])
def export_procedure(request: Any, procedure_id: int) -> HttpResponse:
    """Export a single procedure as Protocol Buffer binary data.

    Args:
        request: The HTTP request object.
        procedure_id: The ID of the procedure to export.

    Returns:
        HttpResponse: The HTTP response with the exported data.

    """
    procedure = get_object_or_404(Procedure, id=procedure_id)
    serializer = ProcedureProtoSerializer(instance=procedure)
    data = serializer.data()
    if not data:
        return JsonResponse({"error": "Failed to export procedure."}, status=400)
    response = HttpResponse(data, content_type="application/octet-stream")
    response["Content-Disposition"] = (
        f'attachment; filename="procedure_{procedure_id}.pb"'
    )
    return response


@beartype
@login_required
@require_http_methods(["GET"])
def export_all_procedures(request: Any) -> HttpResponse:
    """Export all procedures as a Protocol Buffer collection.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The HTTP response with the exported data.

    """
    procedures = list(Procedure.objects.all())
    serializer = ProcedureCollectionProtoSerializer(instances=procedures)
    data = serializer.data()
    if not data:
        return JsonResponse({"error": "Failed to export procedures."}, status=400)
    response = HttpResponse(data, content_type="application/octet-stream")
    response["Content-Disposition"] = 'attachment; filename="procedures.pb"'
    return response


@beartype
@csrf_exempt
@login_required
@require_http_methods(["POST"])
def import_procedure(request: Any) -> HttpResponse:
    """Import a procedure from Protocol Buffer binary data.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The HTTP response after importing.

    """
    data = request.body
    serializer = ProcedureProtoSerializer(data=data)
    if not serializer.is_valid():
        return JsonResponse({"error": serializer.errors}, status=400)
    procedure = serializer.save()
    return JsonResponse(
        {"id": procedure.id, "message": "Procedure imported successfully."},
    )
