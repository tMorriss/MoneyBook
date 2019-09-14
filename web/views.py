from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.template import loader
from django.conf import settings

def index(request):
    if "year" in request.GET and "month" in request.GET:
        monthlyData = Data.monthData(int(request.GET.get("year")), int(request.GET.get("month")))
    else:
        monthlyData = Data.toMonthData()
    content = {
        'monthly_data': monthlyData,
        'app_name': settings.APP_NAME
    }
    return render(request, 'web/index.html', content)