"""Copyright (C) 2025 Adrian Gallo.

This file is part of Greenova.

Greenova is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Greenova is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Greenova. If not, see <https://www.gnu.org/licenses/>.

Author: Adrian Gallo <agallo@enveng-group.com.au>
"""

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

    def handle(self, *args: object, **options: object) -> None:
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
