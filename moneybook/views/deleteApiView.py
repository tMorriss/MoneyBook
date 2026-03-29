from http import HTTPStatus

from django.http import JsonResponse
from django.views import View
from moneybook.models import Data


class DeleteApiView(View):
    def post(self, request, *args, **kwargs):
        pk = request.POST.get('pk')

        try:
            Data.get(pk).delete()
        except:
            res = {'message': 'Data does not exist'}
            return JsonResponse(res, status=HTTPStatus.BAD_REQUEST)

        return JsonResponse({})
