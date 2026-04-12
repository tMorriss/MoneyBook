import calendar
from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views import View
from moneybook.models import LivingCostMark


class LivingCostMarkEditView(LoginRequiredMixin, View):
    """生活費目標編集"""

    def get(self, request, *args, **kwargs):
        """編集画面表示"""
        context = {
            'app_name': settings.APP_NAME,
            'username': request.user,
            'living_cost_marks': LivingCostMark.get_all(),
        }
        return render(request, 'living_cost_mark_edit.html', context)

    def post(self, request, *args, **kwargs):
        """設定を更新して一覧にリダイレクト"""
        new_marks = []
        for key in request.POST.keys():
            if key.startswith('start_date_'):
                id_part = key[len('start_date_'):]
                start_date_str = request.POST.get(f'start_date_{id_part}')
                end_date_str = request.POST.get(f'end_date_{id_part}')
                price_str = request.POST.get(f'price_{id_part}').replace(',', '')

                if start_date_str and price_str:
                    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                    end_date = None
                    if end_date_str:
                        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                    price = int(price_str)
                    new_marks.append(LivingCostMark(start_date=start_date, end_date=end_date, price=price))

        # ソート
        new_marks.sort(key=lambda x: x.start_date)

        # バリデーション
        error_message = None
        for i in range(len(new_marks)):
            mark = new_marks[i]
            # 開始日は1日
            if mark.start_date.day != 1:
                error_message = f'開始日は1日に設定してください: {mark.start_date}'
                break

            if mark.end_date:
                # 終了日は月末
                last_day = calendar.monthrange(mark.end_date.year, mark.end_date.month)[1]
                if mark.end_date.day != last_day:
                    error_message = f'終了日は月末に設定してください: {mark.end_date}'
                    break

                # 開始日 < 終了日
                if mark.start_date >= mark.end_date:
                    error_message = f'開始日は終了日より前に設定してください: {mark.start_date}'
                    break

            # 連続性のチェック
            if i > 0:
                prev_mark = new_marks[i - 1]
                if prev_mark.end_date + relativedelta(days=1) != mark.start_date:
                    error_message = f'期間に隙間または重複があります: {prev_mark.end_date} と {mark.start_date}'
                    break

            # 最後のデータ以外は終了日が必須
            if i < len(new_marks) - 1 and mark.end_date is None:
                error_message = '途中のデータの終了年月は必須です'
                break

        if error_message:
            context = {
                'app_name': settings.APP_NAME,
                'username': request.user,
                'living_cost_marks': new_marks,
                'error_message': error_message,
            }
            return render(request, 'living_cost_mark_edit.html', context)

        # 保存
        with transaction.atomic():
            LivingCostMark.objects.all().delete()
            LivingCostMark.objects.bulk_create(new_marks)

        return HttpResponseRedirect(reverse('moneybook:living_cost_mark'))
