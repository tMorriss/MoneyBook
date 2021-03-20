from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.shortcuts import render
from moneybook.models import (Category, Data, Direction, InOutBalance, Method,
                              SeveralCosts)


def _get_monthly_data_from_get_parameter(request_get):
    if "year" in request_get and "month" in request_get:
        year = request_get.get("year")
        month = request_get.get("month")

    monthly_data = Data.sort_data_descending(
        Data.get_month_data(int(year), int(month)))
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

    context = {
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
        'unused_methods': Method.un_used_list(),
        'first_categories': Category.first_list(),
        'latter_categories': Category.latter_list(),
    }
    return render(request, 'index.html', context)


def index_balance_statistic_mini(request):
    # 全データ
    all_data = Data.get_all_data()
    # 今月のデータ
    monthly_data = _get_monthly_data_from_get_parameter(request.GET)
    # 支払い方法リスト
    methods = Method.list()
    # 立替と貯金
    monthly_temp_and_deposit = Data.get_temp_and_deposit_sum(monthly_data)

    # 支払い方法ごとの残高
    methods_iob = []
    methods_monthly_iob = []
    for m in methods:
        d = Data.get_method_data(all_data, m.pk)
        methods_iob.append(InOutBalance(
            m, None, None, Data.get_income_sum(d) - Data.get_outgo_sum(d)))

        i = Data.get_income_sum(Data.get_method_data(monthly_data, m.pk))
        o = Data.get_outgo_sum(Data.get_method_data(monthly_data, m.pk))
        methods_monthly_iob.append(InOutBalance(m, i, o, None))

    total_income = Data.get_income_sum(
        Data.get_normal_data(monthly_data)) - monthly_temp_and_deposit
    total_outgo = Data.get_outgo_sum(Data.get_normal_data(
        monthly_data)) - monthly_temp_and_deposit

    living_cost = Data.get_living_cost(monthly_data)

    variable_cost = Data.get_variable_cost(monthly_data)

    monthly_data_without_inmove = Data.get_data_without_intra_move(
        monthly_data)

    context = {
        'total_balance':
            Data.get_income_sum(all_data) - Data.get_outgo_sum(all_data),
        'methods_iob': methods_iob,
        'total_income': total_income,
        'total_outgo': total_outgo,
        'total_inout': total_income - total_outgo,
        'variable_cost': variable_cost,
        'living_cost': living_cost,
        'variable_remain': total_income - max(SeveralCosts.get_living_cost_mark(),
                                              living_cost) - variable_cost,
        'all_income': Data.get_income_sum(monthly_data_without_inmove),
        'all_outgo': Data.get_outgo_sum(monthly_data_without_inmove),
        'methods_monthly_iob': methods_monthly_iob,
    }
    return render(request, '_balance_statisticMini.html', context)


def index_chart_data(request):
    # 今月のデータ
    monthly_data = _get_monthly_data_from_get_parameter(request.GET)
    # ジャンルごとの支出
    positive_categories_outgo = {}
    for g in Category.list():
        if g.show_order >= 0:
            d = Data.get_category_data(monthly_data, g.pk)
            positive_categories_outgo[g] = Data.get_outgo_sum(
                d) - Data.get_temp_sum(d)
    context = {
        'categories_outgo': positive_categories_outgo,
    }
    return render(request, '_chart_container_data.html', context)


def data_table(request):
    # 今月のデータ
    monthly_data = _get_monthly_data_from_get_parameter(request.GET)

    context = {
        'show_data': monthly_data,
    }

    # 追加後のmonthlyテーブルを返す
    return render(request, '_data_table.html', context)
