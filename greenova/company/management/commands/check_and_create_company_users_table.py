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

"""Management command to check and create the company_company_users table.

This module defines a custom Django management command for ensuring the
company_company_users table exists in the database for the company app.
"""
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    """Custom management command to check and create company_company_users table."""

    help = "Check and create the company_company_users table if it does not exist."

    def handle(self, *args: object, **options: object) -> None:
        """Execute the command to check and create the company_company_users table.

        Args:
            *args: Variable length argument list.
            **options: Arbitrary keyword arguments.

        """
        with connection.cursor() as cursor:
            # Check if the table exists
            cursor.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name='company_company_users';",
            )
            result = cursor.fetchone()

            if result:
                self.stdout.write(
                    self.style.SUCCESS(
                        "The company_company_users table already exists.",
                    ),
                )
            else:
                # Create the table if it does not exist
                cursor.execute(
                    """
                    CREATE TABLE company_company_users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        company_id INTEGER NOT NULL,
                        user_id INTEGER NOT NULL,
                        FOREIGN KEY(company_id) REFERENCES company_company(id),
                        FOREIGN KEY(user_id) REFERENCES auth_user(id),
                        UNIQUE(company_id, user_id)
                    );
                    """,
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        "The company_company_users table has been created.",
                    ),
                )
