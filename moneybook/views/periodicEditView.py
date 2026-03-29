from django.conf import settings
from django.shortcuts import render
from django.views import View
from moneybook.models import Category, Direction, Method, PeriodicData


class PeriodicEditView(View):
    """定期取引編集"""

    def get(self, request, *args, **kwargs):
        """編集画面表示"""
        context = {
            'app_name': settings.APP_NAME,
            'username': request.user,
            'periodic_data_list': PeriodicData.get_all(),
            'directions': Direction.list(),
            'methods': Method.list(),
            'first_categories': Category.first_list(),
            'latter_categories': Category.latter_list(),
        }
        return render(request, 'periodic_edit.html', context)
