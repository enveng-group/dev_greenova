import logging

from django.core.management.base import BaseCommand
from django.db import transaction
from obligations.models import Obligation
from obligations.utils import normalize_frequency

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Normalize recurring frequency values in the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes'
        )

    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)

        self.stdout.write("Finding obligations with recurring frequencies to normalize...")

        # Get all obligations with a recurring frequency
        obligations = Obligation.objects.filter(
            recurring_obligation=True,
            recurring_frequency__isnull=False
        ).exclude(recurring_frequency='')

        count = obligations.count()
        self.stdout.write(f"Found {count} obligations with recurring frequencies")

        changes = 0
        skipped = 0

        with transaction.atomic():
            # Only actually commit if not a dry run
            if dry_run:
                self.stdout.write("DRY RUN - no changes will be saved")

            for obligation in obligations:
                original = obligation.recurring_frequency
                normalized = normalize_frequency(original)

                if original.lower() != normalized:
                    self.stdout.write(f"  • {obligation.obligation_number}: '{original}' → '{normalized}'")
                    changes += 1

                    if not dry_run:
                        obligation.recurring_frequency = normalized
                        obligation.save(update_fields=['recurring_frequency'])
                else:
                    skipped += 1

        if dry_run:
            self.stdout.write(self.style.SUCCESS(
                f"Would normalize {changes} frequencies (skipped {skipped} already normalized)"
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f"Successfully normalized {changes} frequencies (skipped {skipped} already normalized)"
            ))
