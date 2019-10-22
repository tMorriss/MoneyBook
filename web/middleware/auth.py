from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse

class authMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if not request.user.is_authenticated and request.path != reverse('web:login'):
            return HttpResponseRedirect(reverse('web:login'))
        return response