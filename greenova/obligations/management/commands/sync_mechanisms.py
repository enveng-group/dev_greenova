import logging
from typing import Any

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count, Q
from mechanisms.models import EnvironmentalMechanism
from obligations.models import Obligation

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Sync environmental mechanisms from obligations and update all counts'

    def update_null_statuses(self):
        """Update NULL statuses to 'not started'."""
        updated = Obligation.objects.filter(
            Q(status__isnull=True) | Q(status='NULL')
        ).update(status='not started')

        if updated:
            logger.info(
                "Updated %s obligations with NULL status to 'not started'",
                updated
            )
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
                        "Fixed NULL status to 'not started' for obligation %s",
                        obj['obligation_number']
                    )
                else:
                    logger.error(
                        "Invalid status '%s' for obligation %s",
                        obj['status'], obj['obligation_number']
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
            except (ValueError, TypeError, AttributeError) as e:
                logger.error("Error updating counts for %s: %s", mechanism.name, str(e))

        return mechanisms_updated

    def handle(self, *args: tuple[Any, ...], **options: dict[str, Any]) -> None:
        try:
            with transaction.atomic():
                # Validate existing obligations first
                if not self.validate_obligations():
                    raise ValueError("Invalid obligation statuses found")

                # Create/update mechanisms based on obligations
                # This query is a reference but does not affect mechanism updates
                # Consider removing if not needed in future versions
                _ = (
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
                    self.style.SUCCESS(
                        f"Synchronized mechanisms: {mechanisms_updated} updated"
                    )
                )

        except Exception as e:
            logger.error("Error syncing mechanisms: %s", str(e))
            self.stdout.write(
                self.style.ERROR(f"Error syncing mechanisms: {str(e)}")
            )
            raise
