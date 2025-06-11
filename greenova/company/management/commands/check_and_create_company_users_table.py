from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Check and create the company_company_users table if it does not exist."

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Check if the table exists
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='company_company_users';"
            )
            result = cursor.fetchone()

            if result:
                self.stdout.write(
                    self.style.SUCCESS(
                        "The company_company_users table already exists."
                    )
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
                    """
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        "The company_company_users table has been created."
                    )
                )
