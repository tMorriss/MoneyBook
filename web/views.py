from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.template import loader
from django.conf import settings
from datetime import datetime

def index(request):
    if "year" in request.GET and "month" in request.GET:
        monthlyData = Data.getMonthData(int(request.GET.get("year")), int(request.GET.get("month")))
    else:
        monthlyData = Data.getToMonthData()
    content = {
        'monthly_data': monthlyData,
        'app_name': settings.APP_NAME,
    }
    return render(request, 'web/index.html', content)

def add(request):
    now = datetime.now()
    directions = Direction.list()
    methods = Method.list()
    first_genres = Genre.first_list()
    latter_genres = Genre.latter_list()
    temps = {0:"No", 1:"Yes"}
    content = {
        'app_name': settings.APP_NAME,
        'year': now.year,
        'month': now.month,
        'directions': directions,
        'methods': methods,
        'first_genres': first_genres,
        'latter_genres': latter_genres,
        'temps': temps,
    }
    return render(request, 'web/add.html', content)