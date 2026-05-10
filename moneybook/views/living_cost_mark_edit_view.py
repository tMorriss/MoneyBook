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
        error_message = None
        for key in request.POST.keys():
            if key.startswith('price_'):
                id_part = key[len('price_'):]
                if id_part == 'template':
                    continue

                start_year = request.POST.get(f'start_year_{id_part}')
                start_month = request.POST.get(f'start_month_{id_part}')
                end_year = request.POST.get(f'end_year_{id_part}')
                end_month = request.POST.get(f'end_month_{id_part}')
                price_str = request.POST.get(f'price_{id_part}').replace(',', '')

                if not price_str:
                    continue

                # 開始日の処理
                start_date = None
                if start_year or start_month:
                    if not start_year or not start_month:
                        error_message = '開始年月の入力が不完全です'
                        break
                    try:
                        start_date = datetime(int(start_year), int(start_month), 1).date()
                    except ValueError:
                        error_message = '開始年月の値が不正です'
                        break

                # 終了日の処理
                end_date = None
                if end_year or end_month:
                    if not end_year or not end_month:
                        error_message = '終了年月の入力が不完全です'
                        break
                    try:
                        ey, em = int(end_year), int(end_month)
                        last_day = calendar.monthrange(ey, em)[1]
                        end_date = datetime(ey, em, last_day).date()
                    except ValueError:
                        error_message = '終了年月の値が不正です'
                        break

                try:
                    price = int(price_str)
                except ValueError:
                    error_message = '金額が不正です'
                    break

                new_marks.append(LivingCostMark(start_date=start_date, end_date=end_date, price=price))

        if error_message:
            return self._render_error(request, new_marks, error_message)

        # ソート (Noneは最小として扱う)
        new_marks.sort(key=lambda x: x.start_date if x.start_date else datetime.min.date())

        # バリデーション
        null_start_count = sum(1 for m in new_marks if m.start_date is None)
        if null_start_count > 1:
            error_message = '開始年月が空のデータは1行だけ指定できます'
        else:
            for i in range(len(new_marks)):
                mark = new_marks[i]

                if mark.start_date and mark.end_date:
                    # 開始日 < 終了日
                    if mark.start_date >= mark.end_date:
                        error_message = f'開始年月は終了年月より前に設定してください: {mark.start_date.year}/{mark.start_date.month}'
                        break

                # 連続性のチェック
                if i > 0:
                    prev_mark = new_marks[i - 1]
                    if prev_mark.end_date is None:
                        error_message = '途中のデータの終了年月は必須です'
                        break

                    expected_start = prev_mark.end_date + relativedelta(days=1)
                    if mark.start_date != expected_start:
                        error_message = (
                            f'期間に隙間または重複があります: '
                            f'{prev_mark.end_date.year}/{prev_mark.end_date.month} と '
                            f'{mark.start_date.year}/{mark.start_date.month if mark.start_date else ""}'
                        )
                        break

                # 最後のデータ以外は終了日が必須
                if i < len(new_marks) - 1 and mark.end_date is None:
                    error_message = '途中のデータの終了年月は必須です'
                    break

        if error_message:
            return self._render_error(request, new_marks, error_message)

        # 保存
        with transaction.atomic():
            LivingCostMark.objects.all().delete()
            LivingCostMark.objects.bulk_create(new_marks)

        return HttpResponseRedirect(reverse('moneybook:living_cost_mark'))

    def _render_error(self, request, new_marks, error_message):
        context = {
            'app_name': settings.APP_NAME,
            'username': request.user,
            'living_cost_marks': new_marks,
            'error_message': error_message,
        }
        return render(request, 'living_cost_mark_edit.html', context)
