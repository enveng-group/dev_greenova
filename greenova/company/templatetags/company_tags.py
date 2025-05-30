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

"""Custom template tags for the company app in Greenova.

This module defines custom Django template tags for the company app.
"""


from django import template
from typing import Any
from greenova.company.models import Company, CompanyMembership
from django.utils.html import format_html


register = template.Library()


@register.filter
def company_role(user: Any, company: Any) -> str:
    """Return user's role in a company.

    Returns:
        The user's role as a string, or None if not found.

    """
    try:
        if isinstance(company, int):
            membership = CompanyMembership.objects.get(user=user, company_id=company)
        else:
            membership = CompanyMembership.objects.get(user=user, company=company)
        return membership.role
    except CompanyMembership.DoesNotExist:
        return None


@register.filter
def company_role_badge(role: Any) -> str:
    """Return HTML badge for a company role.

    Returns:
        An HTML string representing the badge for the given role.

    """
    badge_mapping = {
        "owner": '<mark role="status" class="info">Owner</mark>',
        "admin": '<mark role="status" class="info">Admin</mark>',
        "manager": '<mark role="status" class="info">Manager</mark>',
        "client_contact": '<mark role="status">Client Contact</mark>',
        "contractor": '<mark role="status">Contractor</mark>',
        "view_only": '<mark role="status">View Only</mark>',
    }
    badge_html = badge_mapping.get(role, f'<mark role="status">{role}</mark>')
    return format_html(badge_html)


@register.filter
def company_type_label(company_type: Any) -> str:
    """Convert company_type code to display label.

    Returns:
        The display label for the company type as a string.

    """
    for code, label in Company.COMPANY_TYPES:
        if code == company_type:
            return label
    return company_type


@register.filter
def industry_label(industry_code: Any) -> str:
    """Convert industry code to display label.

    Returns:
        The display label for the industry code as a string.

    """
    for code, label in Company.INDUSTRY_SECTORS:
        if code == industry_code:
            return label
    return industry_code


@register.simple_tag
def company_selector(user: Any) -> str:
    """Render a company selector dropdown.

    Returns:
        An HTML string for the company selector dropdown.

    """
    companies = Company.objects.filter(members=user).order_by("name")

    if not companies:
        return format_html(
            '<div class="no-companies">You are not associated with any companies</div>',
        )

    output = ['<select name="company" id="company-selector" class="company-selector">']

    for company in companies:
        try:
            membership = CompanyMembership.objects.get(user=user, company=company)
            is_primary = membership.is_primary
            role = membership.role
        except CompanyMembership.DoesNotExist:
            is_primary = False
            role = "Unknown"

        output.append(
            format_html(
                '<option value="{}" {}>{name} ({role})</option>',
                company.id,
                'selected="selected"' if is_primary else "",
                name=company.name,
                role=role,
            ),
        )

    output.append("</select>")
    return format_html("".join(output))
