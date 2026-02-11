from datetime import date

from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
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
                out_data.date = date(int(request.POST.get('year')), int(request.POST.get('month')), int(request.POST.get('day')))
                out_data.price = request.POST.get('price')
                out_data.direction = Direction.get(2)
                out_data.method = Method.get(request.POST.get('before_method'))
                out_data.category = Category.get_intra_move()
                out_data.temp = False
                out_data.item = request.POST.get('item')

                in_data = Data()
                in_data.date = date(int(request.POST.get('year')), int(
                    request.POST.get('month')), int(request.POST.get('day')))
                in_data.price = request.POST.get('price')
                in_data.direction = Direction.get(1)
                in_data.method = Method.get(request.POST.get('after_method'))
                in_data.category = Category.get_intra_move()
                in_data.temp = False
                in_data.item = request.POST.get('item')

                # 保存
                out_data.save()
                in_data.save()

                # 成功レスポンス
                return HttpResponse()

            except:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()
