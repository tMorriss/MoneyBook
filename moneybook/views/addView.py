import json
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views import View
from moneybook.forms import DataForm
from moneybook.models import Category, Data, Direction, Method


class AddView(View):
    def get(self, request, *args, **kwargs):
        now = datetime.now()
        context = {
            'app_name': settings.APP_NAME,
            'username': request.user,
            'year': now.year,
            'month': now.month,
            'day': now.day,
            'directions': Direction.list(),
            'methods': Method.list(),
            'chargeable_methods': Method.chargeable_list(),
            'first_categories': Category.first_list(),
            'latter_categories': Category.latter_list(),
            'temps': {0: 'No', 1: 'Yes'},
            'paypay_pk': Method.get_paypay().pk,
            'bank_pk': Method.get_bank().pk,
            'traffic_cost_pk': Category.get_traffic_cost().pk,
            'deposit_pk': Category.get_deposit().pk,
            'income_pk': Category.get_income().pk,
        }
        return render(request, 'add.html', context)
