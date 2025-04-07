import logging
from typing import List, Optional

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from .forms import BugReportForm
from .models import BugReport
from .proto_utils import (deserialize_bug_report, deserialize_bug_reports,
                          serialize_bug_report, serialize_bug_reports)

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
        logger.error("Error loading plaintext template %s: %s", template_path, e)
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
        return ""

    lines = status_messages.split('\n')
    for line in lines:
        if line.startswith(status + ':'):
            return line.split(':', 1)[1].strip()

    return ""


def get_cached_bug_reports(status_list: Optional[List[str]] = None) -> List[BugReport]:
    """
    Get bug reports from cache if available, otherwise from the database.
    Uses Protocol Buffers for efficient serialization.

    Args:
        status_list: Optional list of statuses to filter by

    Returns:
        List of BugReport instances
    """
    if status_list is None:
        status_list = ['open', 'in_progress']

    cache_key = f"bug_reports_{'-'.join(status_list)}"
    cached_data = cache.get(cache_key)

    if cached_data:
        try:
            # Deserialize the Protocol Buffer data
            bug_reports = deserialize_bug_reports(cached_data)
            logger.debug("Retrieved %d bug reports from cache", len(bug_reports))
            return bug_reports
        except (ValueError, TypeError, ImportError) as e:
            logger.error("Error deserializing cached bug reports: %s", e)

    # Cache miss or error, retrieve from database
    bug_reports = list(BugReport.objects.filter(status__in=status_list))

    # Cache the serialized data for future requests
    try:
        serialized_data = serialize_bug_reports(bug_reports)
        # Cache for 5 minutes
        cache.set(cache_key, serialized_data, 300)
        logger.debug("Cached %d bug reports", len(bug_reports))
    except (ValueError, TypeError, ImportError) as e:
        logger.error("Error serializing bug reports for cache: %s", e)

    return bug_reports


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """
    Main view for the feedback app. Shows list of bug reports and submission form.
    """
    # Get bug reports from cache if available
    bug_reports = get_cached_bug_reports(['open', 'in_progress'])

    # Augment bug reports with status descriptions from plaintext file
    for report in bug_reports:
        report.status_description = get_status_description(report.status)

    # Create a new form for bug report submission
    form = BugReportForm()

    context = {
        'bug_reports': bug_reports,
        'form': form,
    }

    # Use standard Django Template Language (DTL) template
    return render(request, 'feedback/index.html', context)


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

        # Invalidate the bug reports cache
        cache.delete("bug_reports_open-in_progress")

        # Add success message from plaintext template
        success_msg = render_to_string(
            'feedback/form/messages/success.txt',
            {'bug_report': bug_report}
        )
        # Use the message as plain text to avoid XSS vulnerabilities
        messages.success(request, success_msg)

        # Attempt to send confirmation email using plaintext template
        try:
            send_confirmation_email(bug_report)
        except (ValueError, ConnectionError, TimeoutError) as e:
            logger.error("Failed to send confirmation email: %s", e)

        # Check if it's an HTMX request
        if request.headers.get('HX-Request'):
            return render(request, 'feedback/partials/success_message.html', {
                'bug_report': bug_report,
            })

        # Redirect to the feedback index page for regular requests
        return redirect('feedback:index')

    # If form is not valid, redisplay the form with validation errors
    bug_reports = get_cached_bug_reports(['open', 'in_progress'])

    context = {
        'bug_reports': bug_reports,
        'form': form,
    }
    # Add error message from plaintext template
    error_msg = render_to_string(
        'feedback/form/messages/error.txt',
        {'form': form}
    )
    # Use the message as plain text to avoid XSS vulnerabilities
    messages.error(request, error_msg)

    # Check if it's an HTMX request
    if request.headers.get('HX-Request'):
        return render(request, 'feedback/partials/form.html', context)

    # For regular requests, render the full page
    return render(request, 'feedback/index.html', context)


@login_required
def export_report(request: HttpRequest, report_id: int) -> HttpResponse:
    """
    Export a bug report as a binary protocol buffer.

    Args:
        request: The HTTP request
        report_id: The ID of the bug report to export

    Returns:
        Binary response with the serialized bug report
    """
    try:
        bug_report = BugReport.objects.get(id=report_id)

        # Check if the user created the report or is staff
        if bug_report.created_by != request.user and not request.user.is_staff:
            return JsonResponse(
                {'error': 'You do not have permission to export this report'},
                status=403
            )

        # Serialize the bug report to a Protocol Buffer
        serialized_data = serialize_bug_report(bug_report)

        # Return the binary data as a downloadable file
        response = HttpResponse(
            serialized_data,
            content_type='application/x-protobuf'
        )
        response['Content-Disposition'] = (
            f'attachment; filename="bug_report_{report_id}.pb"'
        )

        return response

    except BugReport.DoesNotExist:
        return JsonResponse({'error': 'Bug report not found'}, status=404)
    except (ValueError, TypeError, ImportError) as e:
        logger.error("Error exporting bug report: %s", e)
        return JsonResponse({'error': 'An error occurred during export'}, status=500)


