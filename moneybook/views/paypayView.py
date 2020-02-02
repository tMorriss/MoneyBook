from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from moneybook.models import *
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import json

def paypay(request):
    now = datetime.now()
    lastMonth = now - relativedelta(months=1)
    # 全データ
    allData = Data.getAllData()
    # PayPayデータ
    paypayData = Data.getMethodData(allData, 5)
    # PayPay残高
    paypayBalance = Data.getIncomeSum(paypayData) - Data.getOutgoSum(paypayData)

    # キャッシュバック確認日
    cachebackDate = CachebackCheckedDate.get(1).date

    content = {
        'app_name': settings.APP_NAME,
        'username': request.user,
        'year': lastMonth.year,
        'month': lastMonth.month,
        'balance': paypayBalance,
        'cacheback_year': cachebackDate.year,
        'cacheback_month': cachebackDate.month,
        'cacheback_day': cachebackDate.day,
    }
    return render(request, 'paypay.html', content)

def recent_paypay_income_table(request):
    # 先々月の頭以降
    now = datetime.now()
    lastMonth = now - relativedelta(months=2)
    recentData = Data.getRangeData(date(lastMonth.year, lastMonth.month, 1), None)
    # 直近のPayPay関係
    paypayData = Data.sortDateDescending(Data.getPayPayData(recentData))
    paypayIncome = Data.filterDirections(paypayData, '1')

    content = {
        'show_data': paypayIncome,
    }

    return render(request, '_data_table.html', content)

def get_paypay_bakance(request):
    # 全データ
    allData = Data.getAllData()
    # PayPayデータ
    paypayData = Data.getMethodData(allData, 5)
    # PayPay残高
    paypayBalance = Data.getIncomeSum(paypayData) - Data.getOutgoSum(paypayData)

    content = {
        'balance': paypayBalance,
    }
    return HttpResponse(json.dumps(content))