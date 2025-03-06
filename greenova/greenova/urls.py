from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from typing import List, Union
from django.urls.resolvers import URLPattern, URLResolver
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponseRedirect, HttpResponsePermanentRedirect
import logging

logger = logging.getLogger(__name__)

def home_router(request: HttpRequest) -> Union[HttpResponseRedirect, HttpResponsePermanentRedirect]:
    """Route to appropriate home page based on auth status."""
    logger.debug(f"Home router - User authenticated: {request.user.is_authenticated}")

    # If user is not authenticated, always go to landing page
    if not request.user.is_authenticated:
        logger.info("Unauthenticated user - redirecting to landing page")
        return redirect('landing:home')

    # Only redirect to dashboard if authenticated
    logger.info("Authenticated user - redirecting to dashboard")
    return redirect('dashboard:home')

urlpatterns: List[Union[URLPattern, URLResolver]] = [
    # Landing page should be first to take precedence
    path('', home_router, name='home'),
    path('landing/', include('landing.urls')),
    path('admin/', admin.site.urls),

    # Authentication URLs
    path('authentication/', include('authentication.urls')),

    # Protected URLs that require login
    path('dashboard/', include('dashboard.urls')),
    path('projects/', include('projects.urls')),
    path('obligations/', include('obligations.urls')),
    path('chat/', include('chatbot.urls')),
    path('mechanisms/', include('mechanisms.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
