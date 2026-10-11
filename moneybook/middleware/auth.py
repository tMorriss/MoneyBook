from http import HTTPStatus

from django.http import HttpResponseRedirect, JsonResponse
from django.urls import resolve, Resolver404, reverse

AUTH_EXEMPT_VIEW_NAMES = ['moneybook:login', 'moneybook:health']


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            try:
                view_name = resolve(request.path_info).view_name
            except Resolver404:
                view_name = None

            if view_name not in AUTH_EXEMPT_VIEW_NAMES:
                if request.path.startswith('/api/'):
                    return JsonResponse({'message': 'login is required'}, status=HTTPStatus.FORBIDDEN)
                return HttpResponseRedirect(reverse('moneybook:login'))

        return self.get_response(request)
