import json
from datetime import date, datetime

from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views import View
from moneybook.forms import DataForm, IntraMoveForm
from moneybook.models import (
    BankBalance, Category, CheckedDate, CreditCheckedDate, Data, Direction,
    InOutBalance, Method, SeveralCosts
)
from moneybook.utils import is_valid_date


class AddApiView(View):
    def post(self, request, *args, **kwargs):
        new_data = DataForm(request.POST)
        if new_data.is_valid():
            # データ追加
            new_data.save()
            # 成功レスポンス
            return HttpResponse()

        else:
            error_list = []
            for a in new_data.errors:
                error_list.append(a)
            res_data = {
                'ErrorList': error_list,
            }
            return HttpResponseBadRequest(json.dumps(res_data))


class AddIntraMoveApiView(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = IntraMoveForm(request.POST)
        if form.is_valid():
            try:
                out_data = Data()
                out_data.date = date(int(request.POST.get('year')), int(
                    request.POST.get('month')), int(request.POST.get('day')))
                out_data.price = request.POST.get('price')
                out_data.direction = Direction.get(2)
                out_data.method = Method.get(request.POST.get('before_method'))
                out_data.category = Category.get_intra_move()
                out_data.temp = False
                out_data.item = request.POST.get('item')

                in_data = Data()
                in_data.date = date(int(request.POST.get('year')), int(
                    request.POST.get('month')), int(request.POST.get('day')))
                in_data.price = request.POST.get('price')
                in_data.direction = Direction.get(1)
                in_data.method = Method.get(request.POST.get('after_method'))
                in_data.category = Category.get_intra_move()
                in_data.temp = False
                in_data.item = request.POST.get('item')

                # 保存
                out_data.save()
                in_data.save()

                # 成功レスポンス
                return HttpResponse()

            except:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class SuggestApiView(View):
    def get(self, request, *args, **kwargs):
        if 'item' not in request.GET:
            res = {'message': 'missing item'}
            return HttpResponseBadRequest(json.dumps(res))

        item = request.GET.get('item')
        if item == '':
            res = {'message': 'empty item'}
            return HttpResponseBadRequest(json.dumps(res))

        data = Data.sort_descending(
            Data.get_startswith_keyword_data(Data.get_all_data(), item))
        suggests = [{'date': v.date.strftime(
            '%Y-%m-%d'), 'item': v.item, 'price': v.price} for v in data]

        return HttpResponse(json.dumps({'suggests': suggests}))


class EditApiView(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']

        try:
            data = Data.get(pk)
        except:
            return HttpResponseBadRequest(json.dumps({'message': 'Data does not exist'}))

        new_data = DataForm(request.POST)
        if new_data.is_valid():
            # データ更新
            data.date = request.POST.get('date')
            data.item = request.POST.get('item')
            data.price = request.POST.get('price')
            data.direction = Direction.get(request.POST.get('direction'))
            data.method = Method.get(request.POST.get('method'))
            data.category = Category.get(request.POST.get('category'))
            data.temp = request.POST.get('temp')
            data.checked = request.POST.get('checked')
            data.save()

            return HttpResponse()
        else:
            res_data = {}
            error_list = []
            for a in new_data.errors:
                error_list.append(a)
            res_data['ErrorList'] = error_list
            return HttpResponseBadRequest(json.dumps(res_data))


class DeleteApiView(View):
    def post(self, request, *args, **kwargs):
        pk = request.POST.get('pk')

        try:
            Data.get(pk).delete()
        except:
            res = {'message': 'Data does not exist'}
            return HttpResponseBadRequest(json.dumps(res))

        return HttpResponse()


class ActualCashApiView(View):
    def post(self, request, *args, **kwargs):
        if 'price' not in request.POST:
            return HttpResponseBadRequest(json.dumps({'message': 'missing parameter'}))

        try:
            price = int(request.POST.get('price'))
        except ValueError:
            return HttpResponseBadRequest(json.dumps({'message': 'price must be int'}))

        SeveralCosts.set_actual_cash_balance(price)
        return HttpResponse()


class CheckedDateApiView(View):
    def get(self, request, *args, **kwargs):
        # 全データ
        all_data = Data.get_all_data()
        # 支払い方法リスト
        methods = Method.list()
        # 支払い方法ごとの残高
        methods_bd = []
        for m in methods:
            d = Data.get_method_data(all_data, m.pk)
            # 銀行はチェック済みだけ
            if m.pk == Method.get_bank().pk:
                d = Data.get_checked_data(d)
            methods_bd.append({
                'pk': m.pk,
                'name': m.name,
                'balance': Data.get_income_sum(d) - Data.get_outgo_sum(d),
                'year': CheckedDate.get(m.pk).date.year,
                'month': CheckedDate.get(m.pk).date.month,
                'day': CheckedDate.get(m.pk).date.day
            })

        return HttpResponse(json.dumps(methods_bd))

    def post(self, request, *args, **kwargs):
        if 'year' not in request.POST or 'month' not in request.POST or 'day' not in request.POST or 'method' not in request.POST:
            return HttpResponseBadRequest(json.dumps({'message': 'missing parameter'}))

        method_pk = request.POST.get('method')
        try:
            new_date = date(int(request.POST.get('year')), int(
                request.POST.get('month')), int(request.POST.get('day')))

            # 指定日以前のを全部チェック
            if 'check_all' in request.POST and request.POST.get('check_all') == '1':
                Data.filter_checkeds(Data.get_method_data(Data.get_range_data(
                    None, new_date), method_pk), [False]).update(checked=True)
        except ValueError:
            return HttpResponseBadRequest(json.dumps({'message': 'date format is invalid'}))

        try:
            # チェック日を更新
            CheckedDate.set(method_pk, new_date)
        except CheckedDate.DoesNotExist:
            return HttpResponseBadRequest(json.dumps({'message': 'method id is invalid'}))

        return HttpResponse()


class CreditCheckedDateApiView(View):
    def post(self, request, *args, **kwargs):
        if 'year' not in request.POST or 'month' not in request.POST or 'day' not in request.POST or 'pk' not in request.POST:
            return HttpResponseBadRequest(json.dumps({'message': 'missing parameter'}))

        pk = request.POST.get('pk')
        try:
            new_date = date(int(request.POST.get('year')), int(
                request.POST.get('month')), int(request.POST.get('day')))
        except ValueError:
            return HttpResponseBadRequest(json.dumps({'message': 'date format is invalid'}))

        try:
            # 更新
            CreditCheckedDate.set_date(pk, new_date)
        except CreditCheckedDate.DoesNotExist:
            return HttpResponseBadRequest(json.dumps({'message': 'method id is invalid'}))

        return HttpResponse()


class LivingCostMarkApiView(View):
    def post(self, request, *args, **kwargs):
        if 'price' not in request.POST:
            return HttpResponseBadRequest(json.dumps({'message': 'missing parameter'}))

        try:
            price = int(request.POST.get('price'))
        except ValueError:
            return HttpResponseBadRequest(json.dumps({'message': 'price must be int'}))

        SeveralCosts.set_living_cost_mark(price)
        return HttpResponse(json.dumps({'message': 'success'}))


class NowBankApiView(View):
    def post(self, request, *args, **kwargs):
        written_bank_data = Data.get_checked_data(
            Data.get_bank_data(Data.get_all_data()))
        bank_sum = 0
        bb = BankBalance.get_all()
        cc = CreditCheckedDate.get_all()

        # フォーマットチェック
        try:
            for b in bb:
                key = 'bank-' + str(b.pk)
                if key in request.POST:
                    int(request.POST.get(key))

            for c in cc:
                key = 'credit-' + str(c.pk)
                if key in request.POST:
                    int(request.POST.get(key))
        except ValueError:
            return HttpResponseBadRequest(json.dumps({'message': 'invalid parameter'}))

        # 更新と計算
        for b in bb:
            key = 'bank-' + str(b.pk)
            if key in request.POST:
                value = int(request.POST.get(key))
                BankBalance.set(b.pk, value)
            bank_sum += BankBalance.get_price(b.pk)

        for c in cc:
            key = 'credit-' + str(c.pk)
            if key in request.POST:
                value = int(request.POST.get(key))
                CreditCheckedDate.set_price(c.pk, value)
            bank_sum -= CreditCheckedDate.get_price(c.pk)
        return HttpResponse(
            json.dumps({'balance': Data.get_income_sum(written_bank_data) - Data.get_outgo_sum(written_bank_data) - bank_sum}))


class ApplyCheckApiView(View):
    def post(self, request, *args, **kwargs):

        all_data = Data.get_all_data()
        unchecked_data = Data.get_unchecked_data(all_data)
        pre_checked_data = Data.get_pre_checked_data(unchecked_data)

        for data in pre_checked_data:
            data.pre_checked = False
            data.checked = True
            data.save()

        return HttpResponse()


class PreCheckApiView(View):
    def post(self, request, *args, **kwargs):
        pk = request.POST.get('id')
        status = request.POST.get('status')

        try:
            data = Data.get(pk)
        except:
            res = {'message': 'Data does not exist'}
            return HttpResponseBadRequest(json.dumps(res))

        if status == '1':
            data.pre_checked = True
        else:
            data.pre_checked = False
        data.save()
        return HttpResponse()


class IndexBalanceStatisticMiniApiView(View):
    def get(self, request, *args, **kwargs):
        # validation
        if 'year' in request.GET and 'month' in request.GET:
            year = request.GET.get('year')
            month = request.GET.get('month')
            if not is_valid_date(year, month):
                return HttpResponseBadRequest('parameter error')
        else:
            return HttpResponseBadRequest('parameter error')

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
            methods_iob.append(InOutBalance(
                m.name, None, None, Data.get_income_sum(d) - Data.get_outgo_sum(d)))

            i = Data.get_income_sum(Data.get_method_data(monthly_data, m.pk))
            o = Data.get_outgo_sum(Data.get_method_data(monthly_data, m.pk))
            methods_monthly_iob.append(InOutBalance(m.name, i, o, None))

        # 貯金合計
        monthly_deposit_sum = Data.get_deposit_sum(monthly_data)
        # 貯金の支出分合計
        monthly_deposit_outgo_sum = Data.get_deposit_outgo_sum(monthly_data)
        # 通常データ
        monthly_normal_data = Data.get_normal_data(monthly_data)
        # 立替合計
        tmp_sum = Data.get_temp_sum(monthly_normal_data)
        # 今月の収入
        monthly_income = Data.get_income_sum(
            monthly_normal_data) - monthly_deposit_outgo_sum - tmp_sum
        # 今月の支出
        monthly_outgo = Data.get_outgo_sum(
            monthly_normal_data) - monthly_deposit_outgo_sum - tmp_sum
        # 生活費
        living_cost = Data.get_living_cost(monthly_data)
        # 変動費
        variable_cost = Data.get_variable_cost(monthly_data)
        # 生活費目標額
        living_cost_mark = SeveralCosts.get_living_cost_mark()
        # 内部移動以外
        monthly_data_without_inmove = Data.filter_without_intra_move(
            monthly_data)

        context = {
            'total_balance': Data.get_income_sum(all_data) - Data.get_outgo_sum(all_data),
            'methods_iob': methods_iob,
            'monthly_income': monthly_income,
            'monthly_outgo': monthly_outgo,
            'monthly_inout': monthly_income - monthly_outgo,
            'deposit': monthly_deposit_sum,
            'living_cost': living_cost,
            'variable_cost': variable_cost,
            'living_remain': living_cost_mark - living_cost,
            'variable_remain': monthly_income - max(SeveralCosts.get_living_cost_mark(), living_cost) - variable_cost,
            'monthly_all_income': Data.get_income_sum(monthly_data_without_inmove),
            'monthly_all_outgo': Data.get_outgo_sum(monthly_data_without_inmove),
            'methods_monthly_iob': methods_monthly_iob,
        }
        return render(request, '_balance_statistic_mini.html', context)


class IndexChartDataApiView(View):
    def get(self, request, *args, **kwargs):
        # validation
        if 'year' in request.GET and 'month' in request.GET:
            year = request.GET.get('year')
            month = request.GET.get('month')
            if not is_valid_date(year, month):
                return HttpResponseBadRequest('parameter error')
        else:
            return HttpResponseBadRequest('parameter error')

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


class DataTableApiView(View):
    def get(self, request, *args, **kwargs):
        # validation
        if 'year' in request.GET and 'month' in request.GET:
            year = request.GET.get('year')
            month = request.GET.get('month')
            if not is_valid_date(year, month):
                return HttpResponseBadRequest('parameter error')
        else:
            return HttpResponseBadRequest('parameter error')

        # 今月のデータ
        monthly_data = Data.sort_descending(
            Data.get_month_data(int(year), int(month)))

        context = {
            'show_data': monthly_data,
        }

        # 追加後のmonthlyテーブルを返す
        return render(request, '_data_table.html', context)


class SeveralCheckedDateApiView(View):
    def get(self, request, *args, **kwargs):
        now = datetime.now()
        # 全データ
        all_data = Data.get_all_data()
        # 現在銀行
        banks = BankBalance.get_all()
        # クレカ確認日
        credit_checked_date = CreditCheckedDate.get_all()
        today = date.today()
        for c in credit_checked_date:
            # 日付が過ぎていたらpriceを0にする
            if c.date <= today:
                c.price = 0

        # 銀行残高
        all_bank_data = Data.get_bank_data(all_data)
        checked_bank_data = Data.get_checked_data(all_bank_data)
        bank_written = Data.get_income_sum(
            checked_bank_data) - Data.get_outgo_sum(checked_bank_data)

        context = {
            'year': now.year,
            'banks': banks,
            'credit_checked_date': credit_checked_date,
            'bank_written': bank_written,
        }
        return render(request, '_several_checked_date.html', context)


class UncheckedDataApiView(View):
    def get(self, request, *args, **kwargs):
        # 全データ
        all_data = Data.get_all_data()
        # 未承認トランザクション
        unchecked_data = Data.get_unchecked_data(all_data)
        context = {
            'unchecked_data': unchecked_data,
        }
        return render(request, '_unchecked_data.html', context)


class PreCheckedSummaryApiView(View):
    def get(self, request, *args, **kwargs):
        # 全データ
        all_data = Data.get_all_data()
        # 未承認トランザクション
        unchecked_data = Data.get_unchecked_data(all_data)
        pre_checked_data = Data.get_pre_checked_data(unchecked_data)

        context = {
            'income_sum': Data.get_income_sum(pre_checked_data),
            'outgo_sum': Data.get_outgo_sum(pre_checked_data),
            'income_count': len(Data.get_income(pre_checked_data)),
            'outgo_count': len(Data.get_outgo(pre_checked_data)),
        }
        return render(request, '_pre_checked_summary.html', context)
