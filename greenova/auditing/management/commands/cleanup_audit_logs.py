from beartype import beartype
from django.core.management.base import BaseCommand
from auditing.tasks import cleanup_audit_logs

class Command(BaseCommand):
    help = "Clean up audit logs older than 2 years."

    @beartype
    def handle(self, *args: object, **options: object) -> None:
        cleanup_audit_logs()
        self.stdout.write(self.style.SUCCESS("Audit logs cleanup complete."))
