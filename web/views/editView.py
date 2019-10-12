from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views import View
from web.models import *
from web.forms import *
import json

class EditView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]

        try:
            data = Data.get(pk)
        except:
            return redirect('web:index')

        content = {
            'app_name': settings.APP_NAME,
            'data': data,
            'directions': Direction.list(),
            'methods': Method.list(),
            'first_genres': Genre.first_list(),
            'latter_genres': Genre.latter_list(),
            'temps': {0:"No", 1:"Yes"},
            'checked': {0: "No", 1: "Yes"},
        }
        return render(request, "web/edit.html", content)

    def post(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        
        try:
            data = Data.get(pk)
        except:
            res = {"message": "Data does not exist"}
            return HttpResponseNotFound(json.dumps(res))

        newData = DataForm(request.POST)
        if newData.is_valid():
            # データ更新
            data.date = request.POST.get("date")
            data.item = request.POST.get("item")
            data.price = request.POST.get("price")
            data.directions = Direction.get(request.POST.get("direction"))
            data.method = Method.get(request.POST.get("method"))
            data.genre = Genre.get(request.POST.get("genre"))
            data.temp = request.POST.get("temp")
            data.checked = request.POST.get("checked")
            data.save()

            res = {"message": "success"}
            return HttpResponse(json.dumps(res))
        else:
            resData = {}
            errorList = []
            for a in newData.errors:
                errorList.append(a)
            resData["ErrorList"] = errorList
            return HttpResponseBadRequest(json.dumps(resData))
