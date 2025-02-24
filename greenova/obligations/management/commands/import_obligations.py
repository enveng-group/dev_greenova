import csv
import logging
from typing import Any, Dict
from django.core.management.base import BaseCommand, CommandParser
from django.utils.dateparse import parse_date
from django.db import transaction
from projects.models import Project
from obligations.models import Obligation

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Import obligations from CSV file'

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

    def process_row(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """Process and clean a CSV row."""
        return {
            'obligation_number': row['obligation__number'],
            'primary_environmental_mechanism': row['primary__environmental__mechanism'] or '',
            'procedure': row['procedure'] or '',
            'environmental_aspect': row['environmental__aspect'] or '',
            'obligation': row['obligation'] or '',
            'accountability': row['accountability'] or '',
            'responsibility': row['responsibility'] or '',
            'project_phase': row['project_phase'] or '',
            'action_due_date': parse_date(
                row['action__due_date']) if row['action__due_date'] else None,
            'close_out_date': parse_date(
                row['close__out__date']) if row['close__out__date'] else None,
            'status': row['status'] or 'not started',
            'supporting_information': row['supporting__information'] or '',
            'general_comments': row['general__comments'] or '',
            'compliance_comments': row['compliance__comments'] or '',
            'non_conformance_comments': row['non_conformance__comments'] or '',
            'evidence': row['evidence'] or '',
            'person_email': row['person_email'] or '',
            'recurring_obligation': self.clean_boolean(
                row['recurring__obligation']),
            'recurring_frequency': row['recurring__frequency'] or '',
            'recurring_status': row['recurring__status'] or '',
            'recurring_forcasted_date': parse_date(
                    row['recurring__forcasted__date']) if row['recurring__forcasted__date'] else None,
            'inspection': self.clean_boolean(
                        row['inspection']),
            'inspection_frequency': row['inspection__frequency'] or '',
            'site_or_desktop': row['site_or__desktop'] or '',
            'new_control_action_required': self.clean_boolean(
                row.get(
                    'new__control__action_required',
                    'False')),
            'obligation_type': row['obligation_type'] or '',
            'gap_analysis': row['gap__analysis'] or '',
            'notes_for_gap_analysis': row['notes_for__gap__analysis'] or '',
            'covered_in_which_inspection_checklist': row['covered_in_which_inspection_checklist'] or ''}

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
                        obligation_data = self.process_row(row)
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
                    f"Error importing obligations: {
                        str(e)}"))
