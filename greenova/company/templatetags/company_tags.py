from company.models import Company, CompanyMembership
from django import template
from django.utils.html import format_html
from beartype import beartype

register = template.Library()


@register.filter
@beartype
def company_role(user, company) -> str | None:
    """Return user's role in a company.

    Args:
        user: The user object.
        company: The company object or company id.

    Returns:
        The user's role in the company, or None if not found.
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
@beartype
def company_role_badge(role: str) -> str:
    """Return HTML badge for a company role.

    Args:
        role: The role string.

    Returns:
        HTML string for the badge.
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
@beartype
def company_type_label(company_type: str) -> str:
    """Convert company_type code to display label.

    Args:
        company_type: The company type code.

    Returns:
        The display label for the company type.
    """
    for code, label in Company.COMPANY_TYPES:
        if code == company_type:
            return label
    return company_type


@register.filter
@beartype
def industry_label(industry_code: str) -> str:
    """Convert industry code to display label.

    Args:
        industry_code: The industry code.

    Returns:
        The display label for the industry.
    """
    for code, label in Company.INDUSTRY_SECTORS:
        if code == industry_code:
            return label
    return industry_code


@register.simple_tag
@beartype
def company_selector(user) -> str:
    """Render a company selector dropdown.

    Args:
        user: The user object.

    Returns:
        HTML string for the company selector dropdown.
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


@register.simple_tag
@beartype
def company_logo_url(company_settings: dict) -> str:
    """Return the logo URL from company_settings dict, or a default placeholder.

    Args:
        company_settings: Dictionary with company settings.

    Returns:
        The logo URL or a default placeholder.
    """
    return company_settings.get("logo_url") or "/static/img/company-placeholder.png"


@register.simple_tag
@beartype
def company_brand_name(company_settings: dict) -> str:
    """Return the company name from company_settings dict, or 'Company'.

    Args:
        company_settings: Dictionary with company settings.

    Returns:
        The company name or 'Company'.
    """
    return company_settings.get("name") or "Company"
