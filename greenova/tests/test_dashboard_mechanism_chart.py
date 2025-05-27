"""
Test that only the environmental mechanisms analysis card is rendered.

This test ensures that no procedures, upcoming obligations, or projects at risk
cards are rendered when a project is selected from the project selector tool.
"""

from typing import Any

import pytest
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from mechanisms.models import EnvironmentalMechanism
from stubs.projects.models import Project

CHART_CARD_EXPECTED_COUNT = 1  # Only Mechanism


@pytest.mark.django_db
def test_single_mechanism_chart_card(
    client: Any,
    regular_user: AbstractUser,
    project: Project,
    mechanism: EnvironmentalMechanism,
) -> None:
    """
    Test that only the environmental mechanisms analysis card is rendered.

    This test ensures that no procedures, upcoming obligations, or projects at risk
    cards are rendered when a project is selected from the project selector tool.
    """
    client.force_login(regular_user)
    url = reverse("dashboard:home") + f"?project_id={getattr(project, 'id', 1)}"
    response = client.get(url, HTTP_HX_REQUEST="true")
    html = response.content.decode("utf-8")
    # There should be only one mechanism chart container
    assert html.count('id="mechanism-data-container"') == 1
    # There should be only one chart card (mechanism)
    assert html.count('class="card chart-container"') == CHART_CARD_EXPECTED_COUNT
    # Ensure no procedures chart card
    assert 'id="procedures-data-container"' not in html
    # Ensure no upcoming obligations card
    assert "Upcoming Obligations" not in html
    # Ensure no projects at risk card
    assert "Projects at Risk of Missing Deadlines" not in html
    # Ensure no duplicate chart galleries
    assert html.count("chart-gallery") <= 1
