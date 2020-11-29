from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from datetime import date, datetime
from moneybook.models import Method, Data, SeveralCosts, CheckedDate
from moneybook.models import CreditCheckedDate, CachebackCheckedDate
from moneybook.models import BankBalance
import json


def tools(request):
    now = datetime.now()
    # 実際の現金残高
    actual_cash_balance = SeveralCosts.getActualCashBalance()
    # クレカ確認日
    credit_checked_date = CreditCheckedDate.getAll()
    # 銀行残高
    bank_balance = BankBalance.getAll()
    # 生活費目標額
    living_cost_mark = SeveralCosts.getLivingCostMark()
    # 現在銀行
    banks = BankBalance.getAll()

    content = {
        'app_name': settings.APP_NAME,
        'username': request.user,
        'cash_balance':
            Data.getIncomeSum(Data.getCashData(Data.getAllData()))
            - Data.getOutgoSum(Data.getCashData(Data.getAllData())),
        'year': now.year,
        'month': now.month,
        'day': now.day,
        'actual_cash_balance': actual_cash_balance,
        'credit_checked_date': credit_checked_date,
        'bank_balance': bank_balance,
        'living_cost_mark': living_cost_mark,
        'banks': banks,
    }
    return render(request, "tools.html", content)


def update_actual_cash(request):
    if "price" not in request.POST:
        return HttpResponseBadRequest(
            json.dumps({"message": "missing parameter"})
        )

    try:
        price = int(request.POST.get("price"))
    except ValueError:
        return HttpResponseBadRequest(
            json.dumps({"message": "price must be int"})
        )

    SeveralCosts.setActualCashBalance(price)
    return HttpResponse(json.dumps({"message": "success"}))


class CheckedDataView(View):
    def get(self, request, *args, **kwargs):
        # 全データ
        all_data = Data.getAllData()
        # 支払い方法リスト
        methods = Method.list()
        # 支払い方法ごとの残高
        methods_bd = []
        for m in methods:
            d = Data.getMethodData(all_data, m.pk)
            # 銀行はチェック済みだけ
            if m.pk == 2:
                d = Data.getCheckedData(d)
            methods_bd.append({
                'pk': m.pk,
                'name': m.name,
                'balance': Data.getIncomeSum(d) - Data.getOutgoSum(d),
                'year': CheckedDate.get(m.pk).date.year,
                'month': CheckedDate.get(m.pk).date.month,
                'day': CheckedDate.get(m.pk).date.day
            })

        return HttpResponse(json.dumps(methods_bd))

    def post(self, request, *args, **kwargs):
        if "year" not in request.POST or "month" not in request.POST \
                or "day" not in request.POST or "method" not in request.POST:
            return HttpResponseBadRequest(
                json.dumps({"message": "missing parameter"})
            )

        method_pk = request.POST.get("method")
        try:
            new_date = date(int(request.POST.get("year")), int(
                request.POST.get("month")), int(request.POST.get("day")))

            # 指定日以前のを全部チェック
            if "check_all" in request.POST and \
                    request.POST.get("check_all") == "1":
                Data.filterCheckeds(Data.getMethodData(Data.getRangeData(
                    None, new_date), method_pk), [False]).update(checked=True)
        except ValueError:
            return HttpResponseBadRequest(
                json.dumps({"message": "date format is invalid"})
            )

        try:
            # チェック日を更新
            CheckedDate.set(method_pk, new_date)
        except CheckedDate.DoesNotExist:
            return HttpResponseBadRequest(
                json.dumps({"message": "method id is invalid"})
            )

        return HttpResponse(json.dumps({"message": "success"}))


