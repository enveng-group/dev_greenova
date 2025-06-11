from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import include, path


def home_router(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        context = {
            "show_landing_content": True,
            "user_authenticated": request.user.is_authenticated,
        }
        return render(request, "landing/index.html", context)
    return redirect("dashboard:home")


def trigger_error(request: HttpRequest) -> HttpResponse:
    _ = 1 / 0
    return HttpResponse("Error triggered")


urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path("", home_router, name="home"),
    path("landing/", include("landing.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.account.urls")),
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
    path("chatbot/", include("chatbot.urls", namespace="chatbot")),
    path("users/", include("users.urls", namespace="users")),
    path("projects/", include("projects.urls")),
    path("obligations/", include("obligations.urls")),
    path("chat/", include("chatbot.urls", namespace="chat")),
    path("mechanisms/", include("mechanisms.urls")),
    path("procedures/", include("procedures.urls")),
    path("company/", include("company.urls", namespace="company")),
    path("responsibility/", include("responsibility.urls")),
    path("feedback/", include("feedback.urls", namespace="feedback")),
    path("reports/", include("reports.urls", namespace="reports")),
    path("sentry-debug/", trigger_error),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
