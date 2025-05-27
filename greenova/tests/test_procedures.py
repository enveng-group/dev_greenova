"""
Unit tests for the procedures functionality in the Greenova project.

These tests cover the interactivity of procedure charts with HTMX for
environmental obligations.
"""

# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

import pytest
from django.urls import reverse
from mechanisms.models import EnvironmentalMechanism
from obligations.models import Obligation
from projects.models import Project

HTTP_OK = 200


@pytest.mark.django_db
def test_procedure_charts_interactivity(authenticated_client):
    """Test the interactivity of procedure charts with HTMX."""
    # Setup test data
    project = Project.objects.create(name="Test Project")
    mechanism = EnvironmentalMechanism.objects.create(
        name="Test Mechanism", project=project
    )
    Obligation.objects.create(
        obligation_number="OBL001",
        obligation="Test Obligation",
        status="not_started",
        primary_environmental_mechanism=mechanism,
        project=project,
        procedure="Cultural Heritage Management",
    )

    # Test HTMX interactivity
    url = reverse("obligations:summary") + f"?mechanism_id={mechanism.id}"
    response = authenticated_client.get(url, HTTP_HX_REQUEST="true")
    assert response.status_code == HTTP_OK
    assert "Test Obligation" in response.content.decode()
