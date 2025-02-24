from typing import Dict, Any, cast, TypeVar, List, Sequence
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from .models import Project
import logging
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from obligations.models import Obligation

User = get_user_model()
logger = logging.getLogger(__name__)

T = TypeVar('T')

class ProjectSelectionView(LoginRequiredMixin, TemplateView):
    """Handle project selection."""
    template_name = 'projects/projects_selector.html'
