from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from projects.models import Project, Obligation
import logging

logger = logging.getLogger(__name__)

class DashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all().order_by('name')
        return context

class ProjectSelectorView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/components/project_content.html'  # Updated path
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.request.GET.get('project')
        
        logger.info(f"ProjectSelectorView: Received project_id={project_id}")
        
        if project_id:
            try:
                project = get_object_or_404(Project, id=project_id)
                
                # Get unique mechanisms for this project
                mechanisms = (Obligation.objects
                    .filter(project=project)
                    .values_list('primary_environmental_mechanism', flat=True)
                    .distinct()
                    .order_by('primary_environmental_mechanism'))
                
                # Get all obligations for this project
                obligations = (Obligation.objects
                    .filter(project=project)
                    .order_by('status', 'action_due_date', 'obligation_number'))
                
                context.update({
                    'project': project,
                    'mechanisms': list(mechanisms),
                    'obligations': obligations
                })
                
                logger.info(f"Found project '{project.name}' with {len(mechanisms)} mechanisms")
                
            except Project.DoesNotExist:
                logger.error(f"Project with id={project_id} not found")
            except Exception as e:
                logger.error(f"Error processing project {project_id}: {str(e)}")
                
        return context

class FilteredObligationsView(LoginRequiredMixin, View):
    def get(self, request, project_id):
        mechanism = request.GET.get('mechanism')
        status = request.GET.get('status', '')
        
        project = get_object_or_404(Project, id=project_id)
        obligations = Obligation.objects.filter(project=project)
        
        # Apply filters
        if mechanism:
            obligations = obligations.filter(
                primary_environmental_mechanism=mechanism)
        if status:
            obligations = obligations.filter(status=status)
            
        # Order results
        obligations = obligations.order_by(
            'status', 'action_due_date', 'obligation_number')
        
        return TemplateResponse(request, 'dashboard/obligation_list.html', {
            'obligations': obligations,
            'project': project
        })