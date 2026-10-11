from http import HTTPStatus

from django.http import HttpResponse
from django.views import View


class HealthView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('ok', content_type='text/plain', status=HTTPStatus.OK)
