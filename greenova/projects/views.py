from typing import Dict, Any, cast
from django.db.models import QuerySet
from django.views.generic import ListView, DetailView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models import Count
from .models import Project, ProjectMembership, ProjectRole
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

class ProjectListView(LoginRequiredMixin, ListView):
    """Display list of all projects."""
    model = Project
    template_name = 'projects/views/list.html'
    context_object_name = 'projects'
    
    def get_queryset(self) -> QuerySet[Project]:
        """Get projects for current user with obligations prefetched."""
        return (Project.objects
                .filter(memberships__user=cast(AbstractUser, self.request.user))
                .prefetch_related('obligations')
                .distinct())

class ProjectDetailView(LoginRequiredMixin, DetailView):
    """Display detailed view of a project."""
    model = Project
    template_name = 'projects/views/detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Add project obligations to context."""
        context = super().get_context_data(**kwargs)
        project = cast(Project, self.get_object())
        context['obligations'] = project.obligations.all()
        return context

class ProjectSelectionView(LoginRequiredMixin, TemplateView):
    """Handle project selection."""
    template_name = 'projects/partials/select.html'

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Get context data for project selection."""
        context = super().get_context_data(**kwargs)
        
        try:
            user = cast(AbstractUser, self.request.user)
            logger.info(f"Getting projects for user ID: {user.pk}")
            
            # Get projects with efficient querying
            projects = (Project.objects
                      .filter(memberships__user=user)
                      .prefetch_related('memberships', 'obligations')
                      .distinct())
            
            # Get user roles for each project
            user_roles: Dict[int, str] = {}
            for project in projects:
                try:
                    membership = project.memberships.get(user=user)
                    user_roles[project.id] = membership.role
                except ProjectMembership.DoesNotExist:
                    continue
            
            context.update({
                'projects': projects,
                'user_roles': user_roles,
                'selected_project_id': self.request.GET.get('project_id'),
                'debug': settings.DEBUG
            })
            
        except Exception as e:
            logger.error(f"Error in project selection: {str(e)}")
            context['error'] = 'Unable to load projects'
            
        return context

class ProjectContentView(LoginRequiredMixin, View):
    """Handle HTMX requests for project content."""
    
    def get(self, request: HttpRequest, project_id: int) -> HttpResponse:
        """Handle GET requests for project content."""
        try:
            project = get_object_or_404(Project, id=project_id)
            user = cast(AbstractUser, request.user)
            
            # Check if user has access
            try:
                membership = project.memberships.get(user=user)
            except ProjectMembership.DoesNotExist:
                logger.warning(f"User {user.pk} attempted to access unauthorized project {project_id}")
                return HttpResponseForbidden("You don't have access to this project")
            
            # Get project data
            mechanisms = (project.obligations
                        .values('primary_environmental_mechanism')
                        .annotate(count=Count('id'))
                        .order_by('primary_environmental_mechanism'))
            
            context = {
                'project': project,
                'mechanisms': mechanisms,
                'obligations': project.obligations.all(),
                'user_role': membership.role
            }
            
            return TemplateResponse(
                request,
                'projects/partials/project_content.html',
                context
            )
            
        except Exception as e:
            logger.error(f"Error loading project content: {str(e)}")
            return HttpResponse(
                status=500,
                content="Error loading project content"
            )