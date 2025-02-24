import csv
import logging
from typing import Any, Dict, Tuple, Optional
from django.core.management.base import BaseCommand, CommandParser
from django.utils.dateparse import parse_date
from django.db import transaction
from projects.models import Project
from obligations.models import Obligation
from mechanisms.models import EnvironmentalMechanism

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Import obligations from CSV file'

    # Mechanism mapping moved directly into the command
    MECHANISM_ID_MAPPING = {
        'Environmental Protection Act 1986': 'EP_ACT_1986',
        'Environmental Protection Regulations 1987': 'EP_REGS_1987',
        # Add other mappings as needed
    }

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run import without saving to database'
        )

    def clean_boolean(self, value: str) -> bool:
        """Convert string boolean values to Python boolean."""
        return value.lower() in ('yes', 'true', '1')

    def get_or_create_mechanism(self, mechanism_name: str, project: Project) -> Tuple[Optional[EnvironmentalMechanism], bool]:
        """Get or create an EnvironmentalMechanism instance."""
        if not mechanism_name:
            return None, False

        try:
            # Check if this mechanism should use a specific ID
            desired_id = self.MECHANISM_ID_MAPPING.get(mechanism_name)

            # Determine the name to use (either mapped ID or original name)
            mech_name = desired_id if desired_id else mechanism_name

            # Try to get existing mechanism
            try:
                mechanism = EnvironmentalMechanism.objects.get(
                    name=mech_name,
                    project=project
                )
                return mechanism, False
            except EnvironmentalMechanism.DoesNotExist:
                # Create new mechanism
                mechanism = EnvironmentalMechanism.objects.create(
                    name=mech_name,
                    project=project,
                    description=f'Auto-created from obligation import for {project.name}'
                )
                # Ensure chart config exists
                mechanism.save()  # This triggers the save() method that creates chart config
                return mechanism, True

        except Exception as e:
            logger.error(
                f"Error creating mechanism {mechanism_name} for project {project.name}: {str(e)}"
            )
            return None, False

    def process_row(self, row: Dict[str, Any], project: Project) -> Dict[str, Any]:
        """Process and clean a CSV row."""
        mechanism_name = row['primary__environmental__mechanism']
        mechanism, created = self.get_or_create_mechanism(mechanism_name, project)

        if created:
            logger.info(f"Created new mechanism: {mechanism_name}")

        return {
            'obligation_number': row['obligation__number'],
            'primary_environmental_mechanism': mechanism,
            'procedure': row['procedure'] or '',
            'environmental_aspect': row['environmental__aspect'] or '',
            'obligation': row['obligation'] or '',
            'accountability': row['accountability'] or '',
            'responsibility': row['responsibility'] or '',
            'project_phase': row['project_phase'] or '',
            'action_due_date': parse_date(row['action__due_date']) if row['action__due_date'] else None,
            'close_out_date': parse_date(row['close__out__date']) if row['close__out__date'] else None,
            'status': row['status'] or 'not started',
            'supporting_information': row['supporting__information'] or '',
            'general_comments': row['general__comments'] or '',
            'compliance_comments': row['compliance__comments'] or '',
            'non_conformance_comments': row['non_conformance__comments'] or '',
            'evidence': row['evidence'] or '',
            'person_email': row['person_email'] or '',
            'recurring_obligation': self.clean_boolean(row['recurring__obligation']),
            'recurring_frequency': row['recurring__frequency'] or '',
            'recurring_status': row['recurring__status'] or '',
            'recurring_forcasted_date': parse_date(row['recurring__forcasted__date']) if row['recurring__forcasted__date'] else None,
            'inspection': self.clean_boolean(row['inspection']),
            'inspection_frequency': row['inspection__frequency'] or '',
            'site_or_desktop': row['site_or__desktop'] or '',
            'new_control_action_required': self.clean_boolean(row.get('new__control__action_required', 'False')),
            'obligation_type': row['obligation_type'] or '',
            'gap_analysis': row['gap__analysis'] or '',
            'notes_for_gap_analysis': row['notes_for__gap__analysis'] or '',
            'covered_in_which_inspection_checklist': row['covered_in_which_inspection_checklist'] or ''
        }

    def handle(self, *args: Any, **options: Any) -> None:
        csv_file = options['csv_file']
        dry_run = options['dry_run']

        logger.info(f"Starting import from {csv_file}")
        self.stdout.write(f"Importing obligations from {csv_file}")

        try:
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)

                with transaction.atomic():
                    for row in reader:
                        # Get or create project
                        project_name = row['project__name']
                        project, created = Project.objects.get_or_create(
                            name=project_name,
                            defaults={'description': f'Imported project {project_name}'}
                        )

                        if created:
                            logger.info(f"Created new project: {project_name}")

                        # Process obligation data
                        obligation_data = self.process_row(row, project)
                        obligation_data['project'] = project

                        if not dry_run:
                            # Create or update obligation
                            obligation, created = Obligation.objects.update_or_create(
                                obligation_number=obligation_data['obligation_number'],
                                defaults=obligation_data
                            )

                            action = "Created" if created else "Updated"
                            logger.info(
                                f"{action} obligation {obligation.obligation_number} "
                                f"for project {project_name}"
                            )

                    if dry_run:
                        self.stdout.write(
                            self.style.SUCCESS("Dry run completed successfully"))
                        raise transaction.TransactionManagementError(
                            "Dry run completed")

                self.stdout.write(self.style.SUCCESS("Import completed successfully"))

        except FileNotFoundError:
            logger.error(f"File not found: {csv_file}")
            self.stdout.write(self.style.ERROR(f"File not found: {csv_file}"))
        except transaction.TransactionManagementError as e:
            if str(e) == "Dry run completed":
                pass
            else:
                logger.error(f"Transaction error: {str(e)}")
                self.stdout.write(self.style.ERROR(f"Transaction error: {str(e)}"))
        except Exception as e:
            logger.error(f"Error importing obligations: {str(e)}")
            self.stdout.write(
                self.style.ERROR(
                    f"Error importing obligations: {str(e)}"))
