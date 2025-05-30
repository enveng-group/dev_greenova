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

"""Forms for submitting and validating bug reports in the feedback app."""


from django import forms
from typing import ClassVar
from django.template.loader import render_to_string
from .models import BugReport
from django.utils.html import escape


class BugReportForm(forms.ModelForm):
    """Form for submitting detailed bug reports."""

    class Meta:
        """Meta options for BugReportForm."""

        model = BugReport
        fields: ClassVar[list[str]] = [
            "title",
            "description",
            "application_version",
            "operating_system",
            "browser",
            "device_type",
            "steps_to_reproduce",
            "expected_behavior",
            "actual_behavior",
            "error_messages",
            "trace_report",
            "frequency",
            "impact_severity",
            "user_impact",
            "workarounds",
            "additional_comments",
        ]

    widgets: ClassVar[dict[str, forms.Widget]] = {
        "title": forms.TextInput(attrs={"size": "80"}),
        "description": forms.Textarea(attrs={"rows": 5, "cols": 80}),
        "application_version": forms.TextInput(attrs={"size": "20"}),
        "operating_system": forms.TextInput(attrs={"size": "50"}),
        "browser": forms.TextInput(attrs={"size": "50"}),
        "device_type": forms.TextInput(attrs={"size": "50"}),
        "steps_to_reproduce": forms.Textarea(attrs={"rows": 8, "cols": 80}),
        "expected_behavior": forms.Textarea(attrs={"rows": 3, "cols": 80}),
        "actual_behavior": forms.Textarea(attrs={"rows": 3, "cols": 80}),
        "error_messages": forms.Textarea(attrs={"rows": 5, "cols": 80}),
        "trace_report": forms.Textarea(attrs={"rows": 10, "cols": 80}),
        "frequency": forms.Select(),
        "impact_severity": forms.Select(),
        "user_impact": forms.Textarea(attrs={"rows": 3, "cols": 80}),
        "workarounds": forms.Textarea(attrs={"rows": 3, "cols": 80}),
        "additional_comments": forms.Textarea(attrs={"rows": 3, "cols": 80}),
    }

    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        """Initialize BugReportForm and set required fields and help text."""
        super().__init__(*args, **kwargs)

        # Mark most fields as required
        required_fields = [
            "title",
            "description",
            "application_version",
            "operating_system",
            "device_type",
            "steps_to_reproduce",
            "expected_behavior",
            "actual_behavior",
            "frequency",
            "impact_severity",
            "user_impact",
        ]

        # Load the mandatory field message
        mandatory_message = escape(
            render_to_string("feedback/form/messages/mandatory_item.txt"),
        )

        # Define field help text
        field_help = {
            "title": (
                "A brief, descriptive title of the issue. Example: 'Dashboard "
                "fails to load environmental metrics when filtering by project'"
            ),
            "description": (
                "A concise summary of the problem. Focus on what happened, "
                "when it happened, and the context."
            ),
            "application_version": (
                "The version of Greenova where the bug was encountered. Check "
                "the footer of any Greenova page or look at the 'About' section "
                "in settings."
            ),
            "operating_system": (
                "Your operating system and version (e.g., Windows 10, macOS 11.2, "
                "Ubuntu 20.04)."
            ),
            "browser": (
                "Browser name and version (e.g., Chrome 89.0, Firefox 86.0). "
                "Leave blank if not applicable."
            ),
            "device_type": (
                "Type of device (e.g., desktop, laptop, smartphone). Include "
                "device model if on mobile."
            ),
            "steps_to_reproduce": (
                "Detailed numbered steps to reproduce the issue. Start from a "
                "known state and be specific about what you clicked, typed, or "
                "selected."
            ),
            "expected_behavior": (
                "What you expected to happen when following the steps above."
            ),
            "actual_behavior": (
                "What actually happened instead. Be specific about error messages, "
                "unexpected behavior, or missing functionality."
            ),
            "error_messages": (
                "Copy and paste the exact error text rather than paraphrasing. "
                "Include any error codes or numbers."
            ),
            "trace_report": (
                "If available, include the Django traceback or browser console logs. "
                "For Django errors: look for the section labeled 'Traceback', click "
                "on 'Switch to copy-and-paste view', and copy the entire trace report."
            ),
            "frequency": (
                "How often the issue occurs. Select the option that best matches "
                "your experience."
            ),
            "impact_severity": (
                "How severe the issue is: Minor (causes inconvenience), Major "
                "(prevents completing specific tasks), Critical (prevents core "
                "functionality, data loss, security risks)."
            ),
            "user_impact": (
                "How the issue affects user experience. Mention any deadlines or "
                "business processes affected."
            ),
            "workarounds": (
                "Any temporary solutions you've found to work around the issue."
            ),
            "additional_comments": (
                "Any other relevant information, patterns you've noticed, or when "
                "the issue started occurring."
            ),
        }

        # Apply help text and required status to fields
        for field_name, field in self.fields.items():
            if field_name in field_help:
                field.help_text = field_help[field_name]

            if field_name in required_fields:
                field.required = True
                field.label = f"{field.label}*"  # Add asterisk to required field labels
                # Add the mandatory message to error messages
                field.error_messages["required"] = escape(mandatory_message)
