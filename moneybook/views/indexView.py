from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.shortcuts import redirect, render
from django.views import View
from moneybook.models import Category, Direction, Method
from moneybook.utils import is_valid_date


class IndexView(View):
    def get(self, request, *args, **kwargs):
        now = datetime.now()
        year = now.year
        month = now.month
        return IndexMonthView().get(request=request, year=year, month=month)


class IndexMonthView(View):
    def get(self, request, *args, **kwargs):
        year = kwargs['year']
        month = kwargs['month']
        # validation
        if not is_valid_date(year, month):
            return redirect('moneybook:index')
        # 前後の日付
        to_month = datetime(int(year), int(month), 1)
        next_month = to_month + relativedelta(months=1)
        last_month = to_month - relativedelta(months=1)

        # 今月の場合だけ日付を入れる
        now = datetime.now()
        day = day = now.day if year == now.year and month == now.month else ''

        context = {
            'app_name': settings.APP_NAME,
            'username': request.user,
            'year': year,
            'month': month,
            'day': day,
            'next_year': next_month.year,
            'next_month': next_month.month,
            'last_year': last_month.year,
            'last_month': last_month.month,
            'directions': Direction.list(),
            'methods': Method.list(),
            'unused_methods': Method.un_used_list(),
            'first_categories': Category.first_list(),
            'latter_categories': Category.latter_list(),
            'temps': {0: 'No', 1: 'Yes'},
            'category_directions': {
                c.pk: c.default_direction.pk if c.default_direction else 2
                for c in Category.list().select_related('default_direction')
            },
        }

        return render(request, 'index.html', context)
