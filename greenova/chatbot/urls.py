from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('api/', views.ChatApiView.as_view(), name='api'),
    path('api/legacy/', views.chat_api_legacy, name='api_legacy'),  # Add legacy endpoint
]