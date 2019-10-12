from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render
from django.views import View
from web.models import *
from web.forms import *
import json


class DeleteView(View):
    def post(self, request, *args, **kwargs):
        pk = request.POST.get("pk")
        
        try:
            Data.get(pk).delete()
        except:
            res = {"message": "Data does not exist"}
            return HttpResponseNotFound(json.dumps(res))
            
        res = {"message": "Success"}
        return HttpResponse(json.dumps(res))