from typing import Any, Dict
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Project, Obligation

class ProjectListView(LoginRequiredMixin, ListView):
    """Displays a list of all projects accessible to the current user."""
    model = Project
    template_name = 'projects/list.html'
    context_object_name = 'projects'

class ProjectDetailView(LoginRequiredMixin, DetailView):
    """Displays a project's details, including related obligations."""
    model = Project
    template_name = 'projects/detail.html'
    context_object_name = 'project'
    object: Project

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context['obligations'] = Obligation.objects.filter(project=project)
        return context