import json

from django.conf import settings
from django.http import (HttpResponse, HttpResponseBadRequest)
from django.shortcuts import redirect, render
from django.views import View
from moneybook.forms import DataForm
from moneybook.models import Category, Data, Direction, Method


class EditView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]

        try:
            data = Data.get(pk)
        except:
            return redirect('moneybook:index')

        context = {
            'app_name': settings.APP_NAME,
            'username': request.user,
            'data': data,
            'directions': Direction.list(),
            'methods': Method.list(),
            'first_categories': Category.first_list(),
            'latter_categories': Category.latter_list(),
            'temps': {0: "No", 1: "Yes"},
            'checked': {0: "No", 1: "Yes"},
        }
        return render(request, "edit.html", context)

    def post(self, request, *args, **kwargs):
        pk = kwargs["pk"]

        try:
            data = Data.get(pk)
        except:
            return HttpResponseBadRequest(
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
            data.category = Category.get(request.POST.get("category"))
            data.temp = request.POST.get("temp")
            data.checked = request.POST.get("checked")
            data.save()

            return HttpResponse()
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
            return HttpResponseBadRequest(json.dumps(res))

        data.checked = True
        data.save()
        return HttpResponse()
