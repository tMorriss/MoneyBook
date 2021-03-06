from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.shortcuts import render
from moneybook.models import (Category, Data, Direction, InOutBalance, Method,
                              SeveralCosts)


def get_monthly_data_from_get_parameter(request_get):
    if "year" in request_get and "month" in request_get:
        year = request_get.get("year")
        month = request_get.get("month")

    monthly_data = Data.sortDateDescending(
        Data.getMonthData(int(year), int(month)))
    return monthly_data


def index(request):
    now = datetime.now()
    year = now.year
    month = str(now.month).zfill(2)
    return index_month(request, year, month)


def index_month(request, year, month):
    # 支払い方法リスト
    methods = Method.list()

    # 前後の日付
    to_month = datetime(int(year), int(month), 1)
    next_month = to_month + relativedelta(months=1)
    last_month = to_month - relativedelta(months=1)

    content = {
        'app_name': settings.APP_NAME,
        'username': request.user,
        'year': year,
        'month': month,
        'next_year': next_month.year,
        'next_month': next_month.month,
        'last_year': last_month.year,
        'last_month': last_month.month,
        'directions': Direction.list(),
        'methods': methods,
        'unused_methods': Method.unUsedList(),
        'first_categories': Category.first_list(),
        'latter_categories': Category.latter_list(),
    }
    return render(request, 'index.html', content)


def index_balance_statistic_mini(request):
    # 全データ
    all_data = Data.getAllData()
    # 今月のデータ
    monthly_data = get_monthly_data_from_get_parameter(request.GET)
    # 支払い方法リスト
    methods = Method.list()
    # 立替と貯金
    monthly_temp_and_deposit = Data.getTempAndDeposit(monthly_data)

    # 支払い方法ごとの残高
    methods_iob = []
    methods_monthly_iob = []
    for m in methods:
        d = Data.getMethodData(all_data, m.pk)
        methods_iob.append(InOutBalance(
            m, None, None, Data.getIncomeSum(d) - Data.getOutgoSum(d)))

        i = Data.getIncomeSum(Data.getMethodData(monthly_data, m.pk))
        o = Data.getOutgoSum(Data.getMethodData(monthly_data, m.pk))
        methods_monthly_iob.append(InOutBalance(m, i, o, None))

    total_income = Data.getIncomeSum(
        Data.getNormalData(monthly_data)) - monthly_temp_and_deposit
    total_outgo = Data.getOutgoSum(Data.getNormalData(
        monthly_data)) - monthly_temp_and_deposit

    living_data = Data.getLivingData(monthly_data)
    living_outgo = Data.getOutgoSum(living_data) - Data.getTempSum(living_data)

    variable_data = Data.getVariableData(monthly_data)
    variable_outgo = Data.getOutgoSum(
        variable_data) - Data.getTempSum(variable_data)

    monthly_data_without_inmove = Data.getDataWithoutInmove(monthly_data)

    content = {
        'total_balance':
            Data.getIncomeSum(all_data) - Data.getOutgoSum(all_data),
        'methods_iob': methods_iob,
        'total_income': total_income,
        'total_outgo': total_outgo,
        'total_inout': total_income - total_outgo,
        'variable_outgo': variable_outgo,
        'living_outgo': living_outgo,
        'variable_remain': total_income - max(SeveralCosts.getLivingCostMark(),
                                              living_outgo) - variable_outgo,
        'all_income': Data.getIncomeSum(monthly_data_without_inmove),
        'all_outgo': Data.getOutgoSum(monthly_data_without_inmove),
        'methods_monthly_iob': methods_monthly_iob,
    }
    return render(request, '_balance_statisticMini.html', content)


def index_chart_data(request):
    # 今月のデータ
    monthly_data = get_monthly_data_from_get_parameter(request.GET)
    # ジャンルごとの支出
    positive_categories_outgo = {}
    for g in Category.list():
        if g.show_order >= 0:
            d = Data.getCategoryData(monthly_data, g.pk)
            positive_categories_outgo[g] = Data.getOutgoSum(
                d) - Data.getTempSum(d)
    content = {
        'categories_outgo': positive_categories_outgo,
    }
    return render(request, '_chart_container_data.html', content)


def data_table(request):
    # 今月のデータ
    monthly_data = get_monthly_data_from_get_parameter(request.GET)

    content = {
        'show_data': monthly_data,
    }

    # 追加後のmonthlyテーブルを返す
    return render(request, '_data_table.html', content)
