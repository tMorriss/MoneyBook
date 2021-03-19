from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if not request.user.is_authenticated and request.path != reverse('moneybook:login'):
            return HttpResponseRedirect(reverse('moneybook:login'))
        return response
