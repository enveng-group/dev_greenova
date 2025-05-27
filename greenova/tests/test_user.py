"""Unit tests for user profile model and profile view in the Greenova project.

These tests cover user profile relationships, overdue obligations logic, and
profile view context and HTML structure.
"""

# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

# pylint: disable=redefined-outer-name

from datetime import timedelta
from typing import Any

import pytest
from company.models import CompanyMembership
from django.urls import reverse
from django.utils import timezone
from obligations.models import Obligation
from users.models import Profile

HTTP_OK = 200


@pytest.fixture
def company_project_mechanism(company, project, mechanism) -> dict[str, Any]:
    """Fixture to bundle company, project, and mechanism for tests."""
    return {
        "company": company,
        "project": project,
        "mechanism": mechanism,
    }


@pytest.mark.django_db
class TestUserProfileModel:
    """Test suite for user profile model relationships and functionality."""

    def test_profile_responsibility_relationship(self, regular_user, test_company):
        """
        Test the relationship between user profile and responsibility.

        Through company membership.
        """
        # Verify user has a profile
        assert hasattr(regular_user, "profile")
        assert isinstance(regular_user.profile, Profile)

        # Create company membership with role
        membership = CompanyMembership.objects.create(
            user=regular_user, company=test_company, role="manager"
        )

        # Verify role relationship
        user_roles = CompanyMembership.objects.filter(user=regular_user).values_list(
            "role", flat=True
        )
        assert membership.role in user_roles

    def test_profile_overdue_obligations(self, regular_user, company_project_mechanism):
        """Test retrieval of overdue obligations for a user profile."""
        company = company_project_mechanism["company"]
        project = company_project_mechanism["project"]
        mechanism = company_project_mechanism["mechanism"]

        # Create company membership
        membership = CompanyMembership.objects.create(
            user=regular_user, company=company, role="manager"
        )

        # Create overdue obligation
        overdue_obligation = Obligation.objects.create(
            obligation_number="OBL001",
            obligation="Test Overdue",
            status="not_started",
            primary_environmental_mechanism=mechanism,
            project=project,
            action_due_date=timezone.now().date() - timedelta(days=1),
            responsibility=membership.role,
        )

        # Create future obligation
        future_obligation = Obligation.objects.create(
            obligation_number="OBL002",
            obligation="Test Future",
            status="not_started",
            primary_environmental_mechanism=mechanism,
            project=project,
            action_due_date=timezone.now().date() + timedelta(days=1),
            responsibility=membership.role,
        )

        # Add user to project
        project.members.add(regular_user)

        # Count overdue obligations
        user_obligations = Obligation.objects.filter(
            responsibility=membership.role, project__members=regular_user
        )
        overdue_count = sum(1 for obl in user_obligations if obl.is_overdue)

        assert overdue_count == 1
        assert overdue_obligation.is_overdue
        assert not future_obligation.is_overdue


