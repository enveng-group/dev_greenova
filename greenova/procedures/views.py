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

"""Views for procedure analysis and charts."""

import io
import base64
import logging
from datetime import timedelta
import matplotlib as mpl
from beartype import beartype
from core.types import QuerySet as CoreQuerySet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers
from django.views.generic import ListView, TemplateView
from mechanisms.models import EnvironmentalMechanism
from obligations.models import Obligation
from .models import Procedure
from .figures import get_procedure_charts as get_all_procedure_charts


mpl.use("Agg")  # Use Agg backend for non-interactive plotting
logger = logging.getLogger(__name__)


@method_decorator(cache_control(max_age=300), name="dispatch")
@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
class ProcedureChartsView(LoginRequiredMixin, TemplateView):
    """View for displaying procedure charts filtered by environmental mechanism."""

    template_name = "procedures/procedure_charts.html"

    def get_template_names(self) -> list[str]:
        """Return appropriate template based on request type."""
        if hasattr(self.request, "htmx") and getattr(self.request, "htmx", False):
            return ["procedures/components/_procedure_charts.html"]
        return [self.template_name]

    @beartype
    def _get_mechanism_and_obligations(
        self, mechanism_id: int,
    ) -> tuple[EnvironmentalMechanism, CoreQuerySet[Obligation]]:
        """Get mechanism and obligations for the given mechanism ID."""
        mechanism = get_object_or_404(EnvironmentalMechanism, id=mechanism_id)
        query = Obligation.objects
        query = query.filter(primary_environmental_mechanism_id=mechanism_id)
        all_obligations = query
        return mechanism, all_obligations

    @beartype
    def _apply_filters(
        self, obligations: CoreQuerySet[Obligation], request_params: dict[str, str],
    ) -> tuple[CoreQuerySet[Obligation], dict[str, object]]:
        """Apply filters to obligations based on request parameters."""
        # Convert QueryDict to dict if needed
        if hasattr(request_params, "dict"):
            params = dict(request_params)
        else:
            params = request_params
        filtered_obligations = obligations
        phase_filter = params.get("phase", "")
        responsibility_filter = params.get("responsibility", "")
        status_filter = params.get("status", "")
        look_ahead = params.get("lookahead", "") == "14days"
        overdue_only = params.get("overdue", "") == "true"
        if phase_filter:
            filtered_obligations = filtered_obligations.filter(
                project_phase=phase_filter,
            )
        if responsibility_filter:
            filtered_obligations = filtered_obligations.filter(
                responsibility=responsibility_filter,
            )
        if status_filter:
            filtered_obligations = filtered_obligations.filter(status=status_filter)
        if look_ahead:
            today = timezone.now().date()
            future_date = today + timedelta(days=14)
            filtered_obligations = filtered_obligations.filter(
                action_due_date__gte=today, action_due_date__lte=future_date,
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
    def _calculate_statistics(
            self, all_obligations: CoreQuerySet[Obligation]) -> dict[str, int]:
        """Calculate statistics based on all obligations."""
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
    def _get_available_filters(
            self, all_obligations: CoreQuerySet[Obligation]) -> dict[str, object]:
        """Get available filter options from obligations."""
        phases = (
            all_obligations.values_list("project_phase", flat=True)
            .distinct()
            .order_by("project_phase")
        )
        responsibilities = (
            all_obligations.values_list("responsibility", flat=True)
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
    def _generate_procedure_charts(
        self,
        mechanism_id: int,
        filtered_obligations: CoreQuerySet[Obligation],
        all_obligations: CoreQuerySet[Obligation],
        filters_applied: bool,
    ) -> list[dict[str, object]]:
        """Generate charts for each procedure."""
        procedure_charts = []
        filtered_ids = None
        if filters_applied:
            filtered_ids = filtered_obligations.values_list("id", flat=True)
        charts_dict = get_all_procedure_charts(
            mechanism_id, filtered_ids=filtered_ids,
        )
        for procedure_name, fig in charts_dict.items():
            procedure_data = self._create_procedure_chart_data(
                procedure_name,
                fig,
                filtered_obligations if filters_applied else all_obligations,
            )
            procedure_charts.append(procedure_data)
        return procedure_charts

    @beartype
    def _create_procedure_chart_data(
        self,
        procedure_name: str,
        fig: Figure,
        obligations: CoreQuerySet[Obligation],
    ) -> dict[str, object]:
        """Create data for a specific procedure chart."""
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        base64_data = base64.b64encode(buf.getvalue()).decode()
        chart_img = (
            f'<img src="data:image/png;base64,{base64_data}" '
            f'alt="{procedure_name} Chart" '
            f'width="300" height="250">'
        )
        proc_obligations = obligations.filter(procedure=procedure_name)
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
            "chart": chart_img,
            "stats": status_counts,
        }

    @beartype
    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        """Get context data for rendering the template."""
        context = super().get_context_data(**kwargs)
        mechanism_id = self.kwargs.get("mechanism_id")
        if not mechanism_id:
            mechanism_id = self.request.GET.get("mechanism_id")
        if not mechanism_id:
            context["error"] = "No mechanism selected"
            return context
        try:
            mechanism, all_obligations = self._get_mechanism_and_obligations(
                int(mechanism_id),
            )
            context["mechanism"] = mechanism
            filtered_obligations, filter_params = self._apply_filters(
                all_obligations, self.request.GET,
            )
            stats = self._calculate_statistics(all_obligations)
            filter_options = self._get_available_filters(all_obligations)
            context.update(
                {
                    "total_obligations": stats["total"],
                    "completed_obligations": stats["completed"],
                    "remaining_obligations": stats["remaining"],
                    "completion_percentage": stats["percentage"],
                    "filter_phase": filter_params["phase_filter"],
                    "filter_responsibility": filter_params["responsibility_filter"],
                    "filter_status": filter_params["status_filter"],
                    "filter_lookahead": filter_params["look_ahead"],
                    "filter_overdue": filter_params["overdue_only"],
                    "available_phases": filter_options["phases"],
                    "available_responsibilities": filter_options["responsibilities"],
                    "status_options": filter_options["status_options"],
                },
            )
            procedure_charts = self._generate_procedure_charts(
                int(mechanism_id),
                filtered_obligations,
                all_obligations,
                filter_params["filters_applied"],
            )
            context["procedure_charts"] = procedure_charts
        except Exception as exc:
            logger.exception("Error generating procedure charts: %s", exc)
            context["error"] = str(exc)
        return context


class ProcedureListView(LoginRequiredMixin, ListView):
    """List all procedures."""

    model = Procedure
    template_name = "procedures/procedures_list.html"
    context_object_name = "procedures"

    @beartype
    def get_queryset(self) -> CoreQuerySet[Procedure]:
        """Return all Procedure objects for the list view.

        Returns:
            QuerySet: All Procedure objects.

        """
        return Procedure.objects.all()
