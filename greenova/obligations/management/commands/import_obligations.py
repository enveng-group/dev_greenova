import csv
import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Optional, Tuple, TypedDict, Union, cast

import django
from django.core.management.base import BaseCommand, CommandParser
from django.db import DatabaseError, connection, transaction
from django.db.models import Manager  # Add this import for type hinting
from django.db.models import Model
from django.utils import timezone
from django.utils.dateparse import parse_date

from ....mechanisms.models import EnvironmentalMechanism
from ....obligations.models import Obligation
from ....obligations.utils import normalize_frequency
from ....projects.models import Project  # Ensure this is the correct import path

if not hasattr(Project, 'objects') or not isinstance(Project.objects, Manager):
    raise ImportError("The Project model is missing a valid 'objects' manager. "
                      "Ensure the model is defined correctly and has a default "
                      "manager.")

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greenova.settings')
django.setup()

# Use relative imports for django apps

# Type annotations for the id attribute that mypy doesn't recognize
if TYPE_CHECKING:
    class DjangoModel(Model):
        id: int

    # Apply the attributes to our models
    class ProjectT(Project, DjangoModel):
        ...

    class EnvironmentalMechanismT(EnvironmentalMechanism, DjangoModel):
        ...

    class ObligationT(Obligation, DjangoModel):
        ...

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
    OBLIGATION_PREFIX_MAPPING: Dict[str, str] = {
        'PREFIX1': 'NormalizedPrefix1',
        'PREFIX2': 'NormalizedPrefix2',
        # Add other mappings as needed
    }

    def handle(self, *args: Any, **options: Any) -> None:
        """Import obligations from a CSV file into the database."""
        csv_path = Path(options['csv_file'])
        if not csv_path.exists():
            self.stderr.write(f"CSV file not found: {csv_path}")
            return

        try:
            # Get or create project
            project_name = options.get('project')
            if not project_name:
                self.stderr.write("Project name is required")
                return

            project = self._get_or_create_project(project_name)
            if not project:
                self.stderr.write(f"Failed to get/create project: {project_name}")
                return

            # Process CSV file
            with csv_path.open('r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)

                if options['dry_run']:
                    self.stdout.write("DRY RUN - No changes will be made")

                for row in reader:
                    try:
                        with transaction.atomic():
                            self._process_obligation_row(row, project, options)
                    except (ValueError, DatabaseError, KeyError) as e:
                        error_msg = f"Error processing row: {e}"
                        if options['continue_on_error']:
                            self.stderr.write(error_msg)
                            continue
                        raise

        except (OSError, csv.Error, DatabaseError) as e:
            self.stderr.write(f"Failed to import obligations: {e}")
            return

        self.stdout.write(self.style.SUCCESS("Successfully imported obligations"))

    def _get_or_create_project(self, project_name: str) -> Optional[Project]:
        """Get existing project or create new one."""
        if not hasattr(Project, 'objects') or not isinstance(Project.objects, Manager):
            raise AttributeError(
                "Project model does not have a valid 'objects' manager."
            )
        try:
            existing_project: Project = Project.objects.get(name=project_name)
            logger.info("Found existing project: %s", project_name)
            return existing_project
        except Project.DoesNotExist:
            try:
                new_project: Project = Project.objects.create(name=project_name)
                logger.info("Created new project: %s", project_name)
                return new_project
            except DatabaseError as e:
                logger.error("Error creating project %s: %s", project_name, e)
                return None

    def _process_obligation_row(
        self,
        row: Dict[str, Any],
        project: Project,
        options: Dict[str, Any]
    ) -> None:
        """Process a single row from the CSV file."""
        if options['dry_run']:
            self.stdout.write(f"Would process row: {row}")
            return

        # Process the row data
        obligation_data = self.process_row(row, project)

        # Create or update the obligation
        result, status = self.create_or_update_obligation(
            obligation_data,
            force_update=options['update']
        )

        if result:
            action = "Created" if status == "created" else "Updated"
            self.stdout.write(
                f"{action} obligation: {obligation_data['obligation_number']}"
            )

    help = 'Import obligations from CSV file'

    # Mechanism mapping moved directly into the command
    MECHANISM_ID_MAPPING: Dict[str, str] = {
        'MS1180': 'MS1180',
        # Add other mappings here if needed
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
            help=(
                'Process each row without wrapping in a transaction '
                '(use for database issues)'
            )
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

        mechanism = self._retrieve_mechanism(mechanism_name, project)
        if mechanism:
            return mechanism, False

        return self._create_mechanism(mechanism_name, project)

    def _retrieve_mechanism(
        self, mechanism_name: str, project: Project
    ) -> Optional[EnvironmentalMechanism]:
        """Retrieve an existing mechanism."""
        try:
            mechanism: EnvironmentalMechanism = (
                EnvironmentalMechanism.objects.get(  # type: ignore
                    name=mechanism_name,
                    project=project,
                )
            )
            if not mechanism.primary_environmental_mechanism:
                mechanism.primary_environmental_mechanism = mechanism_name
                mechanism.save()
            return mechanism
        except EnvironmentalMechanism.MultipleObjectsReturned:
            logger.error(
                'Multiple mechanisms found for %s in project %s',
                mechanism_name,
                project.name
            )
            return None
        except EnvironmentalMechanism.DoesNotExist:
            return None

    def _create_mechanism(
        self, mechanism_name: str, project: Project
    ) -> Tuple[Optional[EnvironmentalMechanism], bool]:
        """Create a new mechanism."""
        try:
            mechanism = EnvironmentalMechanism.objects.create(  # type: ignore
                name=mechanism_name,
                project=project,
                primary_environmental_mechanism=mechanism_name
            )
            logger.info(
                'Created new mechanism: %s for project %s',
                mechanism.name,
                project.name
            )
            return mechanism, True
        except (DatabaseError, ValueError) as e:
            logger.error(
                "Error creating mechanism %s: %s",
                mechanism_name,
                str(e),
            )
            return None, False

    def map_environmental_aspect(self, aspect: str) -> str:
        """Map environmental aspect to standardized value."""
        if not aspect:
            return 'Other'

        aspect = aspect.strip()
        aspect_key = aspect.lower()

        # Define mapping for commonly observed aspects
        aspect_mapping: Dict[str, str] = {
            'administration': 'Administration',
            'cultural heritage management': 'Cultural Heritage Management',
            'terrestrial fauna management': 'Terrestrial Fauna Management',
            'biosecurity and pest management': 'Biosecurity And Pest Management',
            'dust management': 'Dust Management',
            'reporting': 'Reporting',
            'noise management': 'Noise Management',
            'erosion and sedimentation management': (
                'Erosion And Sedimentation Management'
            ),
            'hazardous substances and hydrocarbon management': (
                'Hazardous Substances And Hydrocarbon Management'
            ),
            'waste management': 'Waste Management',
            'artificial light management': 'Artificial Light Management',
            'audits and inspections': 'Audits And Inspections',
            'design and construction requirements': (
                'Design And Construction Requirements'
            ),
            'regulatory compliance reporting': 'Regulatory Compliance Reporting',
            'portside cemp': 'Administration',
            'limitations and extent of proposal': 'Other',
        }

        return aspect_mapping.get(aspect_key, aspect)

    def parse_date_safe(self, date_value: Any) -> Optional[Any]:
        """Safely parse a date value."""
        if not date_value:
            return None

        try:
            return parse_date(str(date_value))
        except (ValueError, TypeError):
            logger.warning("Invalid date value: %s", date_value)
            return None

    def generate_obligation_number(self) -> str:
        """Generate a unique obligation number for missing values."""
        return f"UNKNOWN-{timezone.now().timestamp()}"

    def process_row(self, row: Dict[str, Any], project: Project) -> ObligationData:
        """
        Process and clean a CSV row.

        Args:
            row: Dictionary containing CSV row data
            project: Project instance

        Returns:
            Processed data dictionary with cleaned values
        """
        mechanism = self._process_mechanism(row, project)
        status = self._normalize_status(row.get('status', ''))
        environmental_aspect = self._map_environmental_aspect(
            row.get('environmental__aspect', '')
        )
        action_due_date = self._parse_date_safe(row.get('action__due_date'))
        close_out_date = self._parse_date_safe(row.get('close__out__date'))
        recurring_forecasted_date = self._parse_date_safe(
            row.get('recurring__forcasted__date')
        )
        obligation_number = self._get_or_generate_obligation_number(
            row.get('obligation__number')
        )

        if row.get('recurring__frequency'):
            normalize_frequency(row['recurring__frequency'])

        result: ObligationData = {
            'obligation_number': self.normalize_obligation_number(obligation_number),
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
            'recurring_obligation': self.clean_boolean(
                row.get('recurring__obligation')
            ),
            'recurring_frequency': row.get('recurring__frequency', ''),
            'recurring_status': row.get('recurring__status', ''),
            'recurring_forcasted_date': recurring_forecasted_date,
            'inspection': self.clean_boolean(row.get('inspection')),
            'inspection_frequency': row.get('inspection__frequency', ''),
            'site_or_desktop': row.get('site_or__desktop', ''),
            'gap_analysis': self.clean_boolean(row.get('gap__analysis')),
            'notes_for_gap_analysis': row.get('notes_for__gap__analysis', ''),
        }
        logger.info('Importing obligation: %s', obligation_number)
        return result

    def _process_mechanism(
        self,
        row: Dict[str, Any],
        project: Project
    ) -> Optional[EnvironmentalMechanism]:
        mechanism_name = row.get('primary__environmental__mechanism')
        mechanism, created = self.get_or_create_mechanism(mechanism_name, project)
        if created and mechanism is not None:
            logger.info(
                'Created new mechanism: %s for project %s',
                mechanism.name,
                project.name
            )
        return mechanism

    def _normalize_status(self, status: str) -> str:
        status = status.lower()
        return (
            status
            if status in ('not started', 'in progress', 'completed')
            else 'not started'
        )

    def _map_environmental_aspect(self, aspect: Optional[str]) -> str:
        return self.map_environmental_aspect(aspect or '')

    def _parse_date_safe(self, date_value: Any) -> Optional[Any]:
        return self.parse_date_safe(date_value)

    def _get_or_generate_obligation_number(
        self, obligation_number: Optional[str]
    ) -> str:
        if not obligation_number:
            obligation_number = f"UNKNOWN-{timezone.now().timestamp()}"
            logger.warning(
                "Missing obligation number, using generated number: %s",
                obligation_number,
            )
        return obligation_number

    def create_or_update_obligation(
        self,
        obligation_data: ObligationData,
        force_update: bool = False
    ) -> Tuple[Union[Obligation, bool, None], str]:
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
            existing = Obligation.objects.filter(  # type: ignore[attr-defined]
                obligation_number=obligation_number
            ).first()

            if existing and not force_update:
                return False, "skipped"

            if existing:
                # Update existing obligation
                for key, value in obligation_data.items():
                    if key != 'obligation_number':  # Don't update the primary key
                        setattr(existing, key, value)
                existing.save()
                existing_t = cast(ObligationT, existing) if TYPE_CHECKING else existing
                with connection.cursor() as cursor:
                    cursor.execute(
                        (
                            "UPDATE obligations_obligation "
                            "SET updated_at = NOW() "
                            "WHERE id = %s"
                        ),
                        [existing_t.id]
                    )
                return existing, "updated"
            # Create new obligation
            new_obligation = Obligation(**obligation_data)
            new_obligation.save()
            new_obligation_t = (
                cast(ObligationT, new_obligation)
                if TYPE_CHECKING
                else new_obligation
            )
            with connection.cursor() as cursor:
                cursor.execute(
                    (
                        "UPDATE obligations_obligation "
                        "SET created_at = NOW() "
                        "WHERE id = %s"
                    ),
                    [new_obligation_t.id]  # type: ignore[attr-defined]
                )
            return new_obligation, "created"

        except DatabaseError as e:
            logger.error(
                "Error creating/updating obligation %s: %s",
                obligation_number,
                str(e),
            )
            return None, f"error: {str(e)}"
