from django.urls import path
from . import views

app_name = 'obligations'

urlpatterns = [
    path('summary/', views.ObligationSummaryView.as_view(), name='summary'),
    path('create/', views.ObligationCreateView.as_view(), name='create'),
    path('<str:obligation_number>/', views.ObligationDetailView.as_view(), name='detail'),
    path('<str:obligation_number>/update/', views.ObligationUpdateView.as_view(), name='update'),
    path('<str:obligation_number>/delete/', views.ObligationDeleteView.as_view(), name='delete'),
]
