import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from moneybook.models import Data


class DeleteView(View):
    def post(self, request, *args, **kwargs):
        pk = request.POST.get("pk")

        try:
            Data.get(pk).delete()
        except:
            res = {"message": "Data does not exist"}
            return HttpResponseBadRequest(json.dumps(res))

        return HttpResponse()
