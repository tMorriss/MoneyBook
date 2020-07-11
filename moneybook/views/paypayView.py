from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from moneybook.models import Data, CachebackCheckedDate
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import json


def paypay(request):
    now = datetime.now()
    last_month = now - relativedelta(months=1)
    # 全データ
    all_data = Data.getAllData()
    # PayPayデータ
    paypay_data = Data.getMethodData(all_data, 5)
    # PayPay残高
    paypay_balance = Data.getIncomeSum(
        paypay_data) - Data.getOutgoSum(paypay_data)

    # キャッシュバック確認日
    cacheback_date = CachebackCheckedDate.get(1).date

    content = {
        'app_name': settings.APP_NAME,
        'username': request.user,
        'year': last_month.year,
        'month': last_month.month,
        'balance': paypay_balance,
        'cacheback_year': cacheback_date.year,
        'cacheback_month': cacheback_date.month,
        'cacheback_day': cacheback_date.day,
    }
    return render(request, 'paypay.html', content)


def recent_paypay_income_table(request):
    # 先々月の頭以降
    now = datetime.now()
    last_month = now - relativedelta(months=2)
    recent_data = Data.getRangeData(
        date(last_month.year, last_month.month, 1), None)
    # 直近のPayPay関係
    paypay_data = Data.sortDateDescending(Data.getPayPayData(recent_data))
    paypay_income = Data.filterDirections(paypay_data, '1')

    content = {
        'show_data': paypay_income,
    }

    return render(request, '_data_table.html', content)


def get_paypay_bakance(request):
    # 全データ
    all_data = Data.getAllData()
    # PayPayデータ
    paypay_data = Data.getMethodData(all_data, 5)
    # PayPay残高
    paypay_balance = Data.getIncomeSum(
        paypay_data) - Data.getOutgoSum(paypay_data)

    content = {
        'balance': paypay_balance,
    }
    return HttpResponse(json.dumps(content))
