import calendar
from datetime import datetime

from django.conf import settings
from django.shortcuts import render
from django.views import View
from moneybook.models import Data, InOutBalance, LabelValue


class AllInoutView(View):
    def get(self, request, *args, **kwargs):
        now = datetime.now()
        return AllInoutMonthView().get(request, year=now.year)


class AllInoutMonthView(View):
    def get(self, request, *args, **kwargs):
        year = kwargs['year']
        month_list = list(range(1, 13))
        month_all_iob = []
        period_balances = []

        for i_month in range(len(month_list)):
            monthly_data = Data.get_month_data(year, month_list[i_month])
            monthly_data_without_in_move = Data.filter_without_intra_move(monthly_data)
            t = Data.get_temp_sum(monthly_data)
            i = Data.get_income_sum(monthly_data_without_in_move) - t
            o = Data.get_outgo_sum(monthly_data_without_in_move) - t
            month_all_iob.append(InOutBalance(month_list[i_month], i, o, i - o))

            d = Data.get_range_data(None, datetime(year, month_list[i_month], calendar.monthrange(year, month_list[i_month])[1]))
            period_balances.append(LabelValue(month_list[i_month], Data.get_income_sum(d) - Data.get_outgo_sum(d)))

        context = {
            'app_name': settings.APP_NAME,
            'username': request.user,
            'year': year,
            'month_all_io_list': month_all_iob,
            'period_balances': period_balances,
        }
        return render(request, 'all_inout.html', context)