@pytest.mark.django_db
class TestProfileView:
    """Test suite for profile view functionality."""

    def test_profile_overdue_obligations_count(
        self, authenticated_client, regular_user, company_project_mechanism
    ):
        """Testing profile view correctly counts and displays overdue obligations."""
        company = company_project_mechanism["company"]
        project = company_project_mechanism["project"]
        mechanism = company_project_mechanism["mechanism"]

        # Create company membership
        membership = CompanyMembership.objects.create(
            user=regular_user, company=company, role="manager"
        )

        # Create overdue obligation
        Obligation.objects.create(
            obligation_number="OBL003",
            obligation="Test Overdue",
            status="not_started",
            primary_environmental_mechanism=mechanism,
            project=project,
            action_due_date=timezone.now().date() - timedelta(days=1),
            responsibility=membership.role,
        )

        # Add user to project
        project.members.add(regular_user)

        # Make the client authenticated as the regular_user
        authenticated_client.force_login(regular_user)

        # Request the profile page
        url = reverse("users:profile")
        response = authenticated_client.get(url)

        # Check that the response is successful and contains the overdue count
        assert response.status_code == HTTP_OK
        content = response.content.decode("utf-8")

        # Check that overdue count is properly displayed in the HTML
        assert "You have <strong>1</strong> overdue compliance items" in content

        # Check that the overdue count is positioned correctly in the HTML structure
        # It should appear after the profile section and before the contact information
        profile_section_html = '<div class="profile-section">'
        overdue_alert_html = '<div class="alert alert-warning overdue-alert">'
        contact_info_html = '<div class="contact-info">'

        # Check for proper sequence of elements in the HTML
        profile_pos = content.find(profile_section_html)
        overdue_pos = content.find(overdue_alert_html)
        contact_pos = content.find(contact_info_html)

        # Verify correct positioning - profile -> overdue -> contact info
        assert profile_pos < overdue_pos < contact_pos, (
            "Overdue obligations alert is not positioned correctly"
        )

    def test_profile_view_context(
        self, authenticated_client, regular_user, company_project_mechanism
    ) -> None:
        """Test that the profile view provides the correct context data.

        Args:
            authenticated_client: Django test client authenticated as the user.
            regular_user: The user instance for testing.
            company_project_mechanism: Fixture with company, project, mechanism.

        Returns:
            None
        """
        # Group related objects to reduce local variables
        context_bundle = company_project_mechanism
        company = context_bundle["company"]
        project = context_bundle["project"]
        mechanism = context_bundle["mechanism"]

        # Create company membership and overdue obligation
        membership = CompanyMembership.objects.create(
            user=regular_user, company=company, role="manager"
        )
        Obligation.objects.create(
            obligation_number="OBL003",
            obligation="Test Overdue",
            status="not_started",
            primary_environmental_mechanism=mechanism,
            project=project,
            action_due_date=timezone.now().date() - timedelta(days=1),
            responsibility=membership.role,
        )
        project.members.add(regular_user)
        authenticated_client.force_login(regular_user)
        url = reverse("users:profile")
        response = authenticated_client.get(url)

        # Group context checks
        context = response.context
        assert "profile" in context
        assert "overdue_count" in context
        assert context["overdue_count"] == 1

        # Verify user's role and responsibilities
        user_role = membership.role
        assert CompanyMembership.objects.filter(
            user=regular_user, role=user_role
        ).exists()
        assert Obligation.objects.filter(responsibility=user_role).count() == 1

    def test_profile_overdue_alert_html_structure(
        self, authenticated_client, regular_user, company_project_mechanism
    ):
        """Test the HTML structure of the overdue alert in profile view."""
        company = company_project_mechanism["company"]
        project = company_project_mechanism["project"]
        mechanism = company_project_mechanism["mechanism"]

        # Create company membership
        membership = CompanyMembership.objects.create(
            user=regular_user, company=company, role="manager"
        )

        # Create two overdue obligations
        for i in range(2):
            Obligation.objects.create(
                obligation_number=f"OBL00{i + 3}",
                obligation=f"Test Overdue {i + 1}",
                status="not_started",
                primary_environmental_mechanism=mechanism,
                project=project,
                action_due_date=timezone.now().date() - timedelta(days=1),
                responsibility=membership.role,
            )

        # Add user to project
        project.members.add(regular_user)

        # Make the client authenticated as the regular_user
        authenticated_client.force_login(regular_user)

        # Request the profile page
        url = reverse("users:profile")
        response = authenticated_client.get(url)

        # Check HTML structure
        content = response.content.decode("utf-8")

        # Verify the overdue alert HTML structure
        assert "alert-warning overdue-alert" in content
        assert "You have <strong>2</strong> overdue compliance items" in content
        assert '<a href="' in content and "View all" in content

        # Verify the placement in the document - after profile header, before contact
        assert (
            content.find("<h2>Profile</h2>")
            < content.find("overdue-alert")
            < content.find("contact-info")
        )

    def test_no_overdue_obligations(self, authenticated_client, regular_user, company):
        """Test when user has no overdue obligations."""
        # Create company membership but no overdue obligations
        CompanyMembership.objects.create(
            user=regular_user, company=company, role="manager"
        )

        # Make the client authenticated as the regular_user
        authenticated_client.force_login(regular_user)

        # Request the profile page
        url = reverse("users:profile")
        response = authenticated_client.get(url)

        # Verify context contains profile and overdue_count as 0
        assert "profile" in response.context
        assert "overdue_count" in response.context
        assert response.context["overdue_count"] == 0

        # Verify no overdue alert is shown
        content = response.content.decode("utf-8")
        assert "overdue compliance items" not in content

    def test_no_company_membership(self, authenticated_client, regular_user):
        """Test when user has no company memberships."""
        # Delete any company memberships to ensure clean test
        CompanyMembership.objects.filter(user=regular_user).delete()

        # Make the client authenticated as the regular_user
        authenticated_client.force_login(regular_user)

        # Request the profile page
        url = reverse("users:profile")
        response = authenticated_client.get(url)

        # Verify context contains profile and overdue_count as 0
        assert "profile" in response.context
        assert "overdue_count" in response.context
        assert response.context["overdue_count"] == 0

    def test_profile_image_accessbility(self, authenticated_client, regular_user):
        """Test the profile image accessibility in the template."""
        # Make the client authenticated as the regular_user
        authenticated_client.force_login(regular_user)

        # Request the profile partial directly via HTMX to get just the partial content
        url = reverse("users:profile")
        response = authenticated_client.get(
            url,
            HTTP_HX_REQUEST="true",  # Simulate HTMX request to get partial
        )

        # Check the response status
        assert response.status_code == HTTP_OK

        # Check that the image does not have hardcoded dimensions
        content = response.content.decode("utf-8")
        assert 'height="150"' not in content
        assert 'width="150"' not in content

        # For users with no profile image, check for the profile-initial div
        if "<img" in content:
            # If image is present, check for alt text
            assert (
                'alt="Profile picture"' in content
                or 'alt="profile picture"' in content.lower()
            )
        else:
            # Otherwise check for profile initial
            assert '<div class="profile-initial"' in content
