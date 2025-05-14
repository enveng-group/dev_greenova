"""Tests for the Company and CompanyMembership models and related views.

This module contains unit tests for creating, updating, deleting, and listing
companies, as well as managing company memberships. All tests use Django's
TestCase and pytest fixtures.
"""

# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

import pytest
from company.models import Company, CompanyMembership
from django.urls import reverse
from users.models import User

# HTTP status code constants
HTTP_OK = 200
HTTP_FOUND = 302  # Redirect after successful POST


@pytest.mark.django_db
def test_company_creation(authenticated_client, regular_user):
    """Test creating a new company."""
    # Make the user a company admin by creating a company and making them an admin
    initial_company = Company.objects.create(name="Initial Company")
    CompanyMembership.objects.create(
        company=initial_company, user=regular_user, role="admin", is_primary=True
    )

    url = reverse("company:create")
    data = {
        "name": "New Company",
        "description": "A newly created company",
        "company_type": "client",
        "industry": "consulting",  # Updated to use a valid industry choice
        "is_active": True,
    }
    response = authenticated_client.post(url, data)

    # Print response content if status code is HTTP_OK (form errors)
    if response.status_code == HTTP_OK:
        print("Form errors:", response.content.decode())

    assert response.status_code == HTTP_FOUND  # Redirect after successful creation
    assert Company.objects.filter(name="New Company").exists()


@pytest.mark.django_db
def test_company_update(authenticated_client, test_company, regular_user):
    """Test updating an existing company."""
    CompanyMembership.objects.create(
        company=test_company, user=regular_user, role="admin", is_primary=True
    )
    test_company.users.add(regular_user)
    test_company.save()

    url = reverse("company:update", args=[test_company.id])
    data = {
        "name": "Updated Company",
        "description": "Updated description",
        "company_type": "contractor",
        "industry": "consulting",
        "is_active": False,
        # Add all other possible fields to ensure form validation
        "website": "https://example.com",
        "phone": "123-456-7890",
        "email": "info@example.com",
        "address": "123 Main St",
        "size": "medium",
    }
    response = authenticated_client.post(url, data)

    # Debug output
    if response.status_code != HTTP_FOUND:
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.content.decode()}")

    assert response.status_code == HTTP_FOUND
    test_company.refresh_from_db()
    assert test_company.name == "Updated Company"
    assert test_company.description == "Updated description"
    assert test_company.company_type == "contractor"
    assert test_company.industry == "consulting"
    assert not test_company.is_active


@pytest.mark.django_db
def test_company_delete(authenticated_client, test_company, regular_user):
    """Test deleting a company."""
    # Make the user an owner of the company (only owners can delete companies)
    test_company.users.add(regular_user)
    CompanyMembership.objects.create(
        company=test_company,
        user=regular_user,
        role="owner",  # Must be owner to delete
        is_primary=True,
    )

    url = reverse("company:delete", args=[test_company.id])
    response = authenticated_client.post(url)

    # Debug output
    if response.status_code != HTTP_FOUND:
        print(f"Delete response status: {response.status_code}")
        print(f"Delete response content: {response.content.decode()}")

    assert response.status_code == HTTP_FOUND
    assert not Company.objects.filter(id=test_company.id).exists()


@pytest.mark.django_db
def test_company_list_view(authenticated_client, test_company, regular_user):
    """Test the company list view."""
    # Associate the user with the company to grant access
    test_company.users.add(regular_user)
    CompanyMembership.objects.create(
        company=test_company, user=regular_user, role="member", is_primary=True
    )

    url = reverse("company:list")
    response = authenticated_client.get(url)
    assert response.status_code == HTTP_OK
    assert test_company.name in response.content.decode()


@pytest.mark.django_db
def test_company_membership_creation(authenticated_client, test_company, regular_user):
    """Test adding a user to a company."""
    # First make the regular user an admin of the company
    # (to have permission to add members)
    test_company.users.add(regular_user)
    CompanyMembership.objects.create(
        company=test_company,
        user=regular_user,
        role="admin",  # Admin role needed to add other users
        is_primary=True,
    )

    # Create a new user to add to the company
    new_user = User.objects.create_user(
        username="newuser", password="password123", email="newuser@example.com"
    )

    url = reverse("company:add_member", args=[test_company.id])
    data = {
        "user": new_user.id,
        "role": "manager",
        "department": "Engineering",
        "position": "Lead Engineer",
        "is_primary": True,
    }
    response = authenticated_client.post(url, data)
    assert response.status_code == HTTP_OK  # HTMX response is 200 OK, not 302
    assert CompanyMembership.objects.filter(
        company=test_company, user=new_user
    ).exists()


@pytest.mark.django_db
def test_company_membership_removal(authenticated_client, test_company, regular_user):
    """Test removing a user from a company."""
    # First make the regular user an admin of the company
    # (to have permission to remove members)
    test_company.users.add(regular_user)
    CompanyMembership.objects.create(
        company=test_company,
        user=regular_user,
        role="admin",  # Admin role needed to remove users
        is_primary=True,
    )

    # Create a new user to remove from the company
    new_user = User.objects.create_user(
        username="removeme", password="password123", email="removeme@example.com"
    )

    # Add the new user to the company
    test_company.users.add(new_user)
    membership = CompanyMembership.objects.create(
        company=test_company, user=new_user, role="manager"
    )

    url = reverse("company:remove_member", args=[test_company.id, membership.id])
    response = authenticated_client.post(url)

    # Debug output
    if response.status_code != HTTP_OK:  # HTMX response is 200 OK, not 302
        print(f"Remove member response status: {response.status_code}")
        print(f"Remove member response content: {response.content.decode()}")

    assert response.status_code == HTTP_OK  # HTMX response is 200 OK
    assert not CompanyMembership.objects.filter(id=membership.id).exists()
