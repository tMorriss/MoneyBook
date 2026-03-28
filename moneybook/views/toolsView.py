import json
from datetime import date, datetime

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views import View
from moneybook.models import BankBalance, CheckedDate, CreditCheckedDate, Data, Method, SeveralCosts


class ToolsView(View):
    def get(self, request, *args, **kwargs):
        now = datetime.now()
        # 実際の現金残高
        actual_cash_balance = SeveralCosts.get_actual_cash_balance()
        # クレカ確認日
        credit_checked_date = CreditCheckedDate.get_all()
        # 生活費目標額
        living_cost_mark = SeveralCosts.get_living_cost_mark()

        context = {
            'app_name': settings.APP_NAME,
            'username': request.user,
            'cash_balance':
                Data.get_income_sum(Data.get_cash_data(Data.get_all_data()))
                - Data.get_outgo_sum(Data.get_cash_data(Data.get_all_data())),
            'year': now.year,
            'month': now.month,
            'day': now.day,
            'actual_cash_balance': actual_cash_balance,
            'credit_checked_date': credit_checked_date,
            'living_cost_mark': living_cost_mark,
        }
        return render(request, 'tools.html', context)




