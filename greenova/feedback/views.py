import logging
from typing import Any, Dict, Union

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_http_methods

from .forms import BugReportForm
from .models import BugReport

logger = logging.getLogger(__name__)

@login_required
def index(request: HttpRequest) -> HttpResponse:
    """
    Main view for the feedback app. Shows list of bug reports and submission form.
    """
    # Get all open bug reports
    bug_reports = BugReport.objects.filter(status__in=['open', 'in_progress'])

    # Create a new form for bug report submission
    form = BugReportForm()

    context = {
        'bug_reports': bug_reports,
        'form': form,
    }

    # Return Jinja2 template instead of DTL template
    # The .jinja extension will help Django identify which template engine to use
    return render(request, 'feedback/index.jinja', context)

@login_required
@require_http_methods(['POST'])
def submit_bug_report(request: HttpRequest) -> HttpResponse:
    """
    Handle submission of a new bug report.
    """
    form = BugReportForm(request.POST)

    if form.is_valid():
        # Save the form but don't commit to DB yet
        bug_report = form.save(commit=False)

        # Set the current user as the creator
        bug_report.created_by = request.user

        # Save to database
        bug_report.save()

        # Add success message
        success_msg = render_to_string(
            'feedback/form/messages/success.txt',
            {'bug_report': bug_report}
        )
        messages.success(request, mark_safe(success_msg))

        # Check if it's an HTMX request
        if request.headers.get('HX-Request'):
            return render(request, 'feedback/partials/success_message.jinja', {
                'bug_report': bug_report,
            })

        # Redirect to the feedback index page for regular requests
        return redirect('feedback:index')

    # If form is not valid, redisplay the form with validation errors
    bug_reports = BugReport.objects.filter(status__in=['open', 'in_progress'])

    context = {
        'bug_reports': bug_reports,
        'form': form,
    }

    # Add error message
    error_msg = render_to_string(
        'feedback/form/messages/error.txt',
        {'form': form}
    )
    messages.error(request, mark_safe(error_msg))

    # Check if it's an HTMX request
    if request.headers.get('HX-Request'):
        return render(request, 'feedback/partials/form.jinja', context)

    # For regular requests, render the full page
    return render(request, 'feedback/index.jinja', context)
