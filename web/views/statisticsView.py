from django.conf import settings
from django.shortcuts import render
from datetime import datetime
from web.models import *

def statistics(request):
    now = datetime.now()

    # 月ごとの収入、支出
    monthList = list(range(1, 13))
    monthIOB = []
    monthAllIOB = []
    beforeBalances = []
    infraCosts = []
    FoodCosts = []
    for iMonth in range(len(monthList)):
        monthlyData = Data.getMonthData(now.year, monthList[iMonth])
        monthlyNormalData = Data.getNormalData(monthlyData)
        t = Data.getTempAndDeposit(monthlyData)
        i = Data.getIncomeSum(monthlyNormalData) - t
        o = Data.getOutgoSum(monthlyNormalData) - t

        # if i != 0 and o != 0:
        monthIOB.append(InOutBalance(monthList[iMonth], i, o, i - o))
        
        monthlyDataWithoutInMove = Data.getDataWithoutInmove(monthlyData)
        i = Data.getIncomeSum(monthlyDataWithoutInMove) - t
        o = Data.getOutgoSum(monthlyDataWithoutInMove) - t
        monthAllIOB.append(InOutBalance(monthList[iMonth], i, o, i - o))

        d = Data.getRangeData(None, datetime(now.year, monthList[iMonth], calendar.monthrange(now.year, monthList[iMonth])[1]))
        beforeBalances.append(LabelValue(monthList[iMonth], Data.getIncomeSum(d) - Data.getOutgoSum(d)))

        e = Data.getOutgoSum(Data.getKeywordData(monthlyData, "電気代"))
        g = Data.getOutgoSum(Data.getKeywordData(monthlyData, "ガス代"))
        w = Data.getOutgoSum(Data.getKeywordData(monthlyData, "水道代"))
        if (w > 0):
            if iMonth > 0:
                infraCosts[iMonth - 1].water = w / 2
        infraCosts.append(InfraCost(monthList[iMonth], e + g + w / 2, e, g, w))

        FoodCosts.append(LabelValue(monthList[iMonth], Data.getFoodCosts(monthlyData)))

    content = {
        'app_name': settings.APP_NAME,
        'year': now.year,
        'month': now.month,
        'month_list': monthList,
        'month_io_list': monthIOB,
        'month_all_io_list': monthAllIOB,
        'before_balance': beforeBalances,
        'infra_costs': infraCosts,
        'food_costs': FoodCosts,
    }
    return render(request, 'web/statistics.html', content)
