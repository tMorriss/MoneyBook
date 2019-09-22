from django.conf import settings
from django.shortcuts import render
from datetime import datetime
from web.models import *

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
