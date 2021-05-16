from datetime import date, datetime, timedelta

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.shortcuts import render
from django.views import View
from moneybook.models import Data, LabelValue


class PeriodBalanceView(View):
    def get(self, request, *args, **kwargs):
        now = datetime.now()
        context = {
            'app_name': settings.APP_NAME,
            'username': request.user,
            'draw_graph': False
        }

        # パラメータ取得
        if 'start_year' not in request.GET or 'start_month' not in request.GET or \
                'end_year' not in request.GET or 'end_month' not in request.GET:
            # パラメータが無いときはデフォルト値で去年~今月を入れる
            start_year = now.year - 1
            start_month = 1
            end_year = now.year
            end_month = now.month
        else:
            try:
                start_year = int(request.GET.get('start_year'))
                start_month = int(request.GET.get('start_month'))
                end_year = int(request.GET.get('end_year'))
                end_month = int(request.GET.get('end_month'))
            except ValueError:
                return render(request, 'period_balances.html', context)

        i_date = date(start_year, start_month, 1)
        end_date = date(end_year, end_month, 1)

        period_balances = []
        while True:
            last_day = i_date + relativedelta(months=1) - timedelta(days=1)
            d = Data.get_range_data(None, last_day)
            period_balances.append(LabelValue(datetime.strftime(i_date, '%Y-%m'), Data.get_income_sum(d) - Data.get_outgo_sum(d)))

            if i_date == end_date:
                break
            i_date = i_date + relativedelta(months=1)

        context['draw_graph'] = True
        context['period_balances'] = period_balances
        context['start_year'] = start_year
        context['start_month'] = start_month
        context['end_year'] = end_year
        context['end_month'] = end_month
        return render(request, 'period_balances.html', context)
