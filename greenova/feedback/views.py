import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from .forms import BugReportForm
from .models import BugReport
from .proto_utils import deserialize_bug_report, serialize_bug_report

logger = logging.getLogger(__name__)


def get_plaintext_template(template_path: str) -> str:
    """
    Load and return the contents of a plaintext template file.

    Args:
        template_path: The relative path to the template file from the templates
        directory

    Returns:
        The contents of the plaintext template file
    """
    try:
        return render_to_string(template_path)
    except (FileNotFoundError, OSError, ValueError) as e:
        logger.error("Failed to load template %s: %s", template_path, str(e))
        return ""


def get_status_description(status: str) -> str:
    """
    Get the description for a bug report status from the plaintext template.

    Args:
        status: The status key (open, in_progress, resolved, closed, rejected)

    Returns:
        The description for the given status
    """
    status_messages = get_plaintext_template('feedback/status/status_messages.txt')
    if not status_messages:
        logger.warning("Status message template not found")
        return ""

    lines = status_messages.split('\n')
    for line in lines:
        if line.startswith(status + ':'):
            return line[len(status) + 1:].strip()

    return ""


def index(request: HttpRequest) -> HttpResponse:
    """
    Display the main feedback page showing bug reports and submission form.

    Args:
        request: The HTTP request

    Returns:
        HTTP response with rendered template
    """
    # Get all bug reports if user is staff, otherwise only show the user's reports
    if request.user.is_authenticated and request.user.is_staff:
        bug_reports = BugReport.objects.all().order_by('-created_at')
    elif request.user.is_authenticated:
        bug_reports = (BugReport.objects
                       .filter(created_by=request.user)
                       .order_by('-created_at'))
    else:
        bug_reports = []

    context = {
        'bug_reports': bug_reports,
        'page_title': _('Bug Reports'),
    }

    return render(request, 'feedback/index.html', context)


@login_required
def submit_bug_report(request: HttpRequest) -> HttpResponse:
    """
    Handle bug report submission form.

    Args:
        request: The HTTP request

    Returns:
        HTTP response with form or redirect to index
    """
    if request.method == 'POST':
        form = BugReportForm(request.POST)
        if form.is_valid():
            # Save but don't commit to attach the user
            bug_report = form.save(commit=False)
            bug_report.created_by = request.user
            bug_report.status = 'open'  # Default status
            bug_report.save()

            # Show success message
            messages.success(
                request,
                _('Bug report submitted successfully. Thank you for your feedback!')
            )

            # Notify administrators
            try:
                admin_emails = []  # Replace with actual admin emails logic
                if admin_emails:
                    subject = f'New Bug Report: {bug_report.title}'
                    message = render_to_string('feedback/email/new_bug_report.txt', {
                        'bug_report': bug_report,
                        'user': request.user,
                    })
                    send_mail(
                        subject,
                        message,
                        None,  # Use DEFAULT_FROM_EMAIL
                        admin_emails,
                        fail_silently=True,
                    )
            except (
                ValueError,
                TypeError,
                ConnectionError,
                OSError,
                ImportError,
            ) as e:
                logger.error("Failed to send admin notification: %s", str(e))

            return redirect('feedback:index')
    else:
        # Pre-fill environment info if available
        initial_data = {
            'application_version': getattr(request, 'application_version', ''),
            'operating_system': request.headers.get('user-agent', ''),
            'browser': request.headers.get('user-agent', ''),
            'device_type': 'Desktop',  # Default, can be improved with device detection
        }
        form = BugReportForm(initial=initial_data)

    context = {
        'form': form,
        'page_title': _('Submit Bug Report'),
    }

    return render(request, 'feedback/submit_bug_report.html', context)


@login_required
def export_report(request: HttpRequest, report_id: int) -> HttpResponse:
    """
    Export a bug report as Protocol Buffer binary data.

    Args:
        request: The HTTP request
        report_id: The ID of the bug report to export

    Returns:
        HTTP response with binary data or redirect
    """
    # Get the bug report, ensuring the user has access
    if request.user.is_staff:
        bug_report = get_object_or_404(BugReport, id=report_id)
    else:
        bug_report = get_object_or_404(BugReport, id=report_id, created_by=request.user)

    # Serialize the bug report
    serialized_data = serialize_bug_report(bug_report)

    if not serialized_data:
        messages.error(request, _('Failed to export bug report.'))
        return redirect('feedback:index')

    # Create response with binary data
    response = HttpResponse(serialized_data, content_type='application/octet-stream')
    filename = f'attachment; filename="bug_report_{report_id}.pb"'
    response['Content-Disposition'] = filename

    return response


@login_required
@require_http_methods(["GET", "POST"])
def import_report(request: HttpRequest) -> HttpResponse:
    """
    Import a bug report from Protocol Buffer binary data.

    Args:
        request: The HTTP request

    Returns:
        HTTP response with success/error message or form
    """
    if request.method == 'POST':
        if 'file' not in request.FILES:
            messages.error(request, _('No file was provided.'))
            return redirect('feedback:import_report')

        uploaded_file = request.FILES['file']

        try:
            # Read and deserialize the file
            data = uploaded_file.read()
            bug_report = deserialize_bug_report(data)

            if not bug_report:
                messages.error(
                    request, _('Could not deserialize the file. Invalid format.')
                )
                return redirect('feedback:import_report')

            # Set the creator to the current user
            bug_report.created_by = request.user
            bug_report.id = None  # Ensure a new record is created
            bug_report.save()

            messages.success(request, _('Bug report imported successfully.'))
            return redirect('feedback:index')

        except (ValueError, OSError, AttributeError, TypeError) as e:
            logger.error("Error importing bug report: %s", str(e))
            messages.error(
                request,
                _('An error occurred while importing the bug report.')
            )
            return redirect('feedback:import_report')

    # GET request - show import form
    return render(request, 'feedback/import_report.html', {
        'page_title': _('Import Bug Report'),
    })
