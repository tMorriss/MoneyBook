from django.conf import settings
from django.shortcuts import render
from datetime import datetime
from moneybook.models import Data, InOutBalance, LabelValue, InfraCost
import calendar


def statistics_month(request, year):
    # 月ごとの収入、支出
    month_list = list(range(1, 13))
    month_iob = []
    month_all_iob = []
    before_balances = []
    infra_costs = []
    food_costs = []
    living_costs = []
    salary = []
    for i_month in range(len(month_list)):
        monthly_data = Data.getMonthData(year, month_list[i_month])
        monthly_normal_data = Data.getNormalData(monthly_data)
        t = Data.getTempAndDeposit(monthly_data)
        i = Data.getIncomeSum(monthly_normal_data) - t
        o = Data.getOutgoSum(monthly_normal_data) - t

        # if i != 0 and o != 0:
        month_iob.append(InOutBalance(month_list[i_month], i, o, i - o))

        monthly_data_without_in_move = Data.getDataWithoutInmove(monthly_data)
        i = Data.getIncomeSum(monthly_data_without_in_move) - t
        o = Data.getOutgoSum(monthly_data_without_in_move) - t
        month_all_iob.append(InOutBalance(month_list[i_month], i, o, i - o))

        d = Data.getRangeData(None, datetime(
            year,
            month_list[i_month],
            calendar.monthrange(year, month_list[i_month])[1]))
        before_balances.append(LabelValue(
            month_list[i_month], Data.getIncomeSum(d) - Data.getOutgoSum(d)))

        e = Data.getOutgoSum(Data.getKeywordData(monthly_data, "電気代"))
        g = Data.getOutgoSum(Data.getKeywordData(monthly_data, "ガス代"))
        w = Data.getOutgoSum(Data.getKeywordData(monthly_data, "水道代"))
        if (w > 0):
            if i_month > 0:
                infra_costs[i_month - 1].total += w / 2
                infra_costs[i_month - 1].water = w / 2
        infra_costs.append(
            InfraCost(month_list[i_month], e + g + w / 2, e, g, w / 2))

        food_costs.append(LabelValue(
            month_list[i_month],
            Data.getFoodCosts(monthly_data))
        )

        living_costs.append(LabelValue(
            month_list[i_month],
            Data.getOutgoSum(Data.getLivingData(monthly_data)))
        )

        salary.append(LabelValue(
            month_list[i_month],
            Data.getIncomeSum(Data.getKeywordData(monthly_data, "給与"))
        ))

    content = {
        'app_name': settings.APP_NAME,
        'username': request.user,
        'year': year,
        'month_list': month_list,
        'month_io_list': month_iob,
        'month_all_io_list': month_all_iob,
        'before_balance': before_balances,
        'infra_costs': infra_costs,
        'food_costs': food_costs,
        'living_costs': living_costs,
        'salary': salary
    }
    return render(request, 'statistics.html', content)


def statistics(request):
    now = datetime.now()
    return statistics_month(request, now.year)
