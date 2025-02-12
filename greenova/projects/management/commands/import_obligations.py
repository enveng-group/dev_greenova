from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from projects.models import Project, Obligation
import csv
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Import obligations from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        self.stdout.write(f"Importing obligations from {csv_file}")
        
        try:
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                
                # Create projects first
                projects = {}
                obligations_created = 0
                obligations_updated = 0

                for row in reader:
                    # Create or get project
                    project_name = row['project__name']
                    if project_name not in projects:
                        project, created = Project.objects.get_or_create(
                            name=project_name,
                            defaults={'description': f'Imported from CSV on {datetime.now().date()}'}
                        )
                        projects[project_name] = project
                        if created:
                            self.stdout.write(f"Created new project: {project_name}")
                    
                    # Parse dates
                    action_due_date = parse_date(row['action__due_date']) if row['action__due_date'] else None
                    close_out_date = parse_date(row['close__out__date']) if row['close__out__date'] else None
                    recurring_forecasted_date = parse_date(row['recurring__forcasted__date']) if row['recurring__forcasted__date'] else None

                    # Create or update obligation
                    obligation, created = Obligation.objects.update_or_create(
                        obligation_number=row['obligation__number'],
                        defaults={
                            'project': projects[project_name],
                            'primary_environmental_mechanism': row['primary__environmental__mechanism'],
                            'environmental_aspect': row['environmental__aspect'],
                            'obligation': row['obligation'],
                            'status': row['status'].lower() if row['status'] else 'not started',
                            'action_due_date': action_due_date,
                            'close_out_date': close_out_date,
                            # Add other fields as needed
                        }
                    )

                    if created:
                        obligations_created += 1
                    else:
                        obligations_updated += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully imported {obligations_created} new obligations '
                        f'and updated {obligations_updated} existing obligations'
                    )
                )

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'File not found: {csv_file}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error importing obligations: {str(e)}')
            )