from django.utils.deprecation import MiddlewareMixin
from django.contrib.contenttypes.models import ContentType
from .models import AuditLog

class AuditMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            if request.method in ['POST', 'PUT', 'DELETE']:
                AuditLog.objects.create(
                    user=request.user,
                    action='UPDATE',
                    ip_address=self.get_client_ip(request),
                    details={
                        'method': request.method,
                        'path': request.path,
                    }
                )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')