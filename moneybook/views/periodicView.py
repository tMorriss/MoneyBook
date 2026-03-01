import calendar
import json
from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views import View
from moneybook.forms import PeriodicDataForm
from moneybook.models import Category, Data, Direction, Method, PeriodicData


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
        }
        return render(request, 'periodic_list.html', context)


class PeriodicConfigView(View):
    """定期取引設定画面"""
    def get(self, request, *args, **kwargs):
        context = {
            'app_name': settings.APP_NAME,
            'username': request.user,
            'periodic_data_list': PeriodicData.get_all(),
            'directions': Direction.list(),
            'methods': Method.list(),
            'first_categories': Category.first_list(),
            'latter_categories': Category.latter_list(),
            'temps': {0: 'No', 1: 'Yes'},
        }
        return render(request, 'periodic_config.html', context)

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

            return HttpResponse(json.dumps({'success': True}))
        except Exception as e:
            return HttpResponseBadRequest(json.dumps({'error': str(e)}))


class PeriodicAddBulkView(View):
    """定期取引一括登録API"""
    def post(self, request, *args, **kwargs):
        try:
            # JSONデータを取得
            data = json.loads(request.body)
            year = data.get('year')
            month = data.get('month')
            periodic_id = int(data.get('periodic_id'))

            # yearまたはmonthが空の場合はエラー（JavaScriptでデフォルト値が設定されるはず）
            if not year or not month:
                return HttpResponseBadRequest(json.dumps({'error': '年月が指定されていません'}))

            year = int(year)
            month = int(month)

            # PeriodicDataを取得
            periodic_data = PeriodicData.get(periodic_id)

            # 日付の妥当性チェック
            day = periodic_data.day
            max_day = calendar.monthrange(year, month)[1]
            if day > max_day:
                day = max_day

            # Dataオブジェクトを作成
            target_date = date(year, month, day)

            # データを作成（重複チェックなし）
            new_data = Data(
                date=target_date,
                item=periodic_data.item,
                price=periodic_data.price,
                direction=periodic_data.direction,
                method=periodic_data.method,
                category=periodic_data.category,
                temp=periodic_data.temp,
                checked=False,
                pre_checked=False,
            )
            new_data.save()

            return HttpResponse(json.dumps({
                'success': True,
                'message': 'データを登録しました'
            }))

        except Exception as e:
            return HttpResponseBadRequest(json.dumps({'error': str(e)}))
