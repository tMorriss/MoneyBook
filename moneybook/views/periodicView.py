import json
from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views import View
from moneybook.forms import PeriodicDataForm
from moneybook.models import Category, Direction, Method, PeriodicData


class PeriodicListView(View):
    """定期取引一覧表示"""
    def get(self, request, *args, **kwargs):
        now = datetime.now()
        # 来月を計算
        next_month = now + relativedelta(months=1)

        context = {
            'app_name': settings.APP_NAME,
            'username': request.user,
            'year': now.year,
            'month': now.month,
            'next_year': next_month.year,
            'next_month': next_month.month,
            'periodic_data_list': PeriodicData.get_all(),
            'directions': Direction.list(),
            'methods': Method.list(),
            'first_categories': Category.first_list(),
            'latter_categories': Category.latter_list(),
        }
        return render(request, 'periodic_list.html', context)


class PeriodicConfigView(View):
    """定期取引設定API"""
    def post(self, request, *args, **kwargs):
        """設定を更新"""
        try:
            # JSONデータを取得
            data = json.loads(request.body)
            periodic_data_list = data.get('periodic_data_list', [])

            # 既存のデータを全削除
            PeriodicData.objects.all().delete()

            # 新しいデータを保存
            for item in periodic_data_list:
                form = PeriodicDataForm(item)
                if form.is_valid():
                    form.save()
                else:
                    error_list = [str(e) for e in form.errors]
                    return HttpResponseBadRequest(json.dumps({'errors': error_list}))

            return HttpResponse()
        except Exception as e:
            return HttpResponseBadRequest(json.dumps({'error': str(e)}))
