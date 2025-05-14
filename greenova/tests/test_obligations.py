"""
Unit tests for the obligations app in the Greenova project.

These tests cover the summary view, template rendering, HTMX interactivity,
and delete functionality for obligations.
"""

# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

import pytest
from django.test import Client
from django.urls import reverse
from mechanisms.models import EnvironmentalMechanism
from obligations.models import Obligation
from projects.models import Project

HTTP_OK = 200


@pytest.mark.django_db
def test_obligation_summary_view(authenticated_client: Client):
    """Test the ObligationSummaryView with filtering capabilities."""
    # Setup test data
    project = Project.objects.create(name="Test Project")
    mechanism = EnvironmentalMechanism.objects.create(
        name="Test Mechanism", project=project
    )
    obligation1 = Obligation.objects.create(
        obligation_number="OBL001",
        obligation="Test Obligation 1",
        status="not_started",
        primary_environmental_mechanism=mechanism,
        project=project,
    )
    obligation2 = Obligation.objects.create(
        obligation_number="OBL002",
        obligation="Test Obligation 2",
        status="in_progress",
        primary_environmental_mechanism=mechanism,
        project=project,
    )

    # Test filtering by status
    url = reverse("obligations:summary") + (
        f"?status=not_started&mechanism_id={mechanism.id}"
    )
    response = authenticated_client.get(url)
    assert response.status_code == HTTP_OK
    assert obligation1.obligation_number in response.content.decode()
    assert obligation2.obligation_number not in response.content.decode()


@pytest.mark.django_db
def test_obligation_list_template(authenticated_client: Client):
    """Test the obligation list template rendering."""
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
    )

    # Test rendering of obligation list
    url = reverse("obligations:summary") + (f"?mechanism_id={mechanism.id}")
    response = authenticated_client.get(url)
    assert response.status_code == HTTP_OK
    assert "Test Obligation" in response.content.decode()


@pytest.mark.django_db
def test_procedure_charts_interactivity(authenticated_client: Client):
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


@pytest.mark.django_db
def test_obligation_delete_view(admin_client: Client):
    """Test the ObligationDeleteView functionality."""
    # Setup test data
    project = Project.objects.create(name="Test Project")
    mechanism = EnvironmentalMechanism.objects.create(
        name="Test Mechanism", project=project
    )
    obligation = Obligation.objects.create(
        obligation_number="OBL001",
        obligation="Test Obligation",
        status="not_started",
        primary_environmental_mechanism=mechanism,
        project=project,
    )

    # Test deletion
    url = reverse("obligations:delete", args=[obligation.obligation_number])
    response = admin_client.post(url)
    assert response.status_code == HTTP_OK
    assert not Obligation.objects.filter(obligation_number="OBL001").exists()
