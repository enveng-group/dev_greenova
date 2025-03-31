import csv
import logging
import os
from typing import Any, Dict, List, Optional, Tuple, TypedDict, Union

from django.core.management.base import BaseCommand, CommandParser
from django.db import IntegrityError, transaction
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.dateparse import parse_date
from mechanisms.models import EnvironmentalMechanism
from obligations.models import Obligation
from obligations.utils import normalize_frequency
from projects.models import Project

logger = logging.getLogger(__name__)


# Define TypedDict for obligation data structure
class ObligationData(TypedDict, total=False):
    """Type definition for obligation data dictionary."""

    obligation_number: str
    project: Project
    primary_environmental_mechanism: Optional[EnvironmentalMechanism]
    procedure: str
    environmental_aspect: str
    obligation: str
    accountability: str
    responsibility: str
    project_phase: str
    action_due_date: Optional[Any]  # Date object
    close_out_date: Optional[Any]  # Date object
    status: str
    supporting_information: str
    general_comments: str
    compliance_comments: str
    non_conformance_comments: str
    evidence_notes: str
    recurring_obligation: bool
    recurring_frequency: str
    recurring_status: str
    recurring_forcasted_date: Optional[Any]  # Date object
    inspection: bool
    inspection_frequency: str
    site_or_desktop: str
    gap_analysis: bool
    notes_for_gap_analysis: str
    created_at: Any  # Datetime
    updated_at: Any  # Datetime


