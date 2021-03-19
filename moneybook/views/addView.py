import json
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views import View
from moneybook.forms import DataForm
from moneybook.models import Category, Direction, Method


class AddView(View):
    def get(self, request, *args, **kwargs):
        now = datetime.now()
        content = {
            'app_name': settings.APP_NAME,
            'username': request.user,
            'year': now.year,
            'month': now.month,
            'directions': Direction.list(),
            'methods': Method.list(),
            'chargeable_methods': Method.chargeable_list(),
            'first_categories': Category.first_list(),
            'latter_categories': Category.latter_list(),
            'temps': {0: "No", 1: "Yes"},
        }
        return render(request, 'add.html', content)

    def post(self, request, *args, **kwargs):
        new_data = DataForm(request.POST)
        if new_data.is_valid():
            # データ追加
            new_data.save()

            res_data = {
                "status": "success",
            }
            return HttpResponse(json.dumps(res_data))

        else:
            error_list = []
            for a in new_data.errors:
                error_list.append(a)
            res_data = {
                "ErrorList": error_list,
            }
            return HttpResponseBadRequest(json.dumps(res_data))