@login_required
def import_report(request: HttpRequest) -> HttpResponse:
    """
    Import a bug report from a binary protocol buffer.

    Args:
        request: The HTTP request

    Returns:
        Redirect to the feedback index page
    """
    if request.method != 'POST' or 'protobuf_file' not in request.FILES:
        return JsonResponse({'error': 'No file uploaded'}, status=400)

    try:
        # Read the binary data from the uploaded file
        uploaded_file = request.FILES['protobuf_file']
        binary_data = uploaded_file.read()

        # Deserialize the Protocol Buffer to a BugReport object
        bug_report = deserialize_bug_report(binary_data)

        # Set the current user as the creator if not set
        if not bug_report.created_by:
            bug_report.created_by = request.user

        # Save to database
        bug_report.save()

        # Invalidate the bug reports cache
        cache.delete("bug_reports_open-in_progress")

        messages.success(
            request,
            f"Bug report '{bug_report.title}' successfully imported"
        )

        return redirect('feedback:index')

    except (ValueError, TypeError, ImportError, OSError) as e:
        logger.error("Error importing bug report: %s", e)
        messages.error(
            request,
            "Failed to import bug report. The file may be corrupted or invalid."
        )
        return redirect('feedback:index')


def send_confirmation_email(bug_report: BugReport) -> None:
    """
    Send a confirmation email to the user who submitted a bug report.

    Args:
        bug_report: The BugReport instance that was created
    """
    if not bug_report.created_by or not bug_report.created_by.email:
        logger.warning(
            "Cannot send confirmation email for bug report %d: no valid email",
            bug_report.id
        )
        return

    template = get_plaintext_template('feedback/email/confirmation.txt')
    if not template:
        logger.error("Email template not found, cannot send confirmation email")
        return

    # Format the email content
    subject = f"Greenova Bug Report Received - {bug_report.title}"

    # Replace placeholder variables in the template
    message = template.format(
        user_name=(
            bug_report.created_by.get_full_name()
            or bug_report.created_by.username
        ),
        title=bug_report.title,
        id=bug_report.id,
        created_at=bug_report.created_at.strftime("%Y-%m-%d %H:%M"),
        severity=bug_report.get_severity_display(),
    )

    # Send the email
    try:
        send_mail(
            subject,
            message,
            None,  # Use default FROM email from settings
            [bug_report.created_by.email],
            fail_silently=False,
        )
        logger.info("Confirmation email sent for bug report %d", bug_report.id)
    except (ConnectionError, TimeoutError, ValueError, OSError) as e:
        logger.error("Failed to send confirmation email: %s", e)
        raise


def send_status_update_email(bug_report: BugReport) -> None:
    """
    Send a status update email to the user who submitted a bug report.

    Args:
        bug_report: The BugReport instance that was updated
    """
    if not bug_report.created_by or not bug_report.created_by.email:
        logger.warning(
            "Cannot send status update email for bug report %d: no valid email",
            bug_report.id,
        )
        return

    template = get_plaintext_template('feedback/email/status_update.txt')
    if not template:
        logger.error("Email template not found, cannot send status update email")
        return

    # Get the status description
    status_description = get_status_description(bug_report.status)

    # Format the email content
    subject = f"Greenova Bug Report #{bug_report.id} - Status Update"

    # Replace placeholder variables in the template
    message = template.format(
        user_name=(
            bug_report.created_by.get_full_name()
            or bug_report.created_by.username
        ),
        title=bug_report.title,
        id=bug_report.id,
        created_at=bug_report.created_at.strftime("%Y-%m-%d %H:%M"),
        status=bug_report.get_status_display(),
        severity=bug_report.get_severity_display(),
        status_description=status_description,
        admin_comment=(
            f"Admin Comment: {bug_report.admin_comment}"
            if bug_report.admin_comment
            else ""
        ),
    )

    # Send the email
    try:
        send_mail(
            subject,
            message,
            None,  # Use default FROM email from settings
            [bug_report.created_by.email],
            fail_silently=False,
        )
        logger.info("Status update email sent for bug report %d", bug_report.id)
    except (ConnectionError, TimeoutError, ValueError, OSError) as e:
        logger.error("Failed to send status update email: %s", e)
        raise
