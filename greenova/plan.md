# Plan

## File Structure

```plaintext
.
├── analytics
│   ├── admin.py
│   ├── apps.py
│   ├── chart_data_utils.py
│   ├── data_processors_utils.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── templates
│   │   └── analytics
│   │       ├── aspect_details.html
│   │       ├── base_analytics.html
│   │       ├── mechanism_status.html
│   │       └── performance_metrics.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── authentication
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       └── __init__.cpython-313.pyc
│   ├── models.py
│   ├── __pycache__
│   │   ├── admin.cpython-313.pyc
│   │   ├── apps.cpython-313.pyc
│   │   ├── __init__.cpython-313.pyc
│   │   ├── models.cpython-313.pyc
│   │   ├── urls.cpython-313.pyc
│   │   └── views.cpython-313.pyc
│   ├── templates
│   │   └── authentication
│   │       ├── auth_base.html
│   │       ├── login.html
│   │       ├── logout.html
│   │       ├── password_reset_complete.html
│   │       ├── password_reset_confirm.html
│   │       ├── password_reset_done.html
│   │       ├── password_reset.email.html
│   │       ├── password_reset_email.html
│   │       ├── password_reset.html
│   │       ├── password_reset_subject.txt
│   │       └── register.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── dashboard
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── templates
│   │   └── dashboard
│   │       ├── base_dashboard.html
│   │       ├── chart_container.html
│   │       ├── dashboard.html
│   │       ├── obligation_list.html
│   │       └── project_dropdown.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── db.sqlite3
├── greenova
│   ├── asgi.py
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-313.pyc
│   │   ├── settings.cpython-313.pyc
│   │   ├── urls.cpython-313.pyc
│   │   └── wsgi.cpython-313.pyc
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── landing
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       └── __init__.cpython-313.pyc
│   ├── models.py
│   ├── __pycache__
│   │   ├── admin.cpython-313.pyc
│   │   ├── apps.cpython-313.pyc
│   │   ├── __init__.cpython-313.pyc
│   │   ├── models.cpython-313.pyc
│   │   ├── urls.cpython-313.pyc
│   │   └── views.cpython-313.pyc
│   ├── templates
│   │   └── landing
│   │       └── index.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── projects
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── management
│   │   ├── commands
│   │   │   ├── import_obligations.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── templates
│   │   ├── base_projects.html
│   │   ├── detail.html
│   │   ├── list.html
│   │   ├── project_card.html
│   │   └── project_stats.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── static
│   ├── css
│   │   ├── modern-normalize.css
│   │   └── pico.classless.min.css
│   └── js
│       ├── chart.umd.js
│       └── htmx.min.js
├── staticfiles
│   ├── admin
│   │   ├── css
│   │   │   ├── autocomplete.css
│   │   │   ├── base.css
│   │   │   ├── changelists.css
│   │   │   ├── dark_mode.css
│   │   │   ├── dashboard.css
│   │   │   ├── forms.css
│   │   │   ├── login.css
│   │   │   ├── nav_sidebar.css
│   │   │   ├── responsive.css
│   │   │   ├── responsive_rtl.css
│   │   │   ├── rtl.css
│   │   │   ├── unusable_password_field.css
│   │   │   ├── vendor
│   │   │   │   └── select2
│   │   │   │       ├── LICENSE-SELECT2.md
│   │   │   │       ├── select2.css
│   │   │   │       └── select2.min.css
│   │   │   └── widgets.css
│   │   ├── img
│   │   │   ├── calendar-icons.svg
│   │   │   ├── gis
│   │   │   │   ├── move_vertex_off.svg
│   │   │   │   └── move_vertex_on.svg
│   │   │   ├── icon-addlink.svg
│   │   │   ├── icon-alert.svg
│   │   │   ├── icon-calendar.svg
│   │   │   ├── icon-changelink.svg
│   │   │   ├── icon-clock.svg
│   │   │   ├── icon-deletelink.svg
│   │   │   ├── icon-hidelink.svg
│   │   │   ├── icon-no.svg
│   │   │   ├── icon-unknown-alt.svg
│   │   │   ├── icon-unknown.svg
│   │   │   ├── icon-viewlink.svg
│   │   │   ├── icon-yes.svg
│   │   │   ├── inline-delete.svg
│   │   │   ├── LICENSE
│   │   │   ├── README.txt
│   │   │   ├── search.svg
│   │   │   ├── selector-icons.svg
│   │   │   ├── sorting-icons.svg
│   │   │   ├── tooltag-add.svg
│   │   │   └── tooltag-arrowright.svg
│   │   └── js
│   │       ├── actions.js
│   │       ├── admin
│   │       │   ├── DateTimeShortcuts.js
│   │       │   └── RelatedObjectLookups.js
│   │       ├── autocomplete.js
│   │       ├── calendar.js
│   │       ├── cancel.js
│   │       ├── change_form.js
│   │       ├── core.js
│   │       ├── filters.js
│   │       ├── inlines.js
│   │       ├── jquery.init.js
│   │       ├── nav_sidebar.js
│   │       ├── popup_response.js
│   │       ├── prepopulate_init.js
│   │       ├── prepopulate.js
│   │       ├── SelectBox.js
│   │       ├── SelectFilter2.js
│   │       ├── theme.js
│   │       ├── unusable_password_field.js
│   │       ├── urlify.js
│   │       └── vendor
│   │           ├── jquery
│   │           │   ├── jquery.js
│   │           │   ├── jquery.min.js
│   │           │   └── LICENSE.txt
│   │           ├── select2
│   │           │   ├── i18n
│   │           │   │   ├── af.js
│   │           │   │   ├── ar.js
│   │           │   │   ├── az.js
│   │           │   │   ├── bg.js
│   │           │   │   ├── bn.js
│   │           │   │   ├── bs.js
│   │           │   │   ├── ca.js
│   │           │   │   ├── cs.js
│   │           │   │   ├── da.js
│   │           │   │   ├── de.js
│   │           │   │   ├── dsb.js
│   │           │   │   ├── el.js
│   │           │   │   ├── en.js
│   │           │   │   ├── es.js
│   │           │   │   ├── et.js
│   │           │   │   ├── eu.js
│   │           │   │   ├── fa.js
│   │           │   │   ├── fi.js
│   │           │   │   ├── fr.js
│   │           │   │   ├── gl.js
│   │           │   │   ├── he.js
│   │           │   │   ├── hi.js
│   │           │   │   ├── hr.js
│   │           │   │   ├── hsb.js
│   │           │   │   ├── hu.js
│   │           │   │   ├── hy.js
│   │           │   │   ├── id.js
│   │           │   │   ├── is.js
│   │           │   │   ├── it.js
│   │           │   │   ├── ja.js
│   │           │   │   ├── ka.js
│   │           │   │   ├── km.js
│   │           │   │   ├── ko.js
│   │           │   │   ├── lt.js
│   │           │   │   ├── lv.js
│   │           │   │   ├── mk.js
│   │           │   │   ├── ms.js
│   │           │   │   ├── nb.js
│   │           │   │   ├── ne.js
│   │           │   │   ├── nl.js
│   │           │   │   ├── pl.js
│   │           │   │   ├── ps.js
│   │           │   │   ├── pt-BR.js
│   │           │   │   ├── pt.js
│   │           │   │   ├── ro.js
│   │           │   │   ├── ru.js
│   │           │   │   ├── sk.js
│   │           │   │   ├── sl.js
│   │           │   │   ├── sq.js
│   │           │   │   ├── sr-Cyrl.js
│   │           │   │   ├── sr.js
│   │           │   │   ├── sv.js
│   │           │   │   ├── th.js
│   │           │   │   ├── tk.js
│   │           │   │   ├── tr.js
│   │           │   │   ├── uk.js
│   │           │   │   ├── vi.js
│   │           │   │   ├── zh-CN.js
│   │           │   │   └── zh-TW.js
│   │           │   ├── LICENSE.md
│   │           │   ├── select2.full.js
│   │           │   └── select2.full.min.js
│   │           └── xregexp
│   │               ├── LICENSE.txt
│   │               ├── xregexp.js
│   │               └── xregexp.min.js
│   ├── css
│   │   ├── modern-normalize.css
│   │   └── pico.classless.min.css
│   └── js
│       ├── chart.umd.js
│       └── htmx.min.js
└── templates
    └── base.html
```

