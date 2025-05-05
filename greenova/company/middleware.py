from django.utils.deprecation import MiddlewareMixin

from .models import Company


class ActiveCompanyMiddleware(MiddlewareMixin):
    """
    Middleware that adds the active company to the request context.

    This middleware retrieves the active company ID from the session and
    attaches the corresponding Company instance to the request object as
    `request.active_company`. If no active company is found or the user
    is not authenticated, `request.active_company` will be None.
    """

    def process_request(self, request):
        if request.user.is_authenticated:
            active_company_id = request.session.get('active_company_id')
            if active_company_id:
                try:
                    request.active_company = Company.objects.get(id=active_company_id)
                except Company.DoesNotExist:
                    request.active_company = None
            else:
                request.active_company = None
        else:
            request.active_company = None
