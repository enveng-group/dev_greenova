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

"""Management command to import obligations from CSV into the obligations app."""

# Standard library imports
# Third-party library imports
from django.core.management.base import BaseCommand
import argparse
from typing import TYPE_CHECKING, ClassVar


# Local application imports

if TYPE_CHECKING:
    from django.db.models import Model
    from mechanisms.models import EnvironmentalMechanism
    from models import Obligation
    from projects.models import Project

    class DjangoModel(Model):
        """Type stub for Django model with id attribute."""

        id: int

    class ProjectT(Project):
        """Type stub for Project with DjangoModel attributes."""

    class EnvironmentalMechanismT(EnvironmentalMechanism):
        """Type stub for EnvironmentalMechanism with DjangoModel attributes."""

    class ObligationT(Obligation):
        """Type stub for Obligation with DjangoModel attributes."""


class Command(BaseCommand):
    """Django management command to import obligations from CSV."""

    OBLIGATION_PREFIX_MAPPING: ClassVar[dict[str, str]] = {
        "PREFIX1": "NormalizedPrefix1",
        # ...existing code...
    }
    # ...existing code...

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Add command-line arguments for import_obligations command."""
        parser.add_argument(
            "csv_file",
            help="Path to the CSV file to import.",
        )
        # ...existing code...
