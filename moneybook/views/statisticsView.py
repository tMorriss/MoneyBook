import calendar
from datetime import datetime

from django.conf import settings
from django.shortcuts import render
from django.views import View
from moneybook.models import Data, InfraCost, InOutBalance, LabelValue


class StatisticsView(View):
    def get(self, request, *args, **kwargs):
        now = datetime.now()
        return StatisticsMonthView().get(request=request, year=now.year)


class StatisticsMonthView(View):
    def get(self, request, *args, **kwargs):
        year = kwargs['year']
        # 月ごとの収入、支出
        month_list = list(range(1, 13))
        month_iob = []
        month_all_iob = []
        period_balances = []
        infra_costs = []
        food_costs = []
        living_costs = []
        salary = []
        for i_month in range(len(month_list)):
            monthly_data = Data.get_month_data(year, month_list[i_month])
            monthly_normal_data = Data.get_normal_data(monthly_data)
            td = Data.get_temp_and_deposit_sum(monthly_data)
            i = Data.get_income_sum(monthly_normal_data) - td
            o = Data.get_outgo_sum(monthly_normal_data) - td

            month_iob.append(InOutBalance(month_list[i_month], i, o, i - o))

            monthly_data_without_in_move = Data.filter_without_intra_move(
                monthly_data)
            t = Data.get_temp_sum(monthly_data)
            i = Data.get_income_sum(monthly_data_without_in_move) - t
            o = Data.get_outgo_sum(monthly_data_without_in_move) - t
            month_all_iob.append(InOutBalance(
                month_list[i_month], i, o, i - o))

            d = Data.get_range_data(None, datetime(
                year,
                month_list[i_month],
                calendar.monthrange(year, month_list[i_month])[1]))
            period_balances.append(LabelValue(
                month_list[i_month], Data.get_income_sum(d) - Data.get_outgo_sum(d)))

            e = Data.get_outgo_sum(Data.get_keyword_data(monthly_data, "電気代"))
            g = Data.get_outgo_sum(Data.get_keyword_data(monthly_data, "ガス代"))
            w = Data.get_outgo_sum(Data.get_keyword_data(monthly_data, "水道代"))
            if (w > 0):
                if i_month > 0:
                    infra_costs[i_month - 1].total += w / 2
                    infra_costs[i_month - 1].water = w / 2
            infra_costs.append(
                InfraCost(month_list[i_month], e + g + w / 2, e, g, w / 2))

            food_costs.append(LabelValue(
                month_list[i_month],
                Data.get_food_costs(monthly_data))
            )

            living_costs.append(
                LabelValue(
                    month_list[i_month],
                    Data.get_living_cost(monthly_data)
                )
            )

            salary.append(LabelValue(
                month_list[i_month],
                Data.get_income_sum(Data.get_keyword_data(monthly_data, "給与"))
            ))

        # 12月の水道代
        next_month_data = Data.get_month_data(year + 1, 1)
        w = Data.get_outgo_sum(Data.get_keyword_data(next_month_data, "水道代"))
        if (w > 0):
            if i_month > 0:
                infra_costs[11].total += w / 2
                infra_costs[11].water = w / 2

        context = {
            'app_name': settings.APP_NAME,
            'username': request.user,
            'year': year,
            'month_list': month_list,
            'month_io_list': month_iob,
            'month_all_io_list': month_all_iob,
            'period_balances': period_balances,
            'infra_costs': infra_costs,
            'food_costs': food_costs,
            'living_costs': living_costs,
            'salary': salary
        }
        return render(request, 'statistics.html', context)