class Command(BaseCommand):
    help = 'Import obligations from CSV file'

    # Mechanism mapping moved directly into the command
    MECHANISM_ID_MAPPING: Dict[str, str] = {
        'MS1180': 'MS1180',
        'W6946/2024/1': 'W6946/2024/1',
        'Portside CEMP': 'PORTSIDE_CEMP',
    }

    # Add mapping for obligation number prefixes
    OBLIGATION_PREFIX_MAPPING: Dict[str, str] = {
        'Condition': 'MS1180-',
        'Condtion': 'MS1180-',
        'PCEMP': 'PCEMP-',
    }

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            'csv_file',
            type=str,
            help='Path to the CSV file containing obligations data',
        )
        parser.add_argument(
            '--project',
            type=str,
            help='Project name to use if not specified in the CSV',
        )
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update existing obligations instead of skipping',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be imported without actually importing',
        )
        parser.add_argument(
            '--continue-on-error',
            action='store_true',
            help='Continue processing rows even if some fail',
        )
        parser.add_argument(
            '--no-transaction',
            action='store_true',
            help='Process each row without wrapping in a transaction (use for database issues)'
        )
        parser.add_argument(
            '--no-transaction',
            action='store_true',
            help='Process each row without wrapping in a transaction (use for database issues)'
        )
        parser.add_argument(
            '--no-transaction',
            action='store_true',
            help='Process each row without wrapping in a transaction (use for database issues)'
        )

    def clean_boolean(self, value: Any) -> bool:
        """Convert various boolean representations to Python booleans."""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            value = value.lower().strip()
            return value in ('true', 'yes', 'y', '1', 'on', 't')
        return bool(value)

    def normalize_obligation_number(self, obligation_number: str) -> str:
        """Normalize obligation number format."""
        if not obligation_number:
            return ''

        obligation_number = str(obligation_number).strip()

        # Check if the obligation number starts with any of our prefixes
        for prefix, normalized_prefix in self.OBLIGATION_PREFIX_MAPPING.items():
            if obligation_number.startswith(prefix):
                # Replace the prefix with the normalized version
                return obligation_number.replace(prefix, normalized_prefix, 1)

        # If no prefix match but contains a dash, ensure proper formatting
        if '-' in obligation_number:
            prefix, number = obligation_number.split('-', 1)
            # Ensure there's no extra dash and proper spacing
            return f'{prefix.upper()}-{number.strip()}'

        return obligation_number

    def get_or_create_mechanism(
        self, mechanism_name: Optional[str], project: Project
    ) -> Tuple[Optional[EnvironmentalMechanism], bool]:
        """Get or create an environmental mechanism for the project."""
        if not mechanism_name:
            return None, False

        mechanism_name = mechanism_name.strip()
        mechanism_id = self.MECHANISM_ID_MAPPING.get(mechanism_name, mechanism_name)

        # Try to find existing mechanism
        mechanism = EnvironmentalMechanism.objects.filter(
            name=mechanism_name, project=project
        ).first()

        if mechanism:
            return mechanism, False

        # Create new mechanism if not found
        mechanism = EnvironmentalMechanism(
            name=mechanism_name, project=project, reference_number=mechanism_id
        )
        mechanism.save()
        return mechanism, True

    def process_row(self, row: Dict[str, Any], project: Project) -> ObligationData:
        """Process a single CSV row into an ObligationData dictionary."""
        # Map CSV fields to ObligationData fields
        mechanism_name = row.get('primary__environmental__mechanism', '')
        mechanism, _ = self.get_or_create_mechanism(mechanism_name, project)

        # Process dates
        action_due_date = None
        if row.get('action__due_date'):
            action_due_date = parse_date(row['action__due_date'])

        close_out_date = None
        if row.get('close__out__date'):
            close_out_date = parse_date(row['close__out__date'])

        recurring_forecasted_date = None
        if row.get('recurring__forcasted__date'):
            recurring_forecasted_date = parse_date(row['recurring__forcasted__date'])

        # Normalize obligation number
        obligation_number = self.normalize_obligation_number(
            row.get('obligation__number', '')
        )

        # Normalize recurring frequency
        recurring_frequency = ''
        if row.get('recurring__frequency'):
            recurring_frequency = normalize_frequency(row['recurring__frequency'])

        # Set timestamps for new records
        now = timezone.now()

        # Create the ObligationData dictionary
        obligation_data: ObligationData = {
            'obligation_number': obligation_number,
            'project': project,
            'primary_environmental_mechanism': mechanism,
            'procedure': row.get('procedure', ''),
            'environmental_aspect': row.get('environmental__aspect', ''),
            'obligation': row.get('obligation', ''),
            'accountability': row.get('accountability', ''),
            'responsibility': row.get('responsibility', ''),
            'project_phase': row.get('project_phase', ''),
            'action_due_date': action_due_date,
            'close_out_date': close_out_date,
            'status': row.get('status', 'not started'),
            'supporting_information': row.get('supporting__information', ''),
            'general_comments': row.get('general__comments', ''),
            'compliance_comments': row.get('compliance__comments', ''),
            'non_conformance_comments': row.get('non_conformance__comments', ''),
            'evidence_notes': row.get('evidence', ''),
            'recurring_obligation': self.clean_boolean(
                row.get('recurring__obligation', False)
            ),
            'recurring_frequency': recurring_frequency,
            'recurring_status': row.get('recurring__status', ''),
            'recurring_forcasted_date': recurring_forecasted_date,
            'inspection': self.clean_boolean(row.get('inspection', False)),
            'inspection_frequency': row.get('inspection__frequency', ''),
            'site_or_desktop': row.get('site_or__desktop', ''),
            'gap_analysis': self.clean_boolean(row.get('gap__analysis', False)),
            'notes_for_gap_analysis': row.get('notes_for__gap__analysis', ''),
            'created_at': now,
            'updated_at': now,
        }
        return result

        return obligation_data

    def create_or_update_obligation(
        self, obligation_data: ObligationData, force_update: bool = False
    ) -> Tuple[Union[Obligation, bool, None], str]:
        """Create or update an obligation from the data dictionary."""
        obligation_number = obligation_data.get('obligation_number', '')
        if not obligation_number:
            return None, 'Missing obligation number'

        # Check if obligation already exists
        existing_obligation = Obligation.objects.filter(
            obligation_number=obligation_number
        ).first()

        if existing_obligation and not force_update:
            return (
                False,
                f'Obligation {obligation_number} already exists (use --update to update)',
            )

        try:
            if existing_obligation:
                # Update existing obligation
                for key, value in obligation_data.items():
                    if (
                        key != 'obligation_number' and key != 'created_at'
                    ):  # Skip primary key and created_at
                        setattr(existing_obligation, key, value)

                # Always update the updated_at timestamp
                existing_obligation.updated_at = timezone.now()
                existing_obligation.save()
                return existing_obligation, f'Updated obligation {obligation_number}'
            else:
                # Create new obligation
                new_obligation = Obligation(**obligation_data)
                new_obligation.save()
                return new_obligation, f'Created obligation {obligation_number}'
        except Exception as e:
            return None, f'Failed to save obligation: {str(e)}'

    def process_csv_file(
        self, file_path: str, options: Dict[str, Any]
    ) -> Tuple[int, int, int, List[str]]:
        """Process the entire CSV file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'CSV file not found: {file_path}')

        # Get default project from options or create one
        default_project_name = options.get('project')
        default_project = None

        if default_project_name:
            default_project = Project.objects.filter(name=default_project_name).first()
            if not default_project:
                default_project = Project.objects.create(name=default_project_name)
                logger.info(f'Created default project: {default_project_name}')

        created = 0
        updated = 0
        skipped = 0
        errors = []

        # Open and process the CSV file
        with open(file_path, encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)

            for row_num, row in enumerate(
                reader, start=2
            ):  # Start at 2 to account for header row
                # Use transaction per row to prevent cascading failures
                try:
                    with transaction.atomic():
                        # Determine project for this row
                        project_name = row.get('project__name', '')
                        if not project_name and not default_project:
                            errors.append(
                                f'Row {row_num}: Missing project name and no default project specified'
                            )
                            skipped += 1
                            continue

                        if project_name:
                            project = Project.objects.filter(name=project_name).first()
                            if not project:
                                project = Project.objects.create(name=project_name)
                                logger.info(f'Created project: {project_name}')
                        else:
                            project = default_project

                        # Process the row into ObligationData
                        obligation_data = self.process_row(row, project)

                        # Create or update the obligation
                        if options.get('dry_run'):
                            self.stdout.write(
                                f"Would import: {obligation_data['obligation_number']} - {obligation_data['obligation'][:50]}..."
                            )
                            created += 1
                        else:
                            result, message = self.create_or_update_obligation(
                                obligation_data,
                                force_update=options.get('update', False),
                            )

                            if result is None:
                                errors.append(f'Row {row_num}: {message}')
                                skipped += 1
                            elif result is False:
                                self.stdout.write(f'Skipped: {message}')
                                skipped += 1
                            elif isinstance(result, Obligation):
                                if 'Updated' in message:
                                    updated += 1
                                else:
                                    created += 1
                                self.stdout.write(f'Success: {message}')
                except Exception as e:
                    logger.exception(f'Error processing row {row_num}: {str(e)}')
                    errors.append(f'Row {row_num}: {str(e)}')
                    skipped += 1

                    if not options.get('continue_on_error', False):
                        # Break the loop if not continuing on errors
                        errors.append(
                            'Import halted due to error. Use --continue-on-error to process all rows.'
                        )
                        break

        return created, updated, skipped, errors

    def handle(self, *args: Any, **options: Any) -> None:
        """Main command handler."""
        csv_file = options['csv_file']

        self.stdout.write(f'Importing obligations from {csv_file}')

        if options.get('dry_run'):
            self.stdout.write(
                self.style.WARNING('DRY RUN - no changes will be made to the database')
            )

        try:
            # Disconnect signals temporarily to prevent unnecessary processing
            post_save_receivers = post_save.receivers
            post_save.receivers = []

            # Process the CSV file - NOT within an atomic transaction
            created, updated, skipped, errors = self.process_csv_file(csv_file, options)

            # Report results
            if errors:
                self.stdout.write(
                    self.style.WARNING(f'Encountered {len(errors)} errors:')
                )
                for error in errors[:10]:  # Show first 10 errors
                    self.stdout.write(self.style.WARNING(f'  • {error}'))
                if len(errors) > 10:
                    self.stdout.write(
                        self.style.WARNING(f'  • ...and {len(errors) - 10} more errors')
                    )

            if options.get('dry_run'):
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Would create {created} obligations, update {updated}, skip {skipped}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created {created} obligations, updated {updated}, skipped {skipped}'
                    )
                )
        finally:
            # Reconnect signals
            post_save.receivers = post_save_receivers

            # Now trigger an update for mechanisms
            if not options.get('dry_run'):
                self.stdout.write('Updating mechanism counts...')
                try:
                    from mechanisms.models import update_all_mechanism_counts

                    count = update_all_mechanism_counts()
                    self.stdout.write(f'Updated counts for {count} mechanisms')
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Failed to update mechanism counts: {str(e)}')
                    )
                    # Don't let this error cause the whole command to fail
