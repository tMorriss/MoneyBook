from django.conf import settings
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views import View
from moneybook.models import *
from moneybook.forms import *
from datetime import date
import json

class AddIntraMoveView(View):
    def get(self, request, *args, **kwargs):
        return redirect('moneybook:add')

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = IntraMoveForm(request.POST)
        if form.is_valid():
            try:
                outData = Data()
                outData.date = date(int(request.POST.get("year")), int(request.POST.get("month")), int(request.POST.get("day")))
                outData.price = request.POST.get("price")
                outData.direction = Direction.get(2)
                outData.method = Method.get(request.POST.get("before_method"))
                outData.genre = Genre.get(-2)
                outData.temp = False
                if request.POST.get("item"):
                    outData.item = request.POST.get("item")
                else:
                    outData.item = Method.get(request.POST.get("after_method")).name + "チャージ"

                inData = Data()
                inData.date = date(int(request.POST.get("year")), int(request.POST.get("month")), int(request.POST.get("day")))
                inData.price = request.POST.get("price")
                inData.direction = Direction.get(1)
                inData.method = Method.get(request.POST.get("after_method"))
                inData.genre = Genre.get(-2)
                inData.temp = False
                if request.POST.get("item"):
                    inData.item = request.POST.get("item")
                else:
                    inData.item = inData.method.name + "チャージ"
                
                outData.save()
                inData.save()
                
                year = request.POST.get('year')
                month = request.POST.get('month')
                # 今月のデータ
                monthlyData = Data.sortDateDescending(Data.getMonthData(int(year), int(month)))
                content = {
                    'app_name': settings.APP_NAME,
                    'username': request.user,
                    'show_data': monthlyData,
                }
                # 追加後のmonthlyテーブルを返す
                return render(request, '_data_table.html', content)

            except:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()