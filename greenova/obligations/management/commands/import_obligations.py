from typing import Any, Dict, Tuple, Optional, TypedDict, Union, Set, cast
from django.core.management.base import BaseCommand, CommandParser
from django.utils.dateparse import parse_date
from django.db import transaction
from django.db.models.signals import post_save
from django.utils import timezone
import csv
import re
import logging
from projects.models import Project
from obligations.models import Obligation
from mechanisms.models import EnvironmentalMechanism

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
        parser.add_argument(
            '--no-transaction',
            action='store_true',
            help='Process each row without wrapping in a transaction (use for database issues)'
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
            # Added support for 'Y' and 'N' values (case-sensitive)
            if value.strip() == 'Y':
                return True
            elif value.strip() == 'N':
                return False

            # Handle other string variations
            return value.lower().strip() in ('yes', 'true', '1', 'y', 'yes ', 'y ')

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
                mechanism = EnvironmentalMechanism.objects.create(
                    name=mech_name,
                    project=project,
                    primary_environmental_mechanism=mechanism_name
                )
                # Use getattr for safer access
                mech_name = getattr(mechanism, 'name', mech_name)
                proj_name = getattr(project, 'name', 'Unknown')
                logger.info(f"Created new mechanism: {mech_name} for project {proj_name}")
                return mechanism, True

        except Exception as e:
            logger.error(f"Error creating mechanism {mechanism_name}: {str(e)}")
            return None, False

    def process_row(self, row: Dict[str, Any], project: Project) -> ObligationData:
        """
        Process and clean a CSV row.

        Args:
            row: Dictionary containing CSV row data
            project: Project instance

        Returns:
            Processed data dictionary with cleaned values
        """
        # Get mechanism name, handling possible None value
        mechanism_name = row.get('primary__environmental__mechanism')
        mechanism, created = self.get_or_create_mechanism(mechanism_name, project)

        # Use getattr for safer access - handles type checking issues
        if created and mechanism is not None:
            mech_name = getattr(mechanism, 'name', 'Unknown')
            proj_name = getattr(project, 'name', 'Unknown')
            logger.info(f"Created new mechanism: {mech_name} for project {proj_name}")

        # Normalize status
        status = row.get('status', '').lower()
        if status not in ('not started', 'in progress', 'completed'):
            status = 'not started'

        # Process environmental aspect with improved mapping
        environmental_aspect = row.get('environmental__aspect') or ''

        # Define mapping for commonly observed aspects and clean up format
        aspect_mapping: Dict[str, str] = {
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
            environmental_aspect = environmental_aspect.strip()
        else:
            environmental_aspect = 'Other'

        # Process dates safely
        action_due_date = None
        if row.get('action__due_date'):
            try:
                action_due_date = parse_date(str(row.get('action__due_date')))
            except (ValueError, TypeError):
                logger.warning(f"Invalid action due date: {row.get('action__due_date')}")

        close_out_date = None
        if row.get('close__out__date'):
            try:
                close_out_date = parse_date(str(row.get('close__out__date')))
            except (ValueError, TypeError):
                logger.warning(f"Invalid close out date: {row.get('close__out__date')}")

        recurring_date = None
        if row.get('recurring__forcasted__date'):
            try:
                recurring_date = parse_date(str(row.get('recurring__forcasted__date')))
            except (ValueError, TypeError):
                logger.warning(f"Invalid recurring date: {row.get('recurring__forcasted__date')}")

        # Make sure we have a valid obligation number
        obligation_number = row.get('obligation__number')
        if not obligation_number:
            obligation_number = f"UNKNOWN-{timezone.now().timestamp()}"
            logger.warning(f"Missing obligation number, using generated number: {obligation_number}")

        # Normalize the obligation number
        normalized_obligation_number = self.normalize_obligation_number(obligation_number)

        # Explicitly convert gap_analysis to boolean - THIS IS THE KEY FIX
        gap_analysis_value = self.clean_boolean(row.get('gap__analysis'))

        # Prepare cleaned data
        result: ObligationData = {
            'obligation_number': normalized_obligation_number,
            'project': project,
            'primary_environmental_mechanism': mechanism,
            'procedure': row.get('procedure', ''),
            'environmental_aspect': environmental_aspect,
            'obligation': row.get('obligation', ''),
            'accountability': row.get('accountability', ''),
            'responsibility': row.get('responsibility', ''),
            'project_phase': row.get('project_phase', ''),
            'action_due_date': action_due_date,
            'close_out_date': close_out_date,
            'status': status,
            'supporting_information': row.get('supporting__information', ''),
            'general_comments': row.get('general__comments', ''),
            'compliance_comments': row.get('compliance__comments', ''),
            'non_conformance_comments': row.get('non_conformance__comments', ''),
            'evidence_notes': row.get('evidence', ''),
            'recurring_obligation': self.clean_boolean(row.get('recurring__obligation')),
            'recurring_frequency': row.get('recurring__frequency', ''),
            'recurring_status': row.get('recurring__status', ''),
            'recurring_forcasted_date': recurring_date,
            'inspection': self.clean_boolean(row.get('inspection')),
            'inspection_frequency': row.get('inspection__frequency', ''),
            'site_or_desktop': row.get('site_or__desktop', ''),
            'gap_analysis': gap_analysis_value,
            'notes_for_gap_analysis': row.get('notes_for__gap__analysis', ''),
        }
        return result

    def create_or_update_obligation(self, obligation_data: ObligationData, force_update: bool = False) -> Tuple[Union[Obligation, bool, None], str]:
        """
        Create or update an obligation record.

        Args:
            obligation_data: Dictionary containing obligation data
            force_update: Whether to force update existing records

        Returns:
            Tuple containing (result, status) where result is the created/updated
            obligation or False if skipped, and status is a string indicating
            the action taken
        """
        obligation_number = obligation_data.get('obligation_number', '')

        try:
            # Check if obligation already exists
            existing = Obligation.objects.filter(obligation_number=obligation_number).first()

            if existing and not force_update:
                # Skip if already exists and not forcing update
                return False, "skipped"

            if existing:
                # Update existing obligation
                for key, value in obligation_data.items():
                    if key != 'obligation_number':  # Don't update the primary key
                        setattr(existing, key, value)
                existing.save()
                return existing, "updated"
            else:
                # Create new obligation
                new_obligation = Obligation(**obligation_data)
                new_obligation.save()
                return new_obligation, "created"

        except Exception as e:
            logger.error(f"Error creating/updating obligation {obligation_number}: {str(e)}")
            return None, f"error: {str(e)}"

    def process_single_row(self, row: Dict[str, Any], options: Dict[str, Any]) -> Tuple[str, int]:
        """
        Process a single row without transaction wrapper.

        Args:
            row: Dictionary containing CSV row data
            options: Command line options dictionary

        Returns:
            Tuple of (status, count_to_increment) where status is one of
            "created", "updated", "skipped", "error" and count_to_increment
            is 1 if the operation was successful
        """
        force_update = options.get('force_update', False)
        dry_run = options.get('dry_run', False)

        try:
            # Get or create project
            project_name = row.get('project__name')
            if not project_name:
                logger.error("Missing project name in row")
                return "error", 1

            # Handle database connection for projects
            try:
                project = Project.objects.get(name=project_name)
            except Project.DoesNotExist:
                try:
                    # Try to create project
                    project = Project.objects.create(name=project_name)
                except Exception as e:
                    logger.error(f"Error creating project: {str(e)}")
                    return "error", 1
            except Exception as e:
                logger.error(f"Error getting project: {str(e)}")
                return "error", 1

            # Process row data
            processed_data = self.process_row(row, project)

            if not dry_run:
                # Create or update obligation
                _, status = self.create_or_update_obligation(
                    processed_data, force_update=force_update
                )

                if status.startswith("error"):
                    return "error", 1
                return status, 1
            else:
                # In dry run mode, just check if it would be created/updated
                obligation_number = processed_data.get('obligation_number', '')
                if Obligation.objects.filter(obligation_number=obligation_number).exists():
                    if force_update:
                        return "updated", 1
                    else:
                        return "skipped", 1
                else:
                    return "created", 1

        except Exception as e:
            logger.error(f"Error processing row: {str(e)}")
            return "error", 1

    def handle(self, *_: Any, **options: Any) -> None:
        """
        Execute the command to import obligations from CSV.

        Args:
            _: Command line arguments (not used)
            options: Command line options dictionary
        """
        csv_file = options['csv_file']
        dry_run = options.get('dry_run', False)
        skip_counts_update = options.get('skip_counts_update', False)
        no_transaction = options.get('no_transaction', False)

        # Check for required database tables
        required_tables = {
            "company_company": "Company model",
            "projects_project": "Project model",
            "mechanisms_environmentalmechanism": "EnvironmentalMechanism model"
        }

        missing_tables = []

        # Check database tables exist
        for table, model_name in required_tables.items():
            try:
                # Try a simple query to check table existence
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT 1 FROM {table} LIMIT 1")
            except Exception as e:
                if "no such table" in str(e):
                    missing_tables.append((table, model_name))

        # If any required tables are missing, show migration instructions
        if missing_tables:
            self.stdout.write(self.style.WARNING("\nDatabase tables not ready for import:\n"))
            for table, model_name in missing_tables:
                self.stdout.write(self.style.ERROR(f"  - Missing {table} ({model_name})"))

            self.stdout.write(self.style.WARNING("\nPlease run migrations first:"))
            self.stdout.write(self.style.NOTICE("  python manage.py migrate\n"))
            self.stdout.write(self.style.WARNING("Then try importing again.\n"))
            return  # Exit the command

        # Continue with import if all tables exist
        self.stdout.write(f"Importing obligations from {csv_file}")

        # Disconnect signals if needed
        if skip_counts_update:
            self.stdout.write("Disconnecting post_save signal to skip mechanism counts update")
            try:
                post_save.disconnect(sender=Obligation, dispatch_uid="update_mechanism_counts")
            except Exception as e:
                logger.warning(f"Could not disconnect signal: {str(e)}")

        # Process the CSV file
        try:
            # Rest of your import logic
            # ...

            self.stdout.write(self.style.SUCCESS("Import completed successfully"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Import failed: {str(e)}"))
            logger.error(f"Import error: {str(e)}")
