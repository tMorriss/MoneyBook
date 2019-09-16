from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.template import loader
from django.conf import settings
from datetime import date, datetime
import calendar

def index(request):
    if "year" in request.GET and "month" in request.GET:
        year = request.GET.get("year")
        month = request.GET.get("month")
    else:
        now = datetime.now()
        year = now.year
        month = str(now.month).zfill(2)

    # 全データ
    allData = Data.getAllData()
    # 今月のデータ
    monthlyData = Data.sort_date_descending(Data.getMonthData(int(year), int(month)))
    # 支払い方法リスト
    methods = Method.list()
    # 支払い方法ごとの残高
    methodsIOB = []
    methodsMonthlyIOB = []
    for m in methods:
        d = Data.getMethodData(allData, m.pk)
        methodsIOB.append(InOutBalance(m, None, None, Data.getIncomeSum(d) - Data.getOutgoSum(d)))

        i = Data.getIncomeSum(Data.getMethodData(monthlyData, m.pk))
        o = Data.getOutgoSum(Data.getMethodData(monthlyData, m.pk))
        methodsMonthlyIOB.append(InOutBalance(m, i, o, None))

    # 立替と貯金
    monthlyTempAndDeposit = Data.getTempAndDeposit(monthlyData)

    # ジャンルごとの支出
    positiveGenresOutgo = {}
    for g in Genre.list():
        if g.pk >= 0:
            d = Data.getGenreData(monthlyData, g.pk)
            positiveGenresOutgo[g] = Data.getOutgoSum(d)

    totalIncome = Data.getIncomeSum(Data.getNormalData(monthlyData)) - monthlyTempAndDeposit
    totalOutgo = Data.getOutgoSum(Data.getNormalData(monthlyData)) - monthlyTempAndDeposit
    fixedOutgo = Data.getOutgoSum(Data.getFixedData(monthlyData))
    variableOutgo = Data.getOutgoSum(Data.getVariableData(monthlyData))
    content = {
        'app_name': settings.APP_NAME,
        'year': year,
        'month': month,
        'monthly_data': monthlyData,
        'methods': methods,
        'first_genres': Genre.first_list(),
        'latter_genres': Genre.latter_list(),
        'total_balance': Data.getSum(allData, 0) - Data.getSum(allData, 1),
        'total_income': totalIncome,
        'total_outgo': totalOutgo,
        'total_inout': totalIncome - totalOutgo,
        'fixed_outgo': fixedOutgo,
        'variable_outgo': variableOutgo,
        'variable_remain': totalIncome - max(FixedCostPlan.get(), fixedOutgo) - variableOutgo,
        'all_income': Data.getIncomeSum(monthlyData),
        'all_outgo': Data.getOutgoSum(monthlyData),
        'genres_outgo': positiveGenresOutgo,
        'methods_iob': methodsIOB,
        'methods_monthly_iob': methodsMonthlyIOB,
    }
    return render(request, 'web/index.html', content)

def add(request):
    now = datetime.now()
    content = {
        'app_name': settings.APP_NAME,
        'year': now.year,
        'month': now.month,
        'directions': Direction.list(),
        'methods': Method.list(),
        'first_genres': Genre.first_list(),
        'latter_genres': Genre.latter_list(),
        'temps': {0:"No", 1:"Yes"},
    }
    return render(request, 'web/add.html', content)

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

        e = Data.getSum(Data.getKeywordData(monthlyData, "電気代"), 1)
        g = Data.getSum(Data.getKeywordData(monthlyData, "ガス代"), 1)
        w = Data.getSum(Data.getKeywordData(monthlyData, "水道代"), 1)
        if (w > 0):
            if iMonth > 0:
                infraCosts[iMonth - 1].water = w / 2
        infraCosts.append(InfraCost(monthList[iMonth], e + g + w / 2, e, g, w))

        FoodCosts.append(LabelValue(monthList[iMonth], Data.getFoodCosts(monthlyData)))

    content = {
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