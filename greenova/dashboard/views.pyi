from typing import Any

from beartype import beartype
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

class DashboardIndexView(LoginRequiredMixin, TemplateView):
    template_name: str
    @beartype
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]: ...
