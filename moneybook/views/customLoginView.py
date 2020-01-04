from django.conf import settings
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    extra_context = {
        'app_name': settings.APP_NAME,
    }
    template_name = 'login.html'