from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('api/', views.ChatApiView.as_view(), name='api'),
    path('toggle/', views.ChatToggleView.as_view(), name='toggle'),  # Add toggle endpoint
    path('messages/', views.ChatApiView.as_view(), name='messages'),  # Add messages endpoint
    path('api/legacy/', views.chat_api_legacy, name='api_legacy'),
]