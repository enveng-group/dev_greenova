"""Models for the Greenova core app.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

from beartype import beartype
from django.db import models


class EnvironmentalObligation(models.Model):
    """Model representing an environmental obligation for compliance tracking.

    Attributes:
        name: The name of the obligation.
        description: A detailed description of the obligation.
        due_date: The due date for compliance.
        is_complete: Whether the obligation has been fulfilled.
        created_at: Timestamp when the obligation was created.
        updated_at: Timestamp when the obligation was last updated.

    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @beartype
    def __str__(self) -> str:
        """Return a string representation of the obligation.

        Returns:
            str: The obligation's name and due date as a string.

        """
        return f"{self.name} (Due: {self.due_date})"
