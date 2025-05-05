from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from users.models import Profile

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates profiles for users who do not have one'

    def handle(self, *args, **options):
        count = 0
        for user in User.objects.all():
            try:
                # Try to access profile to see if it exists
                user.profile
            except Profile.DoesNotExist:
                # Create profile if it doesn't exist
                Profile.objects.create(user=user)
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Created {count} missing profiles'))
