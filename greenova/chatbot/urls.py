from django.urls import path

from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chatbot_home, name='chatbot_home'),
    path('conversation/new/', views.create_conversation, name='create_conversation'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('conversation/<int:conversation_id>/send/', views.send_message, name='send_message'),
    path('conversation/<int:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),
]
