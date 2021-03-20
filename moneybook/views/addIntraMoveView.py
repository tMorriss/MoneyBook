from datetime import date

from django.conf import settings
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views import View
from moneybook.forms import IntraMoveForm
from moneybook.models import Category, Data, Direction, Method


class AddIntraMoveView(View):
    def get(self, request, *args, **kwargs):
        return redirect('moneybook:add')

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = IntraMoveForm(request.POST)
        if form.is_valid():
            try:
                out_data = Data()
                out_data.date = date(int(request.POST.get("year")), int(
                    request.POST.get("month")), int(request.POST.get("day")))
                out_data.price = request.POST.get("price")
                out_data.direction = Direction.get(2)
                out_data.method = Method.get(request.POST.get("before_method"))
                out_data.category = Category.get(10)
                out_data.temp = False
                if request.POST.get("item"):
                    out_data.item = request.POST.get("item")
                else:
                    out_data.item = Method.get(
                        request.POST.get("after_method")).name + "チャージ"

                in_data = Data()
                in_data.date = date(int(request.POST.get("year")), int(
                    request.POST.get("month")), int(request.POST.get("day")))
                in_data.price = request.POST.get("price")
                in_data.direction = Direction.get(1)
                in_data.method = Method.get(request.POST.get("after_method"))
                in_data.category = Category.get(10)
                in_data.temp = False
                if request.POST.get("item"):
                    in_data.item = request.POST.get("item")
                else:
                    in_data.item = in_data.method.name + "チャージ"

                out_data.save()
                in_data.save()

                year = request.POST.get('year')
                month = request.POST.get('month')
                # 今月のデータ
                monthly_data = Data.sort_data_descending(
                    Data.get_month_data(int(year), int(month)))
                context = {
                    'app_name': settings.APP_NAME,
                    'username': request.user,
                    'show_data': monthly_data,
                }
                # 追加後のmonthlyテーブルを返す
                return render(request, '_data_table.html', contextcontext)

            except:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()
