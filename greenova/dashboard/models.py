"""Copyright (C) 2024 Adrian Gallo <agallo@enveng-group.com.au>
This file is part of Greenova and is licensed under the AGPL-3.0.

Dashboard app models for Greenova.
"""

from beartype import beartype
from django.db import models


@beartype
class DashboardStubModel(models.Model):
    """Stub model for dashboard app (to be replaced with real models).

    This is a placeholder for future dashboard models.
    """

    name = models.CharField(max_length=128)

    class Meta:
        """Meta options for DashboardStubModel.

        This model is abstract and not registered with the database.

        """

        abstract = True

    def __str__(self) -> str:
        """Return string representation of DashboardStubModel.

        Returns:
            str: String representation of the model.

        """
        return f"DashboardStubModel(name={self.name})"


class DashboardModel(models.Model):
    """Base model for dashboard app (placeholder, extend as needed)."""

    def __str__(self) -> str:
        """Return string representation of DashboardModel.

        Returns:
            str: String representation of the model.

        """
        return f"DashboardModel(pk={self.pk})"
