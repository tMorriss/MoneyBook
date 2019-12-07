from django.conf import settings
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from datetime import datetime
from moneybook.models import *
from moneybook.forms import *
import json

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
            'first_genres': Genre.first_list(),
            'latter_genres': Genre.latter_list(),
            'temps': {0: "No", 1: "Yes"},
        }
        return render(request, 'add.html', content)

    def post(self, request, *args, **kwargs):
        newData = DataForm(request.POST)
        if newData.is_valid():
            # データ追加
            newData.save()

            resData = {
                "status": "success",
            }
            return HttpResponse(json.dumps(resData))

        else:
            errorList = []
            for a in newData.errors:
                errorList.append(a)
            resData = {
                "ErrorList": errorList,
            }
            return HttpResponseBadRequest(json.dumps(resData))