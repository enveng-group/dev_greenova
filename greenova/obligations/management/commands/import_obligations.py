import csv
import logging
import os
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from obligations.models import Obligation

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import obligations from CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file",
            nargs="?",
            type=str,
            default="/home/ubuntu/greenova/clean_output_with_nulls.csv",
            help="Path to the CSV file",
        )

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]

        if not os.path.exists(csv_file):
            raise CommandError(f"CSV file does not exist: {csv_file}")

        try:
            with open(csv_file, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                # Validate CSV headers
                required_fields = [
                    "obligation__number",
                    "project__name",
                    "obligation",
                ]
                missing_fields = []
                if reader.fieldnames:
                    missing_fields = [
                        field
                        for field in required_fields
                        if field not in reader.fieldnames
                    ]
                if missing_fields:
                    raise CommandError(
                        f'Missing required fields in CSV: {", ".join(missing_fields)}'
                    )

                for row in reader:
                    try:
                        # Parse dates
                        action_due_date = None
                        close_out_date = None
                        recurring_forcasted_date = None

                        if (
                            row["action__due_date"]
                            and row["action__due_date"].lower() != "null"
                        ):
                            action_due_date = datetime.strptime(
                                row["action__due_date"], "%Y-%m-%d"
                            ).date()
                        if (
                            row["close__out__date"]
                            and row["close__out__date"].lower() != "null"
                        ):
                            close_out_date = datetime.strptime(
                                row["close__out__date"], "%Y-%m-%d"
                            ).date()
                        if (
                            row["recurring__forcasted__date"]
                            and row["recurring__forcasted__date"].lower()
                            != "null"
                        ):
                            recurring_forcasted_date = datetime.strptime(
                                row["recurring__forcasted__date"], "%Y-%m-%d"
                            ).date()

                        # Parse booleans
                        recurring_obligation = (
                            row["recurring__obligation"].lower() == "true"
                            if row["recurring__obligation"].lower() != "null"
                            else False
                        )
                        inspection = (
                            row["inspection"].lower() == "true"
                            if row["inspection"].lower() != "null"
                            else False
                        )
                        new_control_action_required = (
                            row["new__control__action_required"].lower()
                            == "true"
                            if row["new__control__action_required"].lower()
                            != "null"
                            else False
                        )

                        # Create or update obligation
                        obligation, created = (
                            Obligation.objects.update_or_create(
                                obligation_number=row["obligation__number"],
                                defaults={
                                    "project_name": row["project__name"],
                                    "primary_environmental_mechanism": row[
                                        "primary__environmental__mechanism"
                                    ],
                                    "procedure": row["procedure"],
                                    "environmental_aspect": row[
                                        "environmental__aspect"
                                    ],
                                    "obligation": row["obligation"],
                                    "accountability": row["accountability"],
                                    "project_phase": row["project_phase"],
                                    "action_due_date": action_due_date,
                                    "close_out_date": close_out_date,
                                    "status": row["status"],
                                    "supporting_information": row[
                                        "supporting__information"
                                    ],
                                    "general_comments": row[
                                        "general__comments"
                                    ],
                                    "compliance_comments": row[
                                        "compliance__comments"
                                    ],
                                    "non_conformance_comments": row[
                                        "non_conformance__comments"
                                    ],
                                    "evidence": row["evidence"],
                                    "person_email": row["person_email"],
                                    "recurring_obligation": recurring_obligation,
                                    "recurring_frequency": row[
                                        "recurring__frequency"
                                    ],
                                    "recurring_status": row[
                                        "recurring__status"
                                    ],
                                    "recurring_forcasted_date": recurring_forcasted_date,
                                    "inspection": inspection,
                                    "inspection_frequency": row[
                                        "inspection__frequency"
                                    ],
                                    "site_or_desktop": row["site_or__desktop"],
                                    "new_control_action_required": new_control_action_required,
                                    "obligation_type": row["obligation_type"],
                                    "gap_analysis": row["gap__analysis"],
                                    "notes_for_gap_analysis": row[
                                        "notes_for__gap__analysis"
                                    ],
                                    "covered_in_which_inspection_checklist": row[
                                        "covered_in_which_inspection_checklist"
                                    ],
                                },
                            )
                        )
                        action = "Created" if created else "Updated"
                        logger.info(
                            f'{action} obligation {row["obligation__number"]}'
                        )
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'{action} obligation {row["obligation__number"]}'
                            )
                        )

                    except Exception as e:
                        logger.error(
                            f'Error processing obligation {row["obligation__number"]}: {str(e)}'
                        )
                        self.stdout.write(
                            self.style.ERROR(
                                f'Error processing obligation {row["obligation__number"]}: {str(e)}'
                            )
                        )

        except Exception as e:
            logger.error(f"Error reading CSV file: {str(e)}")
            raise CommandError(f"Error reading CSV file: {str(e)}")

        self.stdout.write(self.style.SUCCESS("Finished importing obligations"))
