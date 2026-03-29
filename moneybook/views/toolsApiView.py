import http
from datetime import date

from django.http import JsonResponse
from django.views import View
from moneybook.models import BankBalance, CheckedDate, CreditCheckedDate, Data, Method, SeveralCosts


class ActualCashApiView(View):
    def post(self, request, *args, **kwargs):
        if 'price' not in request.POST:
            return JsonResponse({'message': 'missing parameter'}, status=http.HTTPStatus.BAD_REQUEST)

        try:
            price = int(request.POST.get('price'))
        except ValueError:
            return JsonResponse({'message': 'price must be int'}, status=http.HTTPStatus.BAD_REQUEST)

        SeveralCosts.set_actual_cash_balance(price)
        return JsonResponse({})


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

        return JsonResponse({'methods_bd': methods_bd})

    def post(self, request, *args, **kwargs):
        if 'year' not in request.POST or 'month' not in request.POST or 'day' not in request.POST or 'method' not in request.POST:
            return JsonResponse({'message': 'missing parameter'}, status=http.HTTPStatus.BAD_REQUEST)

        method_pk = request.POST.get('method')
        try:
            new_date = date(int(request.POST.get('year')), int(
                request.POST.get('month')), int(request.POST.get('day')))

            # 指定日以前のを全部チェック
            if 'check_all' in request.POST and request.POST.get('check_all') == '1':
                Data.filter_checkeds(Data.get_method_data(Data.get_range_data(
                    None, new_date), method_pk), [False]).update(checked=True)
        except ValueError:
            return JsonResponse({'message': 'date format is invalid'}, status=http.HTTPStatus.BAD_REQUEST)

        try:
            # チェック日を更新
            CheckedDate.set(method_pk, new_date)
        except CheckedDate.DoesNotExist:
            return JsonResponse({'message': 'method id is invalid'}, status=http.HTTPStatus.BAD_REQUEST)

        return JsonResponse({})


class CreditCheckedDateApiView(View):
    def post(self, request, *args, **kwargs):
        if 'year' not in request.POST or 'month' not in request.POST or 'day' not in request.POST or 'pk' not in request.POST:
            return JsonResponse({'message': 'missing parameter'}, status=http.HTTPStatus.BAD_REQUEST)

        pk = request.POST.get('pk')
        try:
            new_date = date(int(request.POST.get('year')), int(
                request.POST.get('month')), int(request.POST.get('day')))
        except ValueError:
            return JsonResponse({'message': 'date format is invalid'}, status=http.HTTPStatus.BAD_REQUEST)

        try:
            # 更新
            CreditCheckedDate.set_date(pk, new_date)
        except CreditCheckedDate.DoesNotExist:
            return JsonResponse({'message': 'method id is invalid'}, status=http.HTTPStatus.BAD_REQUEST)

        return JsonResponse({})


class LivingCostMarkApiView(View):
    def post(self, request, *args, **kwargs):
        if 'price' not in request.POST:
            return JsonResponse({'message': 'missing parameter'}, status=http.HTTPStatus.BAD_REQUEST)

        try:
            price = int(request.POST.get('price'))
        except ValueError:
            return JsonResponse({'message': 'price must be int'}, status=http.HTTPStatus.BAD_REQUEST)

        SeveralCosts.set_living_cost_mark(price)
        return JsonResponse({'message': 'success'})


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
            return JsonResponse({'message': 'invalid parameter'}, status=http.HTTPStatus.BAD_REQUEST)

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
        return JsonResponse(
            {'balance': Data.get_income_sum(written_bank_data) - Data.get_outgo_sum(written_bank_data) - bank_sum})
