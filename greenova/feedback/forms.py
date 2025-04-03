from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import BugReport


class BugReportForm(forms.ModelForm):
    """Form for submitting detailed bug reports."""

    class Meta:
        model = BugReport
        fields = [
            # Summary section
            'title', 'description',
            # Environment section
            'application_version', 'operating_system', 'browser', 'device_type',
            # Steps section
            'steps_to_reproduce', 'expected_behavior', 'actual_behavior',
            # Technical details
            'error_messages', 'trace_report',
            # Frequency and impact
            'frequency', 'impact_severity', 'user_impact',
            # Additional info
            'workarounds', 'additional_comments',
        ]

        widgets = {
            # Summary section
            'title': forms.TextInput(attrs={'size': '80'}),
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 80}),

            # Environment section
            'application_version': forms.TextInput(attrs={'size': '20'}),
            'operating_system': forms.TextInput(attrs={'size': '50'}),
            'browser': forms.TextInput(attrs={'size': '50'}),
            'device_type': forms.TextInput(attrs={'size': '50'}),

            # Steps section
            'steps_to_reproduce': forms.Textarea(attrs={'rows': 8, 'cols': 80}),
            'expected_behavior': forms.Textarea(attrs={'rows': 3, 'cols': 80}),
            'actual_behavior': forms.Textarea(attrs={'rows': 3, 'cols': 80}),

            # Technical details
            'error_messages': forms.Textarea(attrs={'rows': 5, 'cols': 80}),
            'trace_report': forms.Textarea(attrs={'rows': 10, 'cols': 80}),

            # Frequency and impact
            'frequency': forms.Select(),
            'impact_severity': forms.Select(),
            'user_impact': forms.Textarea(attrs={'rows': 3, 'cols': 80}),

            # Additional info
            'workarounds': forms.Textarea(attrs={'rows': 3, 'cols': 80}),
            'additional_comments': forms.Textarea(attrs={'rows': 3, 'cols': 80}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Mark most fields as required
        required_fields = [
            'title', 'description', 'application_version', 'operating_system',
            'device_type', 'steps_to_reproduce', 'expected_behavior',
            'actual_behavior', 'frequency', 'impact_severity', 'user_impact'
        ]

        # Load the mandatory field message
        mandatory_message = render_to_string('feedback/form/messages/mandatory_item.txt')

        # Add detailed help text for all fields
        field_help = {
            'title': _("A brief, descriptive title of the issue. Example: 'Dashboard fails to load environmental metrics when filtering by project'"),

            'description': _("A concise summary of the problem. Focus on what happened, when it happened, and the context."),

            'application_version': _("The version of Greenova where the bug was encountered. Check the footer of any Greenova page or look at the 'About' section in settings."),

            'operating_system': _("Your operating system and version (e.g., Windows 10, macOS 11.2, Ubuntu 20.04)."),

            'browser': _("Browser name and version (e.g., Chrome 89.0, Firefox 86.0). Leave blank if not applicable."),

            'device_type': _("Type of device (e.g., desktop, laptop, smartphone). Include device model if on mobile."),

            'steps_to_reproduce': _("Detailed numbered steps to reproduce the issue. Start from a known state and be specific about what you clicked, typed, or selected."),

            'expected_behavior': _("What you expected to happen when following the steps above."),

            'actual_behavior': _("What actually happened instead. Be specific about error messages, unexpected behavior, or missing functionality."),

            'error_messages': _("Copy and paste the exact error text rather than paraphrasing. Include any error codes or numbers."),

            'trace_report': _("If available, include the Django traceback or browser console logs. For Django errors: look for the section labeled 'Traceback', click on 'Switch to copy-and-paste view', and copy the entire trace report."),

            'frequency': _("How often the issue occurs. Select the option that best matches your experience."),

            'impact_severity': _("How severe the issue is: Minor (causes inconvenience), Major (prevents completing specific tasks), Critical (prevents core functionality, data loss, security risks)."),

            'user_impact': _("How the issue affects user experience. Mention any deadlines or business processes affected."),

            'workarounds': _("Any temporary solutions you've found to work around the issue."),

            'additional_comments': _("Any other relevant information, patterns you've noticed, or when the issue started occurring."),
        }

        # Apply help text and required status to fields
        for field_name, field in self.fields.items():
            if field_name in field_help:
                field.help_text = field_help[field_name]

            if field_name in required_fields:
                field.required = True
                field.label = f"{field.label}*"  # Add asterisk to required field labels
                # Add the mandatory message to error messages
                field.error_messages['required'] = mark_safe(mandatory_message)
