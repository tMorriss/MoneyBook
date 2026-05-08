from datetime import date, datetime, timedelta

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.shortcuts import render
from django.views import View
from moneybook.models import Data


class StatisticsView(View):
    def get(self, request, *args, **kwargs):
        now = datetime.now()
        return StatisticsMonthView().get(request=request, year=now.year)


class StatisticsMonthView(View):
    def get(self, request, *args, **kwargs):
        year = kwargs['year']
        month_list = list(range(1, 13))

        # 月ごとのデータ
        monthly_context = []
        for i_month in month_list:
            tomonth_context = {}
            tomonth_context['label'] = i_month
            monthly_data = Data.get_month_data(year, i_month)
            monthly_normal_data = Data.get_normal_data(monthly_data)
            next_month_first = date(year, i_month, 1) + relativedelta(months=1)

            # 収支
            td = Data.get_deposit_sum(monthly_data)
            tomonth_context['income'] = Data.get_income_sum(monthly_normal_data) - td
            tomonth_context['outgo'] = Data.get_outgo_sum(monthly_normal_data) - td
            tomonth_context['balance'] = tomonth_context['income'] - tomonth_context['outgo']
            # 給与
            tomonth_context['salary'] = Data.get_income_sum(Data.get_keyword_data(monthly_data, '給与'))
            # 生活費
            tomonth_context['living_cost'] = Data.get_living_cost(monthly_data)
            # 食費
            tomonth_context['food_cost'] = Data.get_food_costs(monthly_data)
            # 電気代
            tomonth_context['electricity_cost'] = Data.get_outgo_sum(Data.get_keyword_data(monthly_data, '電気代'))
            # ガス代
            tomonth_context['gus_cost'] = Data.get_outgo_sum(Data.get_keyword_data(monthly_data, 'ガス代'))
            # 水道代
            w = Data.get_outgo_sum(Data.get_keyword_data(monthly_data, '水道代')) / 2
            if (w == 0):
                d = Data.get_month_data(next_month_first.year, next_month_first.month)
                w = Data.get_outgo_sum(Data.get_keyword_data(d, '水道代')) / 2
            tomonth_context['water_cost'] = w
            tomonth_context['infra_cost'] = tomonth_context['electricity_cost'] + \
                tomonth_context['gus_cost'] + tomonth_context['water_cost']
            # 全収支
            monthly_data_without_in_move = Data.filter_without_intra_move(monthly_data)
            t = Data.get_temp_sum(monthly_data)
            tomonth_context['all_income'] = Data.get_income_sum(monthly_data_without_in_move) - t
            tomonth_context['all_outgo'] = Data.get_outgo_sum(monthly_data_without_in_move) - t
            tomonth_context['all_balance'] = tomonth_context['all_income'] - tomonth_context['all_outgo']
            # 途中残高
            last_day = next_month_first - timedelta(days=1)
            rd = Data.get_range_data(None, last_day)
            tomonth_context['period_balance'] = Data.get_income_sum(rd) - Data.get_outgo_sum(rd)

            monthly_context.append(tomonth_context)

        context = {
            'app_name': settings.APP_NAME,
            'username': request.user,
            'year': year,
            'monthly_context': monthly_context
        }
        return render(request, 'statistics.html', context)
