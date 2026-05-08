import calendar
import http
from datetime import date
from http import HTTPStatus

from django.db import transaction
from django.http import JsonResponse
from django.views import View
from moneybook.forms import DataForm, IntraMoveForm
from moneybook.models import Category, Data, Direction, Method, PeriodicData


class AddApiView(View):
    def post(self, request, *args, **kwargs):
        new_data = DataForm(request.POST)
        if new_data.is_valid():
            # データ追加
            new_data.save()
            # 成功レスポンス
            return JsonResponse({})

        else:
            error_list = []
            for a in new_data.errors:
                error_list.append(a)
            res_data = {
                'ErrorList': error_list,
            }
            return JsonResponse(res_data, status=http.HTTPStatus.BAD_REQUEST)


class AddIntraMoveApiView(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = IntraMoveForm(request.POST)
        if form.is_valid():
            try:
                out_data = Data()
                out_data.date = date(int(request.POST.get('year')), int(
                    request.POST.get('month')), int(request.POST.get('day')))
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
                return JsonResponse({})

            except:
                return JsonResponse({}, status=http.HTTPStatus.BAD_REQUEST)
        else:
            return JsonResponse({}, status=http.HTTPStatus.BAD_REQUEST)


class SuggestApiView(View):
    def get(self, request, *args, **kwargs):
        if 'item' not in request.GET:
            res = {'message': 'missing item'}
            return JsonResponse(res, status=http.HTTPStatus.BAD_REQUEST)

        item = request.GET.get('item')
        if item == '':
            res = {'message': 'empty item'}
            return JsonResponse(res, status=http.HTTPStatus.BAD_REQUEST)

        data = Data.sort_descending(
            Data.get_startswith_keyword_data(Data.get_all_data(), item))
        suggests = [{'date': v.date.strftime(
            '%Y-%m-%d'), 'item': v.item, 'price': v.price} for v in data]

        return JsonResponse({'suggests': suggests})


class AddPeriodicApiView(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        year = request.POST.get('year')
        month = request.POST.get('month')
        if not year or not month:
            return JsonResponse({'error': 'year and month are required'}, status=HTTPStatus.BAD_REQUEST)

        try:
            year = int(year)
            month = int(month)
            if not 1 <= month <= 12:
                raise ValueError
        except ValueError:
            return JsonResponse({'error': 'invalid year or month'}, status=HTTPStatus.BAD_REQUEST)

        periodic_data = PeriodicData.get_all()
        last_day = calendar.monthrange(year, month)[1]

        data_to_create = [
            Data(
                date=date(year, month, min(pd.day, last_day)),
                item=pd.item,
                price=pd.price,
                direction=pd.direction,
                method=pd.method,
                category=pd.category,
                temp=pd.temp,
                checked=False,
                pre_checked=False,
            )
            for pd in periodic_data
        ]
        if data_to_create:
            Data.objects.bulk_create(data_to_create)

        return JsonResponse({})
