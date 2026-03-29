import http

from django.http import JsonResponse
from django.views import View
from moneybook.forms import DataForm
from moneybook.models import Category, Data, Direction, Method


class EditApiView(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']

        try:
            data = Data.get(pk)
        except:
            return JsonResponse({'message': 'Data does not exist'}, status=http.HTTPStatus.BAD_REQUEST)

        new_data = DataForm(request.POST)
        if new_data.is_valid():
            # データ更新
            data.date = request.POST.get('date')
            data.item = request.POST.get('item')
            data.price = request.POST.get('price')
            data.direction = Direction.get(request.POST.get('direction'))
            data.method = Method.get(request.POST.get('method'))
            data.category = Category.get(request.POST.get('category'))
            data.temp = request.POST.get('temp')
            data.checked = request.POST.get('checked')
            data.save()

            return JsonResponse({})
        else:
            res_data = {}
            error_list = []
            for a in new_data.errors:
                error_list.append(a)
            res_data['ErrorList'] = error_list
            return JsonResponse(res_data, status=http.HTTPStatus.BAD_REQUEST)


class ApplyCheckApiView(View):
    def post(self, request, *args, **kwargs):
        all_data = Data.get_all_data()
        unchecked_data = Data.get_unchecked_data(all_data)
        pre_checked_data = Data.get_pre_checked_data(unchecked_data)

        for data in pre_checked_data:
            data.pre_checked = False
            data.checked = True
            data.save()

        return JsonResponse({})


class PreCheckApiView(View):
    def post(self, request, *args, **kwargs):
        pk = request.POST.get('id')
        status = request.POST.get('status')

        try:
            data = Data.get(pk)
        except:
            res = {'message': 'Data does not exist'}
            return JsonResponse(res, status=http.HTTPStatus.BAD_REQUEST)

        if status == '1':
            data.pre_checked = True
        else:
            data.pre_checked = False
        data.save()
        return JsonResponse({})
