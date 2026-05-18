import calendar
from datetime import datetime
from http import HTTPStatus

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

        # 1. データの収集
        ids = set()
        for key in request.POST.keys():
            for prefix in ['start_year_', 'start_month_', 'end_year_', 'end_month_', 'price_']:
                if key.startswith(prefix):
                    id_part = key[len(prefix):]
                    if id_part != 'template':
                        ids.add(id_part)

        for id_part in ids:
            start_year = request.POST.get(f'start_year_{id_part}')
            start_month = request.POST.get(f'start_month_{id_part}')
            end_year = request.POST.get(f'end_year_{id_part}')
            end_month = request.POST.get(f'end_month_{id_part}')
            price_str = request.POST.get(f'price_{id_part}', '').replace(',', '')

            # 全項目空ならスキップ
            if not any([start_year, start_month, end_year, end_month, price_str]):
                continue

            start_date = None
            end_date = None
            price = 0

            # バリデーション (個別の行)
            if not price_str:
                error_message = error_message or '金額が空の行があります'
            else:
                try:
                    price = int(price_str)
                except ValueError:
                    error_message = error_message or '金額が不正です'

            if start_year or start_month:
                if not start_year or not start_month:
                    error_message = error_message or '開始年月の入力が不完全です'
                else:
                    try:
                        start_date = datetime(int(start_year), int(start_month), 1).date()
                    except ValueError:
                        error_message = error_message or '開始年月の値が不正です'

            if end_year or end_month:
                if not end_year or not end_month:
                    error_message = error_message or '終了年月の入力が不完全です'
                else:
                    try:
                        ey, em = int(end_year), int(end_month)
                        last_day = calendar.monthrange(ey, em)[1]
                        end_date = datetime(ey, em, last_day).date()
                    except ValueError:
                        error_message = error_message or '終了年月の値が不正です'

            new_marks.append(LivingCostMark(start_date=start_date, end_date=end_date, price=price))

        if error_message:
            return self._render_error(request, new_marks, error_message, status=HTTPStatus.BAD_REQUEST)

        # 2. 全体のバリデーション
        # ソート (Noneは最小として扱う)
        new_marks.sort(key=lambda x: x.start_date if x.start_date else datetime.min.date())

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
                            f'{mark.start_date.year}/{mark.start_date.month}'
                        )
                        break

        if error_message:
            return self._render_error(request, new_marks, error_message, status=HTTPStatus.BAD_REQUEST)

        # 3. 保存
        with transaction.atomic():
            LivingCostMark.objects.all().delete()
            LivingCostMark.objects.bulk_create(new_marks)

        return HttpResponseRedirect(reverse('moneybook:living_cost_mark'))

    def _render_error(self, request, new_marks, error_message, status=HTTPStatus.OK):
        context = {
            'app_name': settings.APP_NAME,
            'username': request.user,
            'living_cost_marks': new_marks,
            'error_message': error_message,
        }
        return render(request, 'living_cost_mark_edit.html', context, status=status)
