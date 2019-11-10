from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from datetime import date, datetime
from moneybook.models import *
import json

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
        'username': request.user,
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
    return render(request, "tools.html", content)

def update_actual_cash(request):
    if not "price" in request.POST:
        return HttpResponseBadRequest(json.dumps({"message": "missing parameter"}))

    try:
        price = int(request.POST.get("price"))
    except:
        return HttpResponseBadRequest(json.dumps({"message": "price must be int"}))

    SeveralCosts.setActualCashBalance(price)
    return HttpResponse(json.dumps({"message": "success"}))

def update_checked_date(request):
    if not "year" in request.POST or not "month" in request.POST or not "day" in request.POST or not "method" in request.POST:
        return HttpResponseBadRequest(json.dumps({"message": "missing parameter"}))

    methodPk = request.POST.get("method")
    try:
        newDate = date(int(request.POST.get("year")), int(request.POST.get("month")), int(request.POST.get("day")))

        # 指定日以前のを全部チェック
        if "check_all" in request.POST and request.POST.get("check_all") == "1":
            Data.filterCheckeds(Data.getMethodData(Data.getRangeData(None, newDate), methodPk), [False]).update(checked=True)
    except:
        return HttpResponseBadRequest(json.dumps({"message": "date format is invalid"}))

    try:    
        # チェック日を更新
        CheckedDate.set(methodPk, newDate)
    except:
        return HttpResponseBadRequest(json.dumps({"message": "method id is invalid"}))

    return HttpResponse(json.dumps({"message": "success"}))

def update_credit_checked_date(request):
    if not "year" in request.POST or not "month" in request.POST or not "day" in request.POST or not "pk" in request.POST:
        return HttpResponseBadRequest(json.dumps({"message": "missing parameter"}))

    pk = request.POST.get("pk")
    try:
        newDate = date(int(request.POST.get("year")), int(request.POST.get("month")), int(request.POST.get("day")))
    except:
        return HttpResponseBadRequest(json.dumps({"message": "date format is invalid"}))

    try:
        # 更新
        CreditCheckedDate.setDate(pk, newDate)
    except:
        return HttpResponseBadRequest(json.dumps({"message": "method id is invalid"}))
    
    return HttpResponse(json.dumps({"message": "success"}))
    
def update_cacheback_checked_date(request):
    if not "year" in request.POST or not "month" in request.POST or not "day" in request.POST or not "pk" in request.POST:
        return HttpResponseBadRequest(json.dumps({"message": "missing parameter"}))

    pk = request.POST.get("pk")
    try:
        newDate = date(int(request.POST.get("year")), int(request.POST.get("month")), int(request.POST.get("day")))
    except:
        return HttpResponseBadRequest(json.dumps({"message": "date format is invalid"}))

    try:
        # 更新
        CachebackCheckedDate.set(pk, newDate)
    except:
        return HttpResponseBadRequest(json.dumps({"message": "method id is invalid"}))
    
    return HttpResponse(json.dumps({"message": "success"}))

def update_fixed_cost_mark(request):
    if not "price" in request.POST:
        return HttpResponseBadRequest(json.dumps({"message": "missing parameter"}))

    try:
        price = int(request.POST.get("price"))
    except:
        return HttpResponseBadRequest(json.dumps({"message": "price must be int"}))

    SeveralCosts.setFixedCostMark(price)
    return HttpResponse(json.dumps({"message": "success"}))

def calculate_now_bank(request):
    bankSum = 0
    bb = BankBalance.getAll()
    cc = CreditCheckedDate.getAll()
    try:
        for b in bb:
            key = "bank-" + str(b.pk)
            if key in request.POST:
                value = int(request.POST.get(key))
                BankBalance.set(b.pk, value)
                bankSum += value
            
        for c in cc:
            key = "credit-" + str(c.pk)
            if key in request.POST:
                value = int(request.POST.get(key))
                CreditCheckedDate.setPrice(c.pk, value)
                bankSum -= value
    except:
        return HttpResponseBadRequest(json.dumps({"message": "invalid parameter"}))

    return HttpResponse(json.dumps({"balance": bankSum}))
