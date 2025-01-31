from django.apps import AppConfig

class LoginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'login'

    def ready(self):
        from django.conf import settings
        settings.LOGIN_URL = 'login'
        settings.LOGIN_REDIRECT_URL = 'dashboard'
        settings.LOGOUT_REDIRECT_URL = 'index'
