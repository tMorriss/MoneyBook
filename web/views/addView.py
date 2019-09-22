from django.conf import settings
from django.shortcuts import render
from datetime import datetime
from web.models import *

def add(request):
    now = datetime.now()
    content = {
        'app_name': settings.APP_NAME,
        'year': now.year,
        'month': now.month,
        'directions': Direction.list(),
        'methods': Method.list(),
        'first_genres': Genre.first_list(),
        'latter_genres': Genre.latter_list(),
        'temps': {0:"No", 1:"Yes"},
    }
    return render(request, 'web/add.html', content)
