from django.conf import settings
from django.shortcuts import render
from datetime import datetime
from dateutil.relativedelta import relativedelta
from moneybook.models import *

def index_month(request, year, month):
    # 全データ
    allData = Data.getAllData()
    # 今月のデータ
    monthlyData = Data.sortDateDescending(Data.getMonthData(int(year), int(month)))
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
        if g.show_order >= 0:
            d = Data.getGenreData(monthlyData, g.pk)
            positiveGenresOutgo[g] = Data.getOutgoSum(d)

    totalIncome = Data.getIncomeSum(Data.getNormalData(monthlyData)) - monthlyTempAndDeposit
    totalOutgo = Data.getOutgoSum(Data.getNormalData(monthlyData)) - monthlyTempAndDeposit
    fixedOutgo = Data.getOutgoSum(Data.getFixedData(monthlyData))
    variableOutgo = Data.getOutgoSum(Data.getVariableData(monthlyData))

    # 前後の日付
    toMonth = datetime(int(year), int(month), 1)
    nextMonth = toMonth + relativedelta(months=1)
    lastMonth = toMonth - relativedelta(months=1)

    content = {
        'app_name': settings.APP_NAME,
        'username': request.user,
        'year': year,
        'month': month,
        'next_year': nextMonth.year,
        'next_month': nextMonth.month,
        'last_year': lastMonth.year,
        'last_month': lastMonth.month,
        'show_data': monthlyData,
        'methods': methods,
        'first_genres': Genre.first_list(),
        'latter_genres': Genre.latter_list(),
        'total_balance': Data.getIncomeSum(allData) - Data.getOutgoSum(allData),
        'total_income': totalIncome,
        'total_outgo': totalOutgo,
        'total_inout': totalIncome - totalOutgo,
        'fixed_outgo': fixedOutgo,
        'variable_outgo': variableOutgo,
        'variable_remain': totalIncome - max(SeveralCosts.getFixedCostMark(), fixedOutgo) - variableOutgo,
        'all_income': Data.getIncomeSum(monthlyData),
        'all_outgo': Data.getOutgoSum(monthlyData),
        'genres_outgo': positiveGenresOutgo,
        'methods_iob': methodsIOB,
        'methods_monthly_iob': methodsMonthlyIOB,
    }
    return render(request, 'index.html', content)

def index(request):
    now = datetime.now()
    year = now.year
    month = str(now.month).zfill(2)
    return index_month(request, year, month)
