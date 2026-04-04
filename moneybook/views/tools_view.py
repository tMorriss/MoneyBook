from datetime import date, datetime

from django.conf import settings
from django.shortcuts import render
from django.views import View
from moneybook.models import BankBalance, CreditCheckedDate, Data, SeveralCosts


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


class SeveralCheckedDateView(View):
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


class UncheckedDataView(View):
    def get(self, request, *args, **kwargs):
        # 全データ
        all_data = Data.get_all_data()
        # 未承認トランザクション
        unchecked_data = Data.get_unchecked_data(all_data)
        context = {
            'unchecked_data': unchecked_data,
        }
        return render(request, '_unchecked_data.html', context)


class PreCheckedSummaryView(View):
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
