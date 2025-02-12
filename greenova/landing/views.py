from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'landing/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Welcome to Greenova',
            'description': 'Environmental Management System',
        })
        return context