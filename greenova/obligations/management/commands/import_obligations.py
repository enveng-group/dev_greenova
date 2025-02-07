import csv
import logging
from datetime import datetime
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from obligations.models import Obligation

logger = logging.getLogger('greenova.obligations')


class Command(BaseCommand):
    help = 'Import obligations from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument(
            '--update-existing',
            action='store_true',
            help='Update existing records',
        )

    def clean_data(self, row):
        """Clean and validate row data."""
        cleaned_data = {}

        # Set default values for required fields
        cleaned_data['status'] = 'not started'  # Default status

        for key, value in row.items():
            model_key = key.replace('__', '_')

            # Skip empty values
            if not value or value.lower() in ('', 'null'):
                continue

            # Handle boolean fields
            if model_key in [
                'recurring_obligation',
                'inspection',
                'new_control_action_required',
            ]:
                cleaned_data[model_key] = value.lower() in ['true', '1', 'yes']
                continue

            # Handle date fields
            if model_key in [
                'action_due_date',
                'close_out_date',
                'recurring_forcasted_date',
            ]:
                try:
                    cleaned_data[model_key] = datetime.strptime(
                        value, '%Y-%m-%d'
                    ).date()
                except (ValueError, TypeError):
                    continue

            # Handle regular fields
            cleaned_data[model_key] = value

        return cleaned_data

    def process_row(self, row, update_existing=False):
        """Process a single row with its own transaction."""
        try:
            with transaction.atomic():
                cleaned_data = self.clean_data(row)

                # Validate required fields
                if not cleaned_data.get('obligation_number'):
                    raise ValueError('Missing obligation number')
                if not cleaned_data.get('project_name'):
                    raise ValueError('Missing project name')
                if not cleaned_data.get('obligation'):
                    raise ValueError('Missing obligation text')

                if update_existing:
                    obligation, created = Obligation.objects.update_or_create(
                        obligation_number=cleaned_data['obligation_number'],
                        defaults=cleaned_data,
                    )
                    action = 'Updated' if not created else 'Created'
                else:
                    obligation = Obligation.objects.create(**cleaned_data)
                    action = 'Created'

                logger.info(
                    f'{action} obligation: {obligation.obligation_number}'
                )
                return True, None

        except Exception as e:
            error_msg = f'Error processing obligation: {str(e)}'
            logger.error(error_msg, exc_info=True)
            return False, error_msg

    def handle(self, *args, **options):
        csv_file_path = Path(options['csv_file'])
        update_existing = options['update_existing']
        success_count = 0
        error_count = 0

        if not csv_file_path.exists():
            raise CommandError(f'File not found: {csv_file_path}')

        try:
            with csv_file_path.open('r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                # Validate CSV structure
                required_fields = {
                    'obligation__number',
                    'project__name',
                    'obligation',
                }

                if not reader.fieldnames:
                    raise CommandError('CSV file has no header row')

                missing_fields = required_fields - set(reader.fieldnames)
                if missing_fields:
                    raise CommandError(
                        f'Missing required fields: {", ".join(missing_fields)}'
                    )

                # Process each row individually
                for row_num, row in enumerate(reader, start=1):
                    self.stdout.write(
                        f'Processing row {row_num}: {row.get("obligation__number", "N/A")}'
                    )

                    success, error = self.process_row(row, update_existing)

                    if success:
                        success_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Successfully processed row {row_num}'
                            )
                        )
                    else:
                        error_count += 1
                        self.stdout.write(
                            self.style.ERROR(
                                f'Error on row {row_num}: {error}'
                            )
                        )

        except Exception as e:
            raise CommandError(f'Import failed: {str(e)}')

        finally:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\nImport completed:\n'
                    f'Successfully processed: {success_count}\n'
                    f'Errors: {error_count}'
                )
            )
