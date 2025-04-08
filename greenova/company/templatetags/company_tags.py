from django import template
from django.utils.html import format_html

from ..models import Company, CompanyMembership

register = template.Library()


@register.filter
def company_role(user, company):
    """Return user's role in a company."""
    try:
        if isinstance(company, int):
            membership = CompanyMembership.objects.get(user=user, company_id=company)
        else:
            membership = CompanyMembership.objects.get(user=user, company=company)
        return membership.role
    except CompanyMembership.DoesNotExist:
        return None


@register.filter
def company_role_badge(role):
    """Return HTML badge for a company role."""
    badge_mapping = {
        'owner': '<mark role="status" class="info">Owner</mark>',
        'admin': '<mark role="status" class="info">Admin</mark>',
        'manager': '<mark role="status" class="info">Manager</mark>',
        'client_contact': '<mark role="status">Client Contact</mark>',
        'contractor': '<mark role="status">Contractor</mark>',
        'view_only': '<mark role="status">View Only</mark>',
    }

    badge_html = badge_mapping.get(role, f'<mark role="status">{role}</mark>')
    return format_html(badge_html)
    if role == 'owner':
        return format_html('<mark role="status" class="info">Owner</mark>')
    elif role == 'admin':
        return format_html('<mark role="status" class="info">Admin</mark>')
    try:
        membership = CompanyMembership.objects.get(user=user, is_primary=True)
        return membership.company
    except CompanyMembership.DoesNotExist:
        return None


@register.filter
def company_type_label(company_type):
    """Convert company_type code to display label."""
    for code, label in Company.COMPANY_TYPES:
        if code == company_type:
            return label
    return company_type


@register.filter
def industry_label(industry_code):
    """Convert industry code to display label."""
    for code, label in Company.INDUSTRY_SECTORS:
        if code == industry_code:
            return label
    return industry_code


@register.simple_tag
def company_selector(user):
    """Render a company selector dropdown."""
    companies = Company.objects.filter(members=user).order_by('name')

    if not companies:
        return format_html(
            '<div class="no-companies">You are not associated with any companies</div>'
        )

    output = ['<select name="company" id="company-selector" class="company-selector">']

    for company in companies:
        try:
            membership = CompanyMembership.objects.get(user=user, company=company)
            is_primary = membership.is_primary
            role = membership.role
        except CompanyMembership.DoesNotExist:
            is_primary = False
            role = 'Unknown'

        output.append(
            format_html(
                '<option value="{}" {}>{name} ({role})</option>',
                company.id,
                'selected="selected"' if is_primary else '',
                name=company.name,
                role=role
            )
        )

    output.append('</select>')
    return format_html(''.join(output))
