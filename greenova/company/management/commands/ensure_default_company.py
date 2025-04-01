import logging

from company.models import Company
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Ensures the default TBA company with ID 1 exists'

    def handle(self, *args, **kwargs):
        default_company, created = Company.objects.get_or_create(
            id=1,
            defaults={
                'name': 'TBA',
                'description': 'Default company for unassigned items',
                'company_type': 'other',
                'is_active': True
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Created default TBA company with ID 1'))
        else:
            self.stdout.write(self.style.SUCCESS('Default TBA company already exists'))

        # Removed project-related code as the relationship has been removed
