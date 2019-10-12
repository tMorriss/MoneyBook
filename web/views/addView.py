from django.conf import settings
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseBadRequest
from datetime import datetime
from web.models import *
from web.forms import *
import json

class AddView(View):
    def get(self, request, *args, **kwargs):
        now = datetime.now()
        content = {
            'app_name': settings.APP_NAME,
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

            year = request.POST.get('year')
            month = request.POST.get('month')
            
            # 今月のデータ
            monthlyData = Data.sortDateDescending(Data.getMonthData(int(year), int(month)))

            content = {
                'app_name': settings.APP_NAME,
                'monthly_data': monthlyData,
            }

            # 追加後のmonthlyテーブルを返す
            return render(request, '_monthly_table.html', content)

        else:
            resData = {}
            errorList = []
            for a in newData.errors:
                errorList.append(a)
            resData["ErrorList"] = errorList
            return HttpResponseBadRequest(json.dumps(resData))