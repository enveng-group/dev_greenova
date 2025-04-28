import logging
from typing import Any, Dict, Optional, Tuple, TypedDict, Union

from django.core.management.base import BaseCommand, CommandParser
from django.db import DatabaseError, IntegrityError
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

    # Removed incomplete method definition causing SyntaxError
        # Removed invalid line causing SyntaxError
    def get_or_create_mechanism(
        self, mechanism_name: Optional[str], project: Project
    ) -> Tuple[Optional[EnvironmentalMechanism], bool]:
        """Get or create an environmental mechanism for the project."""
        if not mechanism_name:
            return None, False

        mechanism_name = mechanism_name.strip()

        try:
            mechanism = EnvironmentalMechanism.objects.get(
                name=mechanism_name,
            )
            return mechanism, False
        except EnvironmentalMechanism.DoesNotExist:
            try:
                mechanism = EnvironmentalMechanism.objects.create(
                    name=mechanism_name,
                    project=project,
                    primary_environmental_mechanism=mechanism_name
                )
                mech_name = getattr(mechanism, 'name', mechanism_name)
                proj_name = getattr(project, 'name', 'Unknown')
                logger.info(
                    'Created new mechanism: %s for project %s',
                    mech_name,
                    proj_name
                )
                return mechanism, True
            except (ValueError, TypeError) as e:
                logger.error(
                    'Invalid data for mechanism %s: %s',
                    mechanism_name,
                    str(e)
                )
                return None, False
        except EnvironmentalMechanism.MultipleObjectsReturned as e:
            logger.error('Multiple mechanisms found for %s: %s', mechanism_name, str(e))
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
            'erosion and sedimentation management': 'Erosion And Sedimentation Management',
            'hazardous substances and hydrocarbon management': 'Hazardous Substances And Hydrocarbon Management',
            'waste management': 'Waste Management',
            'artificial light management': 'Artificial Light Management',
            'audits and inspections': 'Audits And Inspections',
            'design and construction requirements': 'Design And Construction Requirements',
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
        # Get mechanism name, handling possible None value
        mechanism_name = row.get('primary__environmental__mechanism')
        mechanism, created = self.get_or_create_mechanism(mechanism_name, project)

        # Use getattr for safer access - handles type checking issues
        if created and mechanism is not None:
            mech_name = getattr(mechanism, 'name', 'Unknown')
            proj_name = getattr(project, 'name', 'Unknown')
            logger.info(
                'Created new mechanism: %s for project %s',
                mech_name,
                proj_name
            )

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
            'design and construction requirements ': (
                'Design And Construction Requirements'
            ),
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
                logger.warning(
                    "Invalid action due date: %s",
                    row.get('action__due_date'),
                )

        close_out_date = None
        if row.get('close__out__date'):
            try:
                close_out_date = parse_date(str(row.get('close__out__date')))
            except (ValueError, TypeError):
                logger.warning(
                    "Invalid close out date: %s",
                    row.get('close__out__date'),
                )

        recurring_forecasted_date = None
        if row.get('recurring__forcasted__date'):
            try:
                recurring_forecasted_date = parse_date(
                    str(row.get('recurring__forcasted__date'))
                )
            except (ValueError, TypeError):
                logger.warning(
                    "Invalid recurring date: %s",
                    row.get('recurring__forcasted__date'),
                )

        # Make sure we have a valid obligation number
        obligation_number = row.get('obligation__number')
        if not obligation_number:
            obligation_number = f"UNKNOWN-{timezone.now().timestamp()}"
            logger.warning(
                "Missing obligation number, using generated number: %s",
                obligation_number,
            )

        # Normalize recurring frequency
        if row.get('recurring__frequency'):
            normalize_frequency(row['recurring__frequency'])

        # Set timestamps for new records (removed unused variable 'now')

        # Prepare cleaned data
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
        # Removed unused variable 'dry_run'
        try:
        # Removed unused variable 'no_transaction'
            existing = Obligation.objects.filter(
                obligation_number=obligation_number
            ).first()

            if existing and not force_update:
                # Skip if already exists and not forcing update
                return False, "skipped"

            if existing:
                # Update existing obligation
                for key, value in obligation_data.items():
                    if key != 'obligation_number':  # Don't update the primary key
                        setattr(existing, key, value)
                existing.save()
                from django.db import connection
                with connection.cursor() as cursor:
            except OperationalError as e:
                # Create new obligation
                new_obligation = Obligation(**obligation_data)
                new_obligation.save()
                return new_obligation, "created"

            self.stdout.write(
                self.style.WARNING(
        obligation_number=obligation_data.get('obligation_number', '')

        try:
            existing=Obligation.objects.filter(
                obligation_number=obligation_number
            ).first()

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
                new_obligation=Obligation(**obligation_data)
                new_obligation.save()
                return new_obligation, "created"

        except DatabaseError as e:
            logger.error(
                "Error creating/updating obligation %s: %s",
                obligation_number,
                str(e),
            )
            return None, f"error: {str(e)}"
                    logger.error("Error creating project: %s", str(e))
            except (DatabaseError, IntegrityError) as e:
                logger.error("Error getting project: %s", str(e))
            return None

        def handle_dry_run(processed_data: Dict[str, Any]) -> Tuple[str, int]:
            """Handle dry run logic."""
            obligation_number=processed_data.get('obligation_number', '')
            exists=Obligation.objects.filter(
                obligation_number=obligation_number
            ).exists()
            if exists:
                return ("updated", 1) if force_update else ("skipped", 1)
            return "created", 1

        try:
            project_name=row.get('project__name')
            if not project_name:
                logger.error("Missing project name in row")
                return "error", 1

            project=get_or_create_project(project_name)
            if not project:
                return "error", 1

            processed_data=self.process_row(row, project)

            if options.get('dry_run', False):
                return handle_dry_run(processed_data)

            _, status=self.create_or_update_obligation(
                processed_data, force_update=force_update
        force_update=options.get('force_update', False)

        def get_or_create_project(project_name: str) -> Optional[Project]:
        except (ValueError, DatabaseError, IntegrityError) as exc:
            logger.error('Error importing obligation: %s', str(exc))
            return "error", 1

    def handle(self, *_: Any, **options: Any) -> None:
        """
        Execute the command to import obligations from CSV.

        Args:
            _: Command line arguments (not used)
            options: Command line options dictionary
        """
        csv_file=options['csv_file']
        dry_run=options.get('dry_run', False)
            obligation_number=processed_data.get('obligation_number', '')
            exists=Obligation.objects.filter(
                obligation_number=obligation_number
            ).exists()
        required_tables={
            "company_company": "Company model",
            "projects_project": "Project model",
            "mechanisms_environmentalmechanism": "EnvironmentalMechanism model"
        try:
            project_name = row.get('project__name')
            if not project_name:
                logger.error("Missing project name in row")
                return "error", 1

            project = get_or_create_project(project_name)
            if not project:
                return "error", 1

            processed_data = self.process_row(row, project)

            if options.get('dry_run', False):
                return handle_dry_run(processed_data)

            _, status = self.create_or_update_obligation(
                processed_data, force_update=force_update
            )
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
            import csv

            from django.db import connection

            with open(csv_file, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                total_rows = 0
                created_count = 0
                updated_count = 0
                skipped_count = 0
                error_count = 0

                for row in reader:
                    total_rows += 1
                    if no_transaction:
                        status, count = self.process_single_row(row, {
                            'force_update': options.get('update', False),
                            'dry_run': dry_run
                        })

                        if status == "created":
                            created_count += count
                        elif status == "updated":
                            updated_count += count
                        elif status == "skipped":
                            skipped_count += count
                        else:
                            error_count += count
                    else:
                        # Process in transaction
                        try:
                            with transaction.atomic():
                                status, count = self.process_single_row(row, {
                                    'force_update': options.get('update', False),
                                    'dry_run': dry_run
                                })

                                if status == "created":
                                    created_count += count
                                elif status == "updated":
                                    updated_count += count
                                elif status == "skipped":
                                    skipped_count += count
                                else:
                                    error_count += count
                        except Exception as e:
                            error_count += 1
                            logger.error(f"Error processing row: {str(e)}")
                            if not options.get('continue_on_error', False):
                                raise

                # Output summary
                self.stdout.write(self.style.SUCCESS(f"Import completed: {total_rows} rows processed"))
                self.stdout.write(f"Created: {created_count}")
                self.stdout.write(f"Updated: {updated_count}")
                self.stdout.write(f"Skipped: {skipped_count}")

                if error_count:
                    self.stdout.write(self.style.WARNING(f"Errors: {error_count}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Import failed: {str(e)}"))
            logger.error(f"Import error: {str(e)}")
