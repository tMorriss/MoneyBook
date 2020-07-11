from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views import View
from moneybook.models import Direction, Method, Genre, Data
from moneybook.forms import DataForm
import json


class EditView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]

        try:
            data = Data.get(pk)
        except:
            return redirect('moneybook:index')

        content = {
            'app_name': settings.APP_NAME,
            'username': request.user,
            'data': data,
            'directions': Direction.list(),
            'methods': Method.list(),
            'first_genres': Genre.first_list(),
            'latter_genres': Genre.latter_list(),
            'temps': {0: "No", 1: "Yes"},
            'checked': {0: "No", 1: "Yes"},
        }
        return render(request, "edit.html", content)

    def post(self, request, *args, **kwargs):
        pk = kwargs["pk"]

        try:
            data = Data.get(pk)
        except:
            return HttpResponseNotFound(
                json.dumps({"message": "Data does not exist"})
            )

        new_data = DataForm(request.POST)
        if new_data.is_valid():
            # データ更新
            data.date = request.POST.get("date")
            data.item = request.POST.get("item")
            data.price = request.POST.get("price")
            data.direction = Direction.get(request.POST.get("direction"))
            data.method = Method.get(request.POST.get("method"))
            data.genre = Genre.get(request.POST.get("genre"))
            data.temp = request.POST.get("temp")
            data.checked = request.POST.get("checked")
            data.save()

            return HttpResponse(json.dumps({"message": "success"}))
        else:
            res_data = {}
            error_list = []
            for a in new_data.errors:
                error_list.append(a)
            res_data["ErrorList"] = error_list
            return HttpResponseBadRequest(json.dumps(res_data))


class CheckView(View):
    def post(self, request, *args, **kwargs):
        pk = request.POST.get("id")

        try:
            data = Data.get(pk)
        except:
            res = {"message": "Data does not exist"}
            return HttpResponseNotFound(json.dumps(res))

        data.checked = True
        data.save()
        return HttpResponse(json.dumps({"message": "success"}))
