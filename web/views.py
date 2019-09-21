from django.shortcuts import render
from django.http import HttpResponse, Http404
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
        'total_balance': Data.getIncomeSum(allData) - Data.getOutgoSum(allData),
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

def search(request):
    queryContent = {}
    queryList = ["start_year", "start_month", "start_day", "end_year", "end_month", "end_day", "item", "lower_price", "upper_price"]
    for q in queryList:
        if q in request.GET:
            queryContent[q] = request.GET.get(q)

    content = {
        'app_name': settings.APP_NAME,
        'directions': Direction.list(),
        'methods': Method.list(),
        'unused_methods': Method.unUsedList(),
        'first_genres': Genre.first_list(),
        'latter_genres': Genre.latter_list(),
        'temps': {0: "No", 1: "Yes"},
        'checked': {0: "No", 1: "Yes"},
    }
    content.update(queryContent)
    return render(request, 'web/search.html', content)

def tools(request):
    now = datetime.now()
    # 全データ
    allData = Data.getAllData()
    # 実際の現金残高
    actualCashBalance = SeveralCosts.getActualCashBalance()
    # 支払い方法リスト
    methods = Method.list()
    # 支払い方法ごとの残高
    methodsBD = []
    for m in methods:
        d = Data.getMethodData(allData, m.pk)
        methodsBD.append(BalanceDate(m, Data.getIncomeSum(d) - Data.getOutgoSum(d), CheckedDate.get(m.pk).date))
    # クレカ確認日
    creditCheckedDate = CreditCheckedDate.getAll()
    # キャッシュバック確認日
    cachebackCheckedDate = CachebackCheckedDate.getAll()
    # 銀行残高
    bankBalance = BankBalance.getAll()
    # 固定費目標額
    fixedCostMark = SeveralCosts.getFixedCostMark()
    # 未承認トランザクション
    uncheckedData = Data.getUncheckedData(allData)
    # 現在銀行
    banks = BankBalance.getAll()
    # 銀行残高
    allBankData = Data.getBankData(allData)
    bankWritten = Data.getIncomeSum(allBankData) - Data.getOutgoSum(allBankData)

    content = {
        'app_name': settings.APP_NAME,
        'cash_balance': Data.getIncomeSum(Data.getCashData(Data.getAllData())) - Data.getOutgoSum(Data.getCashData(Data.getAllData())),
        'year': now.year,
        'month': now.month,
        'day': now.day,
        'actual_cash_balance': actualCashBalance,
        'methods_bd': methodsBD,
        'credit_checked_date': creditCheckedDate,
        'cacheback_checked_date': cachebackCheckedDate,
        'bank_balance': bankBalance,
        'fixed_cost_mark': fixedCostMark,
        'unchecked_data': uncheckedData,
        'banks': banks,
        'bank_written': bankWritten,
    }
    return render(request, "web/tools.html", content)

def edit(request, pk):
    try:
        data = Data.get(pk)
    except Data.DoesNotExist:
        raise Http404("Data does not exist")

    content = {
        'app_name': settings.APP_NAME,
        'data': data,
        'directions': Direction.list(),
        'methods': Method.list(),
        'first_genres': Genre.first_list(),
        'latter_genres': Genre.latter_list(),
        'temps': {0:"No", 1:"Yes"},
        'checked': {0: "No", 1: "Yes"},
    }
    return render(request, "web/edit.html", content)