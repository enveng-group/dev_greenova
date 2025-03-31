from django.urls import path
<<<<<<< HEAD

=======
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
from . import views

app_name = 'responsibility'

urlpatterns = [
<<<<<<< HEAD
    path('chart/', views.ResponsibilityChartView.as_view(), name='responsibility_chart'),
    path('api/options/', views.get_responsibility_options, name='responsibility_options'),
=======
    # Basic URLs - to be expanded later with actual views
    path('', views.responsibility_home, name='home'),
    path('assignments/', views.assignment_list, name='assignment_list'),
    path('roles/', views.role_list, name='role_list'),
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
]
