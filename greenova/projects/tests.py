from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from obligations.models import Obligation
from obligations.utils import is_obligation_overdue
from projects.models import Project

class OverdueStatusTests(TestCase):
    """Test the is_obligation_overdue utility function."""

    def setUp(self):
        """Set up test data."""
        self.project = Project.objects.create(name="Test Project")
        self.today = timezone.now().date()

        # Create test obligations
        self.past_due_not_started = Obligation.objects.create(
            obligation_number="TEST-001",
            project=self.project,
            status="not started",
            action_due_date=self.today - timedelta(days=1)
        )

        self.past_due_completed = Obligation.objects.create(
            obligation_number="TEST-002",
            project=self.project,
            status="completed",
            action_due_date=self.today - timedelta(days=1)
        )

        self.future_due = Obligation.objects.create(
            obligation_number="TEST-003",
            project=self.project,
            status="not started",
            action_due_date=self.today + timedelta(days=1)
        )

        self.no_due_date = Obligation.objects.create(
            obligation_number="TEST-004",
            project=self.project,
            status="not started",
            action_due_date=None
        )

    def test_past_due_not_started_is_overdue(self):
        """Test that past due obligations that aren't completed are overdue."""
        self.assertTrue(is_obligation_overdue(self.past_due_not_started))

    def test_past_due_completed_is_not_overdue(self):
        """Test that completed obligations are never overdue."""
        self.assertFalse(is_obligation_overdue(self.past_due_completed))

    def test_future_due_is_not_overdue(self):
        """Test that future due obligations are not overdue."""
        self.assertFalse(is_obligation_overdue(self.future_due))

    def test_no_due_date_is_not_overdue(self):
        """Test that obligations without due dates are not overdue."""
        self.assertFalse(is_obligation_overdue(self.no_due_date))

    def test_dictionary_input(self):
        """Test that the function works with dictionary inputs."""
        obligation_dict = {
            'status': 'not started',
            'action_due_date': self.today - timedelta(days=1)
        }
        self.assertTrue(is_obligation_overdue(obligation_dict))

    def test_custom_reference_date(self):
        """Test using a custom reference date."""
        future_reference = self.today + timedelta(days=2)
        self.assertTrue(is_obligation_overdue(self.future_due, reference_date=future_reference))
