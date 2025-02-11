from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Admin interface
    path("admin/", admin.site.urls),
    # Authentication and user management
    path("accounts/", include("accounts.urls", namespace="accounts")),
    # Core functionality
    path("core/", include("core.urls", namespace="core")),
    # Obligations
    path("obligations/", include("obligations.urls", namespace="obligations")),
    # Main dashboard
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
    # Environmental services
    path("services/", include("services.urls", namespace="services")),
    # Landing pages (root URLs)
    path("", include("landing.urls", namespace="landing")),
]

# Error handlers
handler400 = "greenova.views.bad_request"
handler403 = "greenova.views.permission_denied"
handler404 = "greenova.views.not_found"
handler500 = "greenova.views.server_error"

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
