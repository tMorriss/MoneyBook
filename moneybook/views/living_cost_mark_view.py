from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from moneybook.models import LivingCostMark


class LivingCostMarkView(LoginRequiredMixin, View):
    """生活費目標一覧表示"""

    def get(self, request, *args, **kwargs):
        context = {
            'app_name': settings.APP_NAME,
            'username': request.user,
            'living_cost_marks': LivingCostMark.get_all(),
        }
        return render(request, 'living_cost_mark.html', context)
