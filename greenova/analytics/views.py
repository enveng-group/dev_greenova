from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from projects.models import Obligation  # Import from projects app

class MechanismStatusChartView(LoginRequiredMixin, View):
    def get(self, request):
        mechanism = request.GET.get('mechanism')
        project_id = request.GET.get('project')
        
        query = Obligation.objects.filter(primary_environmental_mechanism=mechanism)
        if project_id:
            query = query.filter(project_id=project_id)
            
        status_counts = (query
            .values('status')
            .annotate(count=Count('status'))
            .order_by('status'))
        
        # Initialize counts for all statuses
        counts = {'not started': 0, 'in progress': 0, 'completed': 0}
        for item in status_counts:
            counts[item['status']] = item['count']
        
        data = {
            'status_counts': [counts['not started'], counts['in progress'], counts['completed']],
            'labels': ['Not Started', 'In Progress', 'Completed']
        }
        
        return JsonResponse(data)

class AspectDetailsView(LoginRequiredMixin, View):
    def get(self, request, obligation_number):
        obligation = Obligation.objects.get(obligation_number=obligation_number)
        
        context = {
            'obligation': obligation,
            'environmental_aspects': Obligation.objects
                .filter(project=obligation.project)
                .values('environmental_aspect')
                .annotate(count=Count('environmental_aspect'))
        }
        
        return JsonResponse(context)