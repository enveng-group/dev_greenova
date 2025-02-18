from typing import Any, Dict
import logging
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.db.models import Count
from .models import Project

logger = logging.getLogger(__name__)

class ProjectListView(LoginRequiredMixin, ListView):
    """Display list of all projects."""
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/views/list.html'
    paginate_by = 10

    def get_queryset(self):
        return Project.objects.annotate(obligation_count=Count('obligations'))

class ProjectDetailView(LoginRequiredMixin, DetailView):
    """Display detailed view of a project."""
    model = Project
    context_object_name = 'project'
    template_name = 'projects/views/detail.html'

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Add additional context data for project details."""
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        
        try:
            context.update({
                'obligations': project.obligations.all(),
                'mechanisms': project.obligations.values_list(
                    'primary_environmental_mechanism', 
                    flat=True
                ).distinct(),
            })
            logger.info(f"Retrieved project details for {project.name}")
        except Exception as e:
            logger.error(f"Error getting project details: {str(e)}")
            context['error'] = "Unable to load project details"
            
        return context

class ProjectSelectionView(LoginRequiredMixin, View):
    """Handle project selection via HTMX requests."""
    template_name = 'projects/sections/project_selection.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        """Handle GET requests for project selection."""
        try:
            project_id = request.GET.get('project_id')
            if project_id:
                project = get_object_or_404(Project, id=project_id)
                context = {
                    'project': project,
                    'obligations': project.obligations.all()
                }
                html = render_to_string(
                    'projects/views/projects.html',
                    context,
                    request=request
                )
                return HttpResponse(html)
            
            projects = Project.objects.all()
            return render(request, self.template_name, {'projects': projects})
            
        except Exception as e:
            logger.error(f"Error in project selection: {str(e)}")
            return JsonResponse(
                {'error': 'Unable to load project'}, 
                status=400
            )

class ProjectContentView(LoginRequiredMixin, View):
    """Handle HTMX requests for project content updates."""
    def get(self, request: HttpRequest, project_id: int) -> HttpResponse:
        try:
            project = get_object_or_404(Project, id=project_id)
            context = {
                'project': project,
                'obligations': project.obligations.all()
            }
            return render(request, 'projects/views/projects.html', context)
        except Exception as e:
            logger.error(f"Error loading project content: {str(e)}")
            return JsonResponse(
                {'error': 'Unable to load project content'}, 
                status=400
            )