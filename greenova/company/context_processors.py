"""Custom context processors for the company app.

Provides company info (name, logo, settings) for templates.

Returns:
    dict: Context variables for templates.
"""
from typing import Any, Dict
from beartype import beartype
from django.contrib.auth import get_user_model
from .models import Company, CompanyMembership

@beartype
def company_context(request) -> Dict[str, Any]:
    """Inject company-related context variables into templates.

    Args:
        request: The current HttpRequest object.

    Returns:
        A dictionary of company-related context variables, including:
            - current_company: The user's primary company or None.
            - company_settings: Branding/settings dict for the current company.
    """
    user = getattr(request, "user", None)
    current_company = None
    if user and user.is_authenticated:
        membership = (
            CompanyMembership.objects.filter(user=user, is_primary=True)
            .select_related("company")
            .first()
        )
        if membership:
            current_company = membership.company
    # Fallback: try to get from session if not found
    if not current_company:
        company_id = request.session.get("current_company_id")
        if company_id:
            current_company = Company.objects.filter(id=company_id).first()
    company_settings = {}
    if current_company:
        company_settings = {
            "name": current_company.name,
            "logo_url": current_company.logo.url if current_company.logo else None,
            "description": current_company.description,
            "website": current_company.website,
            "industry": current_company.industry,
            "size": current_company.size,
            "is_active": current_company.is_active,
        }
    return {
        "current_company": current_company,
        "company_settings": company_settings,
    }
