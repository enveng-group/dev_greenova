from typing import Any, Dict, Tuple, Optional
from django.core.management.base import BaseCommand, CommandParser
from django.utils.dateparse import parse_date
from django.db import transaction
from django.db.models.signals import post_save
from projects.models import Project
from obligations.models import Obligation
from mechanisms.models import EnvironmentalMechanism
import csv
import logging
import re

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Import obligations from CSV file'

    # Mechanism mapping moved directly into the command
    MECHANISM_ID_MAPPING = {
        'MS1180': 'MS1180',
        'W6946/2024/1': 'W6946/2024/1',
        'Portside CEMP': 'PORTSIDE_CEMP',
    }

    # Add mapping for obligation number prefixes
    OBLIGATION_PREFIX_MAPPING = {
        'Condition': 'MS1180-',   # Map "Condition X" to "MS1180-X"
        'Condtion': 'MS1180-',    # Handle typo in source data
        'PCEMP': 'PCEMP-',        # Keep PCEMP prefix as is
    }

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run import without saving to database'
        )
        parser.add_argument(
            '--skip-counts-update',
            action='store_true',
            help='Skip mechanism counts update (use if experiencing signal issues)'
        )
        parser.add_argument(
            '--force-update',
            action='store_true',
            help='Force update existing records even if they exist'
        )

    def clean_boolean(self, value: Any) -> bool:
        """
        Convert various input values to Python boolean.

        Args:
            value: Any value that needs to be converted to boolean

        Returns:
            bool: True if value is truthy, False otherwise
        """
        if not value:
            return False

        # Handle string values by converting to lowercase string first
        if isinstance(value, str):
            return value.lower() in ('yes', 'true', '1', 'y')

        # Handle any other type
        return bool(value)

    def normalize_obligation_number(self, obligation_number: str) -> str:
        """
        Normalize obligation numbers to ensure consistent formatting.

        Args:
            obligation_number: Original obligation number string

        Returns:
            Properly formatted obligation number
        """
        if not obligation_number:
            return ""

        # Check if the obligation matches any of our known prefixes
        for prefix_key, prefix_value in self.OBLIGATION_PREFIX_MAPPING.items():
            if obligation_number.startswith(prefix_key):
                # Extract the number part
                number_part = obligation_number.replace(prefix_key, "").strip()
                # Remove any leading/trailing spaces and replace multiple spaces with a single space
                number_part = re.sub(r'\s+', ' ', number_part).strip()
                # Remove any starting dash if present
                if number_part.startswith('-'):
                    number_part = number_part[1:].strip()
                return f"{prefix_value}{number_part}"

        # If no mapping matches, return as is but ensure PCEMP- format
        if 'PCEMP' in obligation_number and not obligation_number.startswith('PCEMP-'):
            # Extract number after PCEMP if exists
            match = re.search(r'PCEMP[-\s]*(\d+)', obligation_number)
            if match:
                return f"PCEMP-{match.group(1)}"

        return obligation_number

    def get_or_create_mechanism(self, mechanism_name: Optional[str], project: Project) -> Tuple[Optional[EnvironmentalMechanism], bool]:
        """
        Get or create an EnvironmentalMechanism instance.

        Args:
            mechanism_name: Name of the mechanism, can be None
            project: Project instance the mechanism belongs to

        Returns:
            Tuple containing (mechanism, created) where created is a boolean
            indicating if the mechanism was newly created
        """
        if not mechanism_name:
            # Using string interpolation with getattr to safely access project.name
            proj_name = getattr(project, 'name', 'Unknown')
            logger.warning(f"No mechanism name provided for project {proj_name}")
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
                # Create new mechanism with proper status
                # Using getattr to safely access project.name
                proj_name = getattr(project, 'name', 'Unknown')
                mechanism = EnvironmentalMechanism(
                    name=mech_name,
                    project=project,
                    description=f'Auto-created from obligation import for {proj_name}',
                    status='not started',
                    not_started_count=0,
                    in_progress_count=0,
                    completed_count=0,
                    overdue_count=0
                )
                mechanism.save()
                return mechanism, True

        except Exception as e:
            # Using getattr to safely access project.name
            proj_name = getattr(project, 'name', 'Unknown')
            logger.error(
                f"Error creating mechanism {mechanism_name} for project {proj_name}: {str(e)}"
            )
            return None, False

    def process_row(self, row: Dict[str, Any], project: Project) -> Dict[str, Any]:
        """Process and clean a CSV row."""
        # Get mechanism name, handling possible None value
        mechanism_name = row.get('primary__environmental__mechanism')
        mechanism, created = self.get_or_create_mechanism(mechanism_name, project)

        if created and mechanism:
            logger.info(f"Created new mechanism: {mechanism_name}")

        # Normalize status
        status = row.get('status', '').lower()
        if status not in ('not started', 'in progress', 'completed'):
            status = 'not started'

        # Process environmental aspect with improved mapping
        environmental_aspect = row.get('environmental__aspect') or ''

        # Define mapping for commonly observed aspects and clean up format
        aspect_mapping = {
            'administration': 'Administration',
            'cultural heritage management': 'Cultural Heritage Management',
            'cultural heritage management ': 'Cultural Heritage Management',
            'terrestrial fauna management': 'Terrestrial Fauna Management',
            'biosecurity and pest management': 'Biosecurity And Pest Management',
            'dust management': 'Dust Management',
            'dust management ': 'Dust Management',
            'reporting': 'Reporting',
            'reporting ': 'Reporting',
            'noise management': 'Noise Management',
            'noise management ': 'Noise Management',
            'erosion and sedimentation management': 'Erosion And Sedimentation Management',
            'hazardous substances and hydrocarbon management': 'Hazardous Substances And Hydrocarbon Management',
            'waste management': 'Waste Management',
            'artificial light management': 'Artificial Light Management',
            'audits and inspections': 'Audits And Inspections',
            'design and construction requirements': 'Design And Construction Requirements',
            'design and construction requirements ': 'Design And Construction Requirements',
            'regulatory compliance reporting': 'Regulatory Compliance Reporting',
            'regulatory compliance reporting ': 'Regulatory Compliance Reporting',
            'portside cemp': 'Administration',
            'limitations and extent of proposal ': 'Other',
        }

        # Try to map using our custom mapping
        aspect_key = environmental_aspect.lower().strip()
        if aspect_key in aspect_mapping:
            environmental_aspect = aspect_mapping[aspect_key]
        elif environmental_aspect:
            # If no direct match but not empty, log a warning and default to "Other"
            logger.warning(f"Environmental aspect '{environmental_aspect}' not recognized, defaulting to 'Other'")
            environmental_aspect = 'Other'
        else:
            environmental_aspect = 'Other'

        # Process dates safely
        action_due_date = None
        if row.get('action__due_date'):
            try:
                action_due_date = parse_date(row.get('action__due_date'))
            except Exception as e:
                logger.warning(f"Error parsing action due date for {row.get('obligation__number')}: {str(e)}")

        close_out_date = None
        if row.get('close__out__date'):
            try:
                close_out_date = parse_date(row.get('close__out__date'))
            except Exception as e:
                logger.warning(f"Error parsing close out date for {row.get('obligation__number')}: {str(e)}")

        recurring_date = None
        if row.get('recurring__forcasted__date'):
            try:
                recurring_date = parse_date(row.get('recurring__forcasted__date'))
            except Exception as e:
                logger.warning(f"Error parsing recurring forecasted date for {row.get('obligation__number')}: {str(e)}")

        # Make sure we have a valid obligation number
        obligation_number = row.get('obligation__number')
        if not obligation_number:
            logger.error("Missing obligation number in row, skipping")
            return {}

        # Normalize the obligation number
        normalized_obligation_number = self.normalize_obligation_number(obligation_number)

        return {
            'obligation_number': normalized_obligation_number,
            'project': project,
            'primary_environmental_mechanism': mechanism,
            'procedure': row.get('procedure') or '',
            'environmental_aspect': environmental_aspect,
            'obligation': row.get('obligation') or '',
            'accountability': row.get('accountability') or '',
            'responsibility': row.get('responsibility') or '',
            'project_phase': row.get('project_phase') or '',
            'action_due_date': action_due_date,
            'close_out_date': close_out_date,
            'status': status,
            'supporting_information': row.get('supporting__information') or '',
            'general_comments': row.get('general__comments') or '',
            'compliance_comments': row.get('compliance__comments') or '',
            'non_conformance_comments': row.get('non_conformance__comments') or '',
            'evidence': row.get('evidence') or '',
            'recurring_obligation': self.clean_boolean(row.get('recurring__obligation')),
            'recurring_frequency': row.get('recurring__frequency') or '',
            'recurring_status': row.get('recurring__status') or '',
            'recurring_forcasted_date': recurring_date,
            'inspection': self.clean_boolean(row.get('inspection')),
            'inspection_frequency': row.get('inspection__frequency') or '',
            'site_or_desktop': row.get('site_or__desktop') or '',
            'new_control_action_required': self.clean_boolean(row.get('new__control__action_required', 'False')),
            'obligation_type': row.get('obligation_type') or '',
            'gap_analysis': row.get('gap__analysis') or '',
            'notes_for_gap_analysis': row.get('notes_for__gap__analysis') or ''
        }

    def handle(self, *args: Any, **options: Any) -> None:
        """
        Main handler for importing obligations from a CSV file.
        """
        csv_file = options['csv_file']
        dry_run = options['dry_run']
        skip_counts_update = options['skip_counts_update']
        force_update = options['force_update']

        # Always run with skip_counts_update to avoid the signal issues
        if not skip_counts_update:
            self.stdout.write("Automatically enabling --skip-counts-update to prevent signal errors")
            skip_counts_update = True

        # Temporarily disconnect signals if requested
        if skip_counts_update:
            # Import the signal handler function directly
            from obligations.models import update_mechanism_counts_on_save

            # Disconnect the signal entirely - we'll handle updates differently
            post_save.disconnect(receiver=update_mechanism_counts_on_save, sender=Obligation)
            self.stdout.write("Disconnected post_save signal to skip mechanism counts update")

        logger.info(f"Starting import from {csv_file}")
        self.stdout.write(f"Importing obligations from {csv_file}")

        row_count = 0
        created_count = 0
        updated_count = 0
        error_count = 0
        skipped_count = 0

        try:
            # Open and read the CSV file
            with open(csv_file, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                rows = list(reader)

            total_rows = len(rows)
            self.stdout.write(f"Found {total_rows} rows to process")

            with transaction.atomic():
                # Process each row in the CSV
                for i, row in enumerate(rows, 1):
                    if i % 5 == 0 or i == total_rows:
                        self.stdout.write(f"Processing row {i}/{total_rows}...")

                    row_count += 1

                    try:
                        # Get or create project
                        project_name = row.get('project__name')
                        if not project_name:
                            logger.warning(f"Missing project name in row {i}, skipping")
                            error_count += 1
                            continue

                        project, project_created = Project.objects.get_or_create(
                            name=project_name,
                            defaults={'description': f'Imported project {project_name}'}
                        )

                        if project_created:
                            logger.info(f"Created new project: {project_name}")

                        # Process obligation data
                        obligation_data = self.process_row(row, project)
                        if not obligation_data:
                            logger.warning(f"Could not process row {i}, skipping")
                            error_count += 1
                            continue

                        if not dry_run:
                            # Create or update obligation
                            obligation_number = obligation_data.pop('obligation_number')
                            try:
                                # Check if obligation already exists
                                exists = Obligation.objects.filter(obligation_number=obligation_number).exists()

                                if exists and not force_update:
                                    # Skip if already exists and not forcing update
                                    logger.info(f"Obligation {obligation_number} already exists, skipping")
                                    skipped_count += 1
                                    continue

                                # Use update_or_create with transaction to avoid race conditions
                                obligation, created = Obligation.objects.update_or_create(
                                    obligation_number=obligation_number,
                                    defaults=obligation_data
                                )

                                if created:
                                    created_count += 1
                                    logger.info(f"Created obligation {obligation.obligation_number} for project {project_name}")
                                else:
                                    updated_count += 1
                                    logger.info(f"Updated obligation {obligation.obligation_number} for project {project_name}")

                            except Exception as e:
                                error_msg = f"Error saving obligation {obligation_number}: {str(e)}"
                                logger.error(error_msg)
                                self.stdout.write(self.style.ERROR(error_msg))
                                error_count += 1

                    except Exception as e:
                        logger.error(f"Error processing row {i}: {str(e)}")
                        self.stdout.write(
                            self.style.ERROR(f"Error processing row {i}: {str(e)}")
                        )
                        error_count += 1

                if dry_run:
                    self.stdout.write(
                        self.style.SUCCESS("Dry run completed successfully")
                    )
                    raise transaction.TransactionManagementError(
                        "Dry run completed"
                    )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Import completed: {created_count} created, {updated_count} updated, "
                        f"{skipped_count} skipped, {error_count} errors"
                    )
                )

            # Update mechanism counts if we skipped the signals
            if skip_counts_update:
                self.stdout.write("Manually updating mechanism counts...")
                mechanisms = EnvironmentalMechanism.objects.all()
                updated_count = 0
                error_count = 0
                for mechanism in mechanisms:
                    try:
                        mechanism.update_obligation_counts()
                        updated_count += 1
                    except Exception as e:
                        error_count += 1
                        logger.error(f"Error updating counts for mechanism {mechanism.name}: {str(e)}")

                self.stdout.write(f"Mechanism counts updated: {updated_count} updated, {error_count} errors")

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
                self.style.ERROR(f"Error importing obligations: {str(e)}"))
        finally:
            # We'll deliberately NOT reconnect the signal handler
            # This avoids potential issues if the signal handler
            # is connected but the parameters don't match
            logger.info("Import process completed")
            self.stdout.write("Import process completed")
