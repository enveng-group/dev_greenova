from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count, Q
from obligations.models import Obligation
from mechanisms.models import EnvironmentalMechanism
from projects.models import Project
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Sync environmental mechanisms from obligations'

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

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                if not self.validate_obligations():
                    raise ValueError("Invalid obligation statuses found")

                mechanisms_data = (
                    Obligation.objects
                    .filter(primary_environmental_mechanism__isnull=False)
                    .values(
                        'project',
                        'primary_environmental_mechanism__name'  # Changed to get name
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

                mechanisms_processed = 0

                for data in mechanisms_data:
                    try:
                        project = Project.objects.get(id=data['project'])
                        mech_name = data['primary_environmental_mechanism__name']

                        if not mech_name:
                            continue

                        # Calculate counts
                        counts = {
                            'not_started': data['not_started_count'],
                            'in_progress': data['in_progress_count'],
                            'completed': data['completed_count']
                        }

                        # Determine status
                        total = sum(counts.values())
                        if total == 0:
                            status = 'not started'
                        elif counts['completed'] == total:
                            status = 'completed'
                        elif counts['in_progress'] > 0:
                            status = 'in progress'
                        else:
                            status = 'not started'

                        # Update or create mechanism
                        mechanism, created = EnvironmentalMechanism.objects.update_or_create(
                            name=mech_name,
                            project=project,
                            defaults={
                                'not_started_count': counts['not_started'],
                                'in_progress_count': counts['in_progress'],
                                'completed_count': counts['completed'],
                                'status': status,
                                'description': f'Environmental mechanism for {project.name}'
                            }
                        )

                        mechanisms_processed += 1
                        logger.info(
                            f"{'Created' if created else 'Updated'} mechanism "
                            f"{mech_name} for {project.name}"
                        )

                    except Project.DoesNotExist:
                        logger.error(f"Project {data['project']} not found")
                        continue
                    except Exception as e:
                        logger.error(
                            f"Error processing mechanism {mech_name}: {str(e)}"
                        )
                        continue

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully synced {mechanisms_processed} mechanisms'
                    )
                )

        except Exception as e:
            logger.error(f"Error syncing mechanisms: {str(e)}")
            self.stdout.write(
                self.style.ERROR(f"Error syncing mechanisms: {str(e)}")
            )
            raise
