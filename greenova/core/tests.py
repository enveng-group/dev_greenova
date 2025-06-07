"""Unit tests for the Greenova core app.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

from datetime import UTC, datetime

from beartype import beartype
from core.serializers import (
    MechanismCollectionProtoSerializer,
    MechanismProtoSerializer,
)
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
        assert getattr(obj, "name", None) == "Test Obligation"
        assert not getattr(obj, "is_complete", True)


class EnvironmentalObligationListViewTests(TestCase):
    """Tests for EnvironmentalObligationListView."""

    @beartype
    def test_obligation_list_view(self) -> None:
        """Test the obligation list view returns 200 and contains expected content."""
        url = reverse("core:obligation_list")
        response = self.client.get(url)
        assert response.status_code == 200
        self.assertContains(response, "Environmental Obligations")


class MechanismProtoSerializerTests(TestCase):
    """Tests for MechanismProtoSerializer."""

    @beartype
    def test_is_valid_with_none_data(self) -> None:
        serializer = MechanismProtoSerializer(data=None)
        assert not serializer.is_valid()
        assert serializer.errors == "No data provided."

    @beartype
    def test_is_valid_with_invalid_data(self) -> None:
        serializer = MechanismProtoSerializer(data=b"invalid")
        assert not serializer.is_valid()
        assert serializer.errors == "Invalid protobuf data."

    @beartype
    def test_data_with_no_instance(self) -> None:
        serializer = MechanismProtoSerializer()
        assert serializer.data() is None


class MechanismCollectionProtoSerializerTests(TestCase):
    """Tests for MechanismCollectionProtoSerializer."""

    @beartype
    def test_is_valid_with_none_data(self) -> None:
        serializer = MechanismCollectionProtoSerializer(data=None)
        assert not serializer.is_valid()
        assert serializer.errors == "No data provided."

    @beartype
    def test_is_valid_with_invalid_data(self) -> None:
        serializer = MechanismCollectionProtoSerializer(data=b"invalid")
        assert not serializer.is_valid()
        assert serializer.errors == "Invalid protobuf data or empty collection."

    @beartype
    def test_data_with_no_instances(self) -> None:
        serializer = MechanismCollectionProtoSerializer()
        assert serializer.data() is None
