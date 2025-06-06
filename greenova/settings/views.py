from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class SettingsHomeView(LoginRequiredMixin, TemplateView):
    """Minimal settings home view."""
    template_name = "settings/settings_home.html"
