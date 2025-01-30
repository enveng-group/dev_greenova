from audit.views import audit_log_view
from dashboard.views import dashboard_view, logout_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from landing.views import index
from login.views import login_view, password_reset_request, register_view
from users.views import change_password, edit_profile, user_profile
from obligations import views as obligation_views
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Landing
    path("", index, name="index"),
    # Authentication
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("accounts/", include("django.contrib.auth.urls")),
    # Dashboard
    path("dashboard/", dashboard_view, name="dashboard"),
    # Password Management
    path("password-reset/", password_reset_request, name="password_reset"),
    # User Profile
    path("profile/", user_profile, name="user_profile"),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path("profile/password/", change_password, name="change_password"),
    # Audit
    path("audit/", audit_log_view, name="audit_log"),
    # Obligations
    path("obligations/", obligation_views.obligation_list, name="obligations_list"),
    path("obligations/create/", obligation_views.obligation_create, name="obligations_create"),
    path("obligations/<str:pk>/", obligation_views.obligation_detail, name="obligations_detail"),
    path("obligations/<str:pk>/edit/", obligation_views.obligation_update, name="obligations_update"),
    path("obligations/<str:pk>/delete/", obligation_views.obligation_delete, name="obligations_delete"),
    path("obligations/overdue/", obligation_views.obligation_list, {"due_range": "overdue"}, name="obligations_overdue"),
    path("obligations/next-7-days/", obligation_views.obligation_list, {"due_range": "7days"}, name="obligations_next_7_days"),
    path("obligations/next-14-days/", obligation_views.obligation_list, {"due_range": "14days"}, name="obligations_next_14_days"),
    path("obligations/next-month/", obligation_views.obligation_list, {"due_range": "month"}, name="obligations_next_month"),
]
+ debug_toolbar_urls()
+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)