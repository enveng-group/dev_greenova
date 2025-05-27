"""Management command to create missing user profiles in Greenova.

This command iterates through all users and creates a profile for any user
who does not have one.
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from models import Profile

User = get_user_model()


class Command(BaseCommand):
    """Command to create missing user profiles."""
    help = "Creates profiles for users who do not have one"

    def handle(self, *args, **options):
        """Handle the command execution to create missing profiles."""
        count = 0
        for user in User.objects.all():
            try:
                # Try to access profile to see if it exists
                user.profile
            except Profile.DoesNotExist:
                # Create profile if it doesn't exist
                Profile.objects.create(user=user)
                count += 1

        self.stdout.write(self.style.SUCCESS(f"Created {count} missing profiles"))
