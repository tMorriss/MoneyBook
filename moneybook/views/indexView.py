from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views import View
from moneybook.models import Category, Data, Direction, InOutBalance, Method, SeveralCosts
from moneybook.utils import is_valid_date


class IndexView(View):
    def get(self, request, *args, **kwargs):
        now = datetime.now()
        year = now.year
        month = now.month
        return IndexMonthView().get(request=request, year=year, month=month)


class IndexMonthView(View):
    def get(self, request, *args, **kwargs):
        year = kwargs["year"]
        month = kwargs["month"]
        # validation
        if not is_valid_date(year, month):
            return HttpResponseBadRequest("parameter error")
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
            'methods': Method.list(),
            'unused_methods': Method.un_used_list(),
            'first_categories': Category.first_list(),
            'latter_categories': Category.latter_list(),
        }
        return render(request, 'index.html', context)


class IndexBalanceStatisticMiniView(View):
    def get(self, request, *args, **kwargs):
        # validation
        if "year" in request.GET and "month" in request.GET:
            year = request.GET.get("year")
            month = request.GET.get("month")
            if not is_valid_date(year, month):
                return HttpResponseBadRequest("parameter error")
        else:
            return HttpResponseBadRequest("parameter error")

        # 全データ
        all_data = Data.get_all_data()
        # 今月のデータ
        monthly_data = Data.get_month_data(int(year), int(month))
        # 支払い方法リスト
        methods = Method.list()
        # 支払い方法ごとの残高
        methods_iob = []
        methods_monthly_iob = []
        for m in methods:
            d = Data.get_method_data(all_data, m.pk)
            methods_iob.append(InOutBalance(m.name, None, None, Data.get_income_sum(d) - Data.get_outgo_sum(d)))

            i = Data.get_income_sum(Data.get_method_data(monthly_data, m.pk))
            o = Data.get_outgo_sum(Data.get_method_data(monthly_data, m.pk))
            methods_monthly_iob.append(InOutBalance(m.name, i, o, None))

        # 立替と貯金
        monthly_temp_and_deposit = Data.get_temp_and_deposit_sum(monthly_data)
        # 通常データ
        monthly_normal_data = Data.get_normal_data(monthly_data)
        # 今月の収入
        monthly_income = Data.get_income_sum(monthly_normal_data) - monthly_temp_and_deposit
        # 今月の支出
        monthly_outgo = Data.get_outgo_sum(monthly_normal_data) - monthly_temp_and_deposit
        # 生活費
        living_cost = Data.get_living_cost(monthly_data)
        # 変動費
        variable_cost = Data.get_variable_cost(monthly_data)
        # 生活費目標額
        living_cost_mark = SeveralCosts.get_living_cost_mark()
        # 内部移動以外
        monthly_data_without_inmove = Data.filter_without_intra_move(monthly_data)

        context = {
            'total_balance': Data.get_income_sum(all_data) - Data.get_outgo_sum(all_data),
            'methods_iob': methods_iob,
            'monthly_income': monthly_income,
            'monthly_outgo': monthly_outgo,
            'monthly_inout': monthly_income - monthly_outgo,
            'living_cost': living_cost,
            'variable_cost': variable_cost,
            'living_remain': living_cost_mark - living_cost,
            'variable_remain': monthly_income - max(SeveralCosts.get_living_cost_mark(), living_cost) - variable_cost,
            'monthly_all_income': Data.get_income_sum(monthly_data_without_inmove),
            'monthly_all_outgo': Data.get_outgo_sum(monthly_data_without_inmove),
            'methods_monthly_iob': methods_monthly_iob,
        }
        return render(request, '_balance_statistic_mini.html', context)


class IndexChartDataView(View):
    def get(self, request, *args, **kwargs):
        # validation
        if "year" in request.GET and "month" in request.GET:
            year = request.GET.get("year")
            month = request.GET.get("month")
            if not is_valid_date(year, month):
                return HttpResponseBadRequest("parameter error")
        else:
            return HttpResponseBadRequest("parameter error")

        # 今月のデータ
        monthly_data = Data.get_month_data(int(year), int(month))
        # ジャンルごとの支出
        positive_categories_outgo = {}
        for c in Category.list():
            if c.show_order >= 0:
                d = Data.get_category_data(monthly_data, c.pk)
                positive_categories_outgo[c.name] = Data.get_outgo_sum(
                    d) - Data.get_temp_sum(d)
        context = {
            'categories_outgo': positive_categories_outgo,
        }
        return render(request, '_chart_container_data.html', context)


class DataTableView(View):
    def get(self, request, *args, **kwargs):
        # validation
        if "year" in request.GET and "month" in request.GET:
            year = request.GET.get("year")
            month = request.GET.get("month")
            if not is_valid_date(year, month):
                return HttpResponseBadRequest("parameter error")
        else:
            return HttpResponseBadRequest("parameter error")

        # 今月のデータ
        monthly_data = Data.sort_descending(
            Data.get_month_data(int(year), int(month)))

        context = {
            'show_data': monthly_data,
        }

        # 追加後のmonthlyテーブルを返す
        return render(request, '_data_table.html', context)
