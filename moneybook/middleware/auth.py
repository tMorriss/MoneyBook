from django.http import HttpResponseRedirect
from django.urls import reverse


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path != reverse('moneybook:login'):
            return HttpResponseRedirect(reverse('moneybook:login'))

        return self.get_response(request)
