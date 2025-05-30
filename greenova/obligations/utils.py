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

"""Utility functions for the obligations app.

Provides helpers for status, frequency normalization, and responsibility display.
"""

from typing import cast
from datetime import date
from beartype import beartype
from models import Obligation
from constants import FREQUENCY_ALIASES


@beartype
def normalize_frequency(frequency: str) -> str:
    """Normalize frequency string to canonical value used in the system.

    Args:
        frequency: The frequency string to normalize.

    Returns:
        The canonical frequency string.

    """
    freq = frequency.strip().lower().replace(" ", "-")
    # Explicitly cast to str to satisfy type checker
    return cast("str", FREQUENCY_ALIASES.get(freq, freq))


@beartype
def is_obligation_overdue(obligation: Obligation) -> bool:
    """Check if an obligation is overdue.

    Args:
        obligation: The Obligation instance to check.

    Returns:
        True if the obligation is overdue, False otherwise.

    """
    if not obligation.action_due_date:
        return False
    if obligation.status == "completed":
        return False
    # Ensure the comparison returns a bool
    return bool(obligation.action_due_date < date.today())
