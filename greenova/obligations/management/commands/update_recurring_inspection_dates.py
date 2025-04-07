import logging

from django.core.management.base import BaseCommand
from obligations.models import Obligation

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Update all recurring forecasted dates'

    def handle(self, *args, **options):
        """Update forecasted dates for all recurring obligations."""
        self.stdout.write("Updating recurring forecasted dates...")

        # Get all recurring obligations
        obligations = Obligation.objects.filter(recurring_obligation=True)
        count = 0

        for obligation in obligations:
            if obligation.update_recurring_forecasted_date():
                obligation.save()
                count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Successfully updated {count} recurring forecasted dates"
        ))
