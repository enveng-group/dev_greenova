from django import template
from django.utils.html import format_html
from django.contrib.auth.models import User
from ..models import CompanyMembership, Company

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
    if role == 'owner':
        return format_html('<mark role="status" class="info">Owner</mark>')
    elif role == 'admin':
        return format_html('<mark role="status" class="info">Admin</mark>')
    elif role == 'manager':
        return format_html('<mark role="status" class="info">Manager</mark>')
    elif role == 'member':
        return format_html('<mark role="status">Member</mark>')
    elif role == 'client_contact':
        return format_html('<mark role="status">Client Contact</mark>')
    elif role == 'contractor':
        return format_html('<mark role="status">Contractor</mark>')
    elif role == 'view_only':
        return format_html('<mark role="status">View Only</mark>')
    return format_html('<mark role="status">{}</mark>', role)


@register.filter
def primary_company(user):
    """Return user's primary company."""
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
        return format_html('<div class="no-companies">You are not associated with any companies</div>')

    output = ['<select name="company" id="company-selector" class="company-selector">']

    for company in companies:
        try:
            membership = CompanyMembership.objects.get(user=user, company=company)
            is_primary = membership.is_primary
            role = membership.role
        except CompanyMembership.DoesNotExist:
            is_primary = False
            role = 'Unknown'

        selected = 'selected' if is_primary else ''
        output.append(f'<option value="{company.id}" {selected}>{company.name} ({role})</option>')

    output.append('</select>')
    return format_html(''.join(output))
