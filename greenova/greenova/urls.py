from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from typing import List, Union
from django.urls.resolvers import URLPattern, URLResolver

urlpatterns: List[Union[URLPattern, URLResolver]] = [
    path('admin/', admin.site.urls),
    path('', include(('landing.urls', 'landing'))),
    path('auth/', include(('authentication.urls', 'authentication'))),
    path('dashboard/', include(('dashboard.urls', 'dashboard'))),
    path('analytics/', include(('analytics.urls', 'analytics'))),
    path('projects/', include(('projects.urls', 'projects'))),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)