# pylint: disable=import-error
import pytest
from django.urls import reverse
from feedback.forms import BugReportForm
from feedback.models import BugReport


@pytest.mark.django_db
class TestBugReportModel:
    """Test the BugReport model."""

    def test_create_bug_report(self, regular_user):
        """Test creating a bug report."""
        bug_report = BugReport.objects.create(
            title='Test Bug',
            description='This is a test bug report.',
            created_by=regular_user,
            severity='medium',
            status='open'
        )
        # Use proper pytest assertions
        assert bug_report.title == 'Test Bug'
        assert bug_report.created_by == regular_user
        assert bug_report.severity == 'medium'
        assert bug_report.status == 'open'

    def test_bug_report_str(self, regular_user):
        """Test the string representation of a bug report."""
        bug_report = BugReport.objects.create(
            title='Test Bug',
            description='This is a test bug report.',
            created_by=regular_user
        )
        assert str(bug_report) == 'Test Bug'


@pytest.mark.django_db
class TestBugReportForm:
    """Test the BugReportForm."""

    def test_valid_form(self):
        """Test form with valid data."""
        form = BugReportForm(data={
            # Summary section
            'title': 'Test Bug',
            'description': 'This is a test bug report.',

            # Environment section
            'application_version': '1.2.3',
            'operating_system': 'Ubuntu 20.04',
            'browser': 'Chrome 98.0.4758.102',
            'device_type': 'Desktop',

            # Steps section
            'steps_to_reproduce': 'Step 1: Do this\nStep 2: Do that',
            'expected_behavior': 'It should work',
            'actual_behavior': 'It does not work',

            # Technical details (optional)
            'error_messages': 'Error: Something went wrong',
            'trace_report': 'Traceback: file.py, line 42',

            # Frequency and impact
            'frequency': 'frequently',
            'impact_severity': 'major',
            'user_impact': 'Users cannot complete their environmental reports',

            # Additional info (optional)
            'workarounds': 'Refresh the page',
            'additional_comments': 'This happens after system updates'
        })
        assert form.is_valid(), f'Form errors: {form.errors}'

    def test_invalid_form(self):
        """Test form with invalid data."""
        # Missing title which is required
        form = BugReportForm(data={
            'description': 'This is a test bug report.',
        })
        assert not form.is_valid()
        assert 'title' in form.errors


@pytest.mark.django_db
class TestFeedbackViews:
    """Test feedback views."""

    def test_index_view(self, client, admin_user):
        """Test the index view."""
        client.force_login(admin_user)
        response = client.get(reverse('feedback:index'))
        assert response.status_code == 200
        assert 'form' in response.context
        assert 'bug_reports' in response.context

    def test_submit_bug_report(self, client, admin_user):
        """Test submitting a bug report."""
        client.force_login(admin_user)
        response = client.post(
            reverse('feedback:submit_bug_report'),
            {
                'title': 'New Bug',
                'description': 'This is a new bug report.',
                'steps_to_reproduce': 'Step 1: Do this\nStep 2: Do that',
                'expected_behavior': 'It should work',
                'actual_behavior': 'It does not work',
                'environment': 'Chrome 98.0.4758.102'
            },
            follow=True
        )
        assert response.status_code == 200

        # Check that the bug report was created
        assert BugReport.objects.filter(title='New Bug').exists()

        # Check that success message is displayed
        messages = list(response.context['messages'])
        assert len(messages) > 0
        assert 'submitted successfully' in str(messages[0])

    def test_submit_invalid_bug_report(self, client, admin_user):
        """Test submitting an invalid bug report."""
        client.force_login(admin_user)
        response = client.post(
            reverse('feedback:submit_bug_report'),
            {
                # Missing required title
                'description': 'This is a new bug report.',
            }
        )
        assert response.status_code == 200

        # Check that form errors are displayed
        assert 'form' in response.context
        assert response.context['form'].errors

        # Check that error message is displayed
        messages = list(response.context['messages'])
        assert len(messages) > 0
        assert 'problem with your submission' in str(messages[0])

    def test_login_required(self, client):
        """Test that views require login."""
        # Test index view
        response = client.get(reverse('feedback:index'))
        assert response.status_code == 302  # Redirect to login
        assert '/authentication/login/' in response.url

        # Test submit view
        response = client.post(reverse('feedback:submit_bug_report'), {'title': 'Test'})
        assert response.status_code == 302  # Redirect to login
        assert '/authentication/login/' in response.url
