"""Unit tests for the Greenova core app.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

from datetime import UTC, datetime

from beartype import beartype
from django.test import TestCase
from django.urls import reverse

from .models import EnvironmentalObligation


class EnvironmentalObligationModelTests(TestCase):
    """Tests for EnvironmentalObligation model."""

    @beartype
    def test_create_obligation(self) -> None:
        """Test creating an EnvironmentalObligation instance."""
        obj = EnvironmentalObligation.objects.create(
            name="Test Obligation",
            description="Test description.",
            due_date=datetime.now(UTC).date(),
            is_complete=False,
        )
        assert obj.name == "Test Obligation"
        assert not obj.is_complete


class EnvironmentalObligationListViewTests(TestCase):
    """Tests for EnvironmentalObligationListView."""

    @beartype
    def test_obligation_list_view(self) -> None:
        """Test the obligation list view returns 200 and contains expected content."""
        url = reverse("core:obligation_list")
        response = self.client.get(url)
        assert response.status_code == 200
        self.assertContains(response, "Environmental Obligations")
