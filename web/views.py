from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.template import loader
from django.conf import settings
from datetime import datetime

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
    monthlyData = Data.getMonthData(int(year), int(month))
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
    monthIncome = {}
    monthOutgo = {}
    for m in monthList:
        monthIncome[m] = Data.getIncomeSum(Data.getMonthData(now.year, m))
        monthOutgo[m] = Data.getOutgoSum(Data.getMonthData(now.year, m))
        i = Data.getIncomeSum(Data.getMonthData(now.year, m))
        o = Data.getOutgoSum(Data.getMonthData(now.year, m))
        monthIOB.append(InOutBalance(m, i, o, i-o))

    content = {
        'year': now.year,
        'month': now.month,
        'month_list': monthList,
        'month_io_list': monthIOB,
        'month_income': monthIncome,
        'month_outgo': monthOutgo,
    }
    return render(request, 'web/statistics.html', content)