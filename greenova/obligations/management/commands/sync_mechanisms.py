from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count, Q
from django.utils import timezone
from obligations.models import Obligation
from mechanisms.models import EnvironmentalMechanism
from projects.models import Project
from typing import Any
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Sync environmental mechanisms from obligations and update all counts including overdue status'

    def update_null_statuses(self):
        """Update NULL statuses to 'not started'."""
        updated = Obligation.objects.filter(
            Q(status__isnull=True) | Q(status='NULL')
        ).update(status='not started')

        if updated:
            logger.info(f"Updated {updated} obligations with NULL status to 'not started'")
        return updated

    def validate_obligations(self):
        """Validate obligation status values and fix NULL statuses."""
        # First update any NULL values
        self.update_null_statuses()

        # Then check for any remaining invalid statuses
        invalid_status = Obligation.objects.exclude(
            status__in=['not started', 'in progress', 'completed']
        ).values('obligation_number', 'status')

        if invalid_status.exists():
            for obj in invalid_status:
                # Update NULL statuses to 'not started'
                if obj['status'] in (None, 'NULL'):
                    Obligation.objects.filter(
                        obligation_number=obj['obligation_number']
                    ).update(status='not started')
                    logger.info(
                        f"Fixed NULL status to 'not started' for obligation {obj['obligation_number']}"
                    )
                else:
                    logger.error(
                        f"Invalid status '{obj['status']}' for obligation {obj['obligation_number']}"
                    )
            # Return True since we've fixed the NULL values
            return True
        return True

    def update_mechanism_counts(self):
        """Update all mechanism counts including overdue status."""
        mechanisms = EnvironmentalMechanism.objects.all().select_related('project')
        count = mechanisms.count()

        self.stdout.write(f"Updating counts for {count} mechanisms...")

        mechanisms_updated = 0
        for i, mechanism in enumerate(mechanisms, 1):
            if i % 10 == 0 or i == count:
                self.stdout.write(f"Processed {i}/{count} mechanisms")

            try:
                mechanism.update_obligation_counts()
                mechanisms_updated += 1
            except Exception as e:
                logger.error(f"Error updating counts for {mechanism.name}: {str(e)}")

        return mechanisms_updated

    def handle(self, *args: tuple[Any, ...], **options: dict[str, Any]) -> None:
        try:
            with transaction.atomic():
                # Validate existing obligations first
                if not self.validate_obligations():
                    raise ValueError("Invalid obligation statuses found")

                # Create/update mechanisms based on obligations
                mechanisms_data = (
                    Obligation.objects
                    .filter(primary_environmental_mechanism__isnull=False)
                    .values(
                        'project',
                        'primary_environmental_mechanism__name'
                    )
                    .annotate(
                        not_started_count=Count(
                            'obligation_number',
                            filter=Q(status='not started')
                        ),
                        in_progress_count=Count(
                            'obligation_number',
                            filter=Q(status='in progress')
                        ),
                        completed_count=Count(
                            'obligation_number',
                            filter=Q(status='completed')
                        )
                    )
                )

                # Now update all mechanism counts including overdue status
                mechanisms_updated = self.update_mechanism_counts()

                self.stdout.write(
                    self.style.SUCCESS(f"Synchronized mechanisms: {mechanisms_updated} updated")
                )

        except Exception as e:
            logger.error(f"Error syncing mechanisms: {str(e)}")
            self.stdout.write(
                self.style.ERROR(f"Error syncing mechanisms: {str(e)}")
            )
            raise
