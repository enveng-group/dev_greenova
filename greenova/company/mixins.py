from django.core.exceptions import PermissionDenied

from .models import CompanyMembership


class CompanyAccessMixin:
    """
    Mixin to ensure users can only access data for companies they belong to.

    This mixin handles both direct company membership and active_company.
    """

    def dispatch(self, request, *args, **kwargs):
        """Check if user has permission to access this view."""
        # Superusers always have access
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # First check if the user is a member of any company (for list views)
        if request.user.companies.exists():
            return super().dispatch(request, *args, **kwargs)

        # Otherwise check specific company access (for detail/edit views)
        company_id = kwargs.get("company_id")
        if company_id:
            try:
                # Check if user has direct membership
                CompanyMembership.objects.get(company_id=company_id, user=request.user)
                return super().dispatch(request, *args, **kwargs)
            except CompanyMembership.DoesNotExist:
                pass

        # Finally, check active company from session
        company = getattr(request, "active_company", None)
        if company and company.users.filter(id=request.user.id).exists():
            return super().dispatch(request, *args, **kwargs)

        # No access granted
        raise PermissionDenied("You do not have access to this company.")