## Key Models Required
Projects App Models
- Project
  - name
  - description
  - created_at
  - updated_at

- Obligation (from SQL schema)
  - All fields from provided schema
  - ForeignKey to Project
```python
from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Obligation(models.Model):
    obligation_number = models.CharField(max_length=20, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    primary_environmental_mechanism = models.TextField()
    procedure = models.TextField()
    environmental_aspect = models.TextField()
    obligation = models.TextField()
    accountability = models.CharField(max_length=255)
    responsibility = models.CharField(max_length=255)
    project_phase = models.TextField()
    action_due_date = models.DateField()
    close_out_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('not started', 'Not Started'),
            ('in progress', 'In Progress'),
            ('completed', 'Completed')
        ]
    )
```

Dashboard App Models
- UserDashboardPreference
  - user (ForeignKey)
  - default_project (ForeignKey)
  - chart_preferences (JSONField)
```python
from django.db import models
from django.contrib.auth import get_user_model

class UserDashboardPreference(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    default_project = models.ForeignKey('projects.Project', null=True, on_delete=models.SET_NULL)
    chart_preferences = models.JSONField(default=dict)
```

## Required Views

Dashboard Views
- DashboardHomeView
- ProjectSelectorView
- ObligationListView
```python
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        return context

class ProjectSelectorView(LoginRequiredMixin, View):
    def post(self, request):
        # HTMX view to update dashboard based on selected project
        pass

class ObligationListView(LoginRequiredMixin, ListView):
    model = Obligation
    template_name = 'dashboard/components/obligation_list.html'
    context_object_name = 'obligations'
```

