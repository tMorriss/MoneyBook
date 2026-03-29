from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.shortcuts import render
from django.views import View
from moneybook.models import PeriodicData


class PeriodicView(View):
    """定期取引一覧表示"""

    def get(self, request, *args, **kwargs):
        """定期取引一覧表示"""
        now = datetime.now()
        # 来月を計算
        next_month = now + relativedelta(months=1)

        context = {
            'app_name': settings.APP_NAME,
            'username': request.user,
            'year': now.year,
            'month': now.month,
            'next_year': next_month.year,
            'next_month': next_month.month,
            'periodic_data_list': PeriodicData.get_all(),
        }
        return render(request, 'periodic.html', context)
