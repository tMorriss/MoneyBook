from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.template import loader

# Create your views here.

def index(request):
    if "year" in request.GET and "month" in request.GET:
        monthlyData = Data.monthData(int(request.GET.get("year")), int(request.GET.get("month")))
    else:
        monthlyData = Data.toMonthData()
    # allData = Data.objects.all()
    content = {'monthly_data': monthlyData}
    return render(request, 'web/index.html', content)
    # template = loader.get_template('web/index.html')
    # return HttpResponse(template.render(content, request))