def get_several_checked_date(request):
    now = datetime.now()
    # 全データ
    all_data = Data.getAllData()
    # 現在銀行
    banks = BankBalance.getAll()
    # クレカ確認日
    credit_checked_date = CreditCheckedDate.getAll()
    today = date.today()
    for c in credit_checked_date:
        # 日付が過ぎていたらpriceを0にする
        if c.date <= today:
            c.price = 0

    # 銀行残高
    all_bank_data = Data.getBankData(all_data)
    checked_bank_data = Data.getCheckedData(all_bank_data)
    bank_written = Data.getIncomeSum(
        checked_bank_data) - Data.getOutgoSum(checked_bank_data)

    content = {
        'year': now.year,
        'banks': banks,
        'credit_checked_date': credit_checked_date,
        'bank_written': bank_written,
    }
    return render(request, "_several_checked_date.html", content)


def update_credit_checked_date(request):
    if "year" not in request.POST or "month" not in request.POST \
            or "day" not in request.POST or "pk" not in request.POST:
        return HttpResponseBadRequest(
            json.dumps({"message": "missing parameter"})
        )

    pk = request.POST.get("pk")
    try:
        new_date = date(int(request.POST.get("year")), int(
            request.POST.get("month")), int(request.POST.get("day")))
    except ValueError:
        return HttpResponseBadRequest(
            json.dumps({"message": "date format is invalid"})
        )

    try:
        # 更新
        CreditCheckedDate.setDate(pk, new_date)
    except CheckedDate.DoesNotExist:
        return HttpResponseBadRequest(
            json.dumps({"message": "method id is invalid"})
        )

    return HttpResponse(json.dumps({"message": "success"}))


def update_cacheback_checked_date(request):
    if "year" not in request.POST or "month" not in request.POST or "day" \
            not in request.POST or "pk" not in request.POST:
        return HttpResponseBadRequest(
            json.dumps({"message": "missing parameter"})
        )

    pk = request.POST.get("pk")
    try:
        new_date = date(int(request.POST.get("year")), int(
            request.POST.get("month")), int(request.POST.get("day")))
    except ValueError:
        return HttpResponseBadRequest(
            json.dumps({"message": "date format is invalid"})
        )

    try:
        # 更新
        CachebackCheckedDate.set(pk, new_date)
    except CheckedDate.DoesNotExist:
        return HttpResponseBadRequest(
            json.dumps({"message": "method id is invalid"})
        )

    return HttpResponse(json.dumps({"message": "success"}))


def update_living_cost_mark(request):
    if "price" not in request.POST:
        return HttpResponseBadRequest(
            json.dumps({"message": "missing parameter"})
        )

    try:
        price = int(request.POST.get("price"))
    except ValueError:
        return HttpResponseBadRequest(
            json.dumps({"message": "price must be int"})
        )

    SeveralCosts.setLivingCostMark(price)
    return HttpResponse(json.dumps({"message": "success"}))


def get_unchecked_transaction(request):
    # 全データ
    all_data = Data.getAllData()
    # 未承認トランザクション
    unchecked_data = Data.getUncheckedData(all_data)
    content = {
        'unchecked_data': unchecked_data,
    }
    return render(request, "_unchecked_transaction.html", content)


def update_now_bank(request):
    written_bank_data = Data.getCheckedData(
        Data.getBankData(Data.getAllData()))
    bank_sum = 0
    bb = BankBalance.getAll()
    cc = CreditCheckedDate.getAll()
    try:
        for b in bb:
            key = "bank-" + str(b.pk)
            if key in request.POST:
                value = int(request.POST.get(key))
                BankBalance.set(b.pk, value)
                bank_sum += value

        for c in cc:
            key = "credit-" + str(c.pk)
            if key in request.POST:
                value = int(request.POST.get(key))
                CreditCheckedDate.setPrice(c.pk, value)
                bank_sum -= value
    except ValueError:
        return HttpResponseBadRequest(
            json.dumps({"message": "invalid parameter"})
        )

    return HttpResponse(
        json.dumps({"balance": Data.getIncomeSum(written_bank_data)
                    - Data.getOutgoSum(written_bank_data) - bank_sum})
    )
