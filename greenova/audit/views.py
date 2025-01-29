from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from .models import AuditLog


@login_required(login_url="login")
def audit_log_view(request):
    audit_logs = AuditLog.objects.all()
    paginator = Paginator(audit_logs, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "audit.html", {"page_obj": page_obj})
