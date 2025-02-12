from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('landing.urls', 'landing'))),
    path('auth/', include(('authentication.urls', 'authentication'))),
    path('dashboard/', include('dashboard.urls')),
    path('analytics/', include('analytics.urls')),
    path('projects/', include('projects.urls')),
]