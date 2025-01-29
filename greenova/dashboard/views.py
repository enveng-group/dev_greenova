import json
from datetime import timedelta

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from obligations.models import Obligation


@login_required(login_url="/login/")
def dashboard_view(request):
    today = timezone.now().date()

    # Enhanced status data with obligation numbers
    status_data = {}
    for status in Obligation.STATUS_CHOICES:
        obligations = Obligation.objects.filter(status=status[0])
        status_data[status[0]] = {
            "status": status[1],
            "count": obligations.count(),
            "obligations": list(
                obligations.values(
                    "obligation_number",
                    "project_name",
                    "environmental_aspect",
                    "accountability",
                    "action_due_date",
                    "status",
                    "responsibility_id",
                    "evidence",
                )
            ),
        }

    # Format dates in obligations list
    for data in status_data.values():
        for obligation in data["obligations"]:
            if obligation["action_due_date"]:
                obligation["action_due_date"] = obligation[
                    "action_due_date"
                ].strftime("%Y-%m-%d")

    # Convert to list format for Chart.js
    status_chart_data = [
        {
            "status": data["status"],
            "count": data["count"],
            "obligations": data["obligations"],
        }
        for status, data in status_data.items()
    ]

    # Risk assessment data
    risk_data = list(
        Obligation.objects.values(
            "project_name", "environmental_aspect"
        ).annotate(
            total=Count("obligation_number"),
            overdue=Count(
                "obligation_number",
                filter=Q(
                    action_due_date__lt=today,
                    status__in=["not_started", "in_progress"],
                ),
            ),
            compliant=Count("obligation_number", filter=Q(status="completed")),
        )
    )

    # Timeline analysis
    timeline_data = {
        "overdue": list(
            Obligation.objects.filter(
                action_due_date__lt=today,
                status__in=["not_started", "in_progress"],
            ).values(
                "action_due_date",
                "obligation_number",
                "project_name",
                "status",
                "environmental_aspect",
                "accountability",
            )
        ),
        "week": list(
            Obligation.objects.filter(
                action_due_date__range=[today, today + timedelta(days=7)]
            ).values(
                "action_due_date",
                "obligation_number",
                "project_name",
                "status",
                "environmental_aspect",
                "accountability",
            )
        ),
        "fortnight": list(
            Obligation.objects.filter(
                action_due_date__range=[today, today + timedelta(days=14)]
            ).values(
                "action_due_date",
                "obligation_number",
                "project_name",
                "status",
                "environmental_aspect",
                "accountability",
            )
        ),
        "month": list(
            Obligation.objects.filter(
                action_due_date__range=[today, today + timedelta(days=30)]
            ).values(
                "action_due_date",
                "obligation_number",
                "project_name",
                "status",
                "environmental_aspect",
                "accountability",
            )
        ),
    }

    # Format dates
    for period in timeline_data.values():
        for item in period:
            if "action_due_date" in item:
                item["action_due_date"] = item["action_due_date"].strftime(
                    "%Y-%m-%d"
                )

    context = {
        "user": request.user,
        "status_data": json.dumps(status_chart_data),
        "risk_data": json.dumps(risk_data),
        "timeline_data": json.dumps(timeline_data),
    }
    return render(request, "dashboard.html", context)


@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return redirect("index")