Analytics Views
- MechanismStatusChartView
- AspectDetailsChartView
- PerformanceMetricsView
```python
class MechanismStatusChartView(LoginRequiredMixin, View):
    def get(self, request):
        # Return chart data for environmental mechanisms
        pass

class AspectDetailsChartView(LoginRequiredMixin, View):
    def get(self, request):
        # Return chart data for environmental aspects
        pass
```

- ProjectListView
- ProjectDetailView
- ObligationDetailView

## Charts implementation

Chart.js Configuration

```javascript
// Dashboard charts configuration
const mechanismChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ['Not Started', 'In Progress', 'Completed'],
        datasets: [{
            data: [12, 19, 3],
            backgroundColor: [
                '#ff6384',
                '#36a2eb',
                '#4bc0c0'
            ]
        }]
    }
});
```

## URL configuration

```python
# dashboard/urls.py
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardHomeView.as_view(), name='home'),
    path('select-project/', views.ProjectSelectorView.as_view(), name='select_project'),
    path('obligations/', views.ObligationListView.as_view(), name='obligations'),
]
```

```python
# analytics/urls.py
urlpatterns = [
    path('charts/mechanism-status/', views.MechanismStatusChartView.as_view(), name='mechanism_status'),
    path('charts/aspect-details/', views.AspectDetailsChartView.as_view(), name='aspect_details'),
]
```

## Import Command for CSV

- Create custom management command to import CSV data
- Map CSV columns to model fields
- Handle data validation and transformation
- Create relationships between models

```python
from django.core.management.base import BaseCommand
import csv
from projects.models import Project, Obligation

class Command(BaseCommand):
    help = 'Import obligations from CSV file'

    def handle(self, *args, **kwargs):
        with open('clean_output_with_nulls.csv') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Create or update obligations
                Obligation.objects.update_or_create(
                    obligation_number=row['obligation__number'],
                    defaults={
                        'project': Project.objects.get_or_create(
                            name=row['project__name']
                        )[0],
                        'primary_environmental_mechanism': row['primary__environmental__mechanism'],
                        # ... other fields
                    }
                )
```

## Templates

- dashboard/base_dashboard.html
- analytics/base_analytics.html
- projects/base_project.html
- dashboard/home.html
- dashboard/components/project_dropdown.html
- dashboard/components/chart_container.html
- dashboard/components/obligation_list.html
- analytics/charts/mechanism_status.html
- analytics/charts/aspect_details.html
- analytics/charts/performance_metrics.html
- projects/list.html
- projects/detail.html
- projects/obligation_detail.html

## API endpoints
- /api/charts/mechanism-status/
- /api/charts/aspect-details/
- /api/charts/performance-metrics/
- /api/projects/list/
- /api/projects/<id>/obligations/