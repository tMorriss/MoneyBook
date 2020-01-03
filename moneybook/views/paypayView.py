from django.conf import settings
from django.shortcuts import render
from moneybook.models import *
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

def paypay(request):
    now = datetime.now()
    lastMonth = now - relativedelta(months=1)
    content = {
        'app_name': settings.APP_NAME,
        'username': request.user,
        'year': lastMonth.year,
        'month': lastMonth.month,
    }
    return render(request, 'paypay.html', content)

def recent_paypay_income_table(request):
    # 先月の頭以降
    now = datetime.now()
    lastMonth = now - relativedelta(months=1)
    recentData = Data.getRangeData(date(lastMonth.year, lastMonth.month, 1), None)
    # 直近のPayPay関係
    paypayData = Data.sortDateDescending(Data.getPayPayData(recentData))
    paypayIncome = Data.filterDirections(paypayData, '1')

    content = {
        'show_data': paypayIncome,
    }

    return render(request, '_data_table.html', content)