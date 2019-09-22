from django.conf import settings
from django.shortcuts import render
from web.models import *

def search(request):
    queryContent = {}
    queryList = ["start_year", "start_month", "start_day", "end_year", "end_month", "end_day", "item", "lower_price", "upper_price"]
    for q in queryList:
        if q in request.GET:
            queryContent[q] = request.GET.get(q)

    content = {
        'app_name': settings.APP_NAME,
        'directions': Direction.list(),
        'methods': Method.list(),
        'unused_methods': Method.unUsedList(),
        'first_genres': Genre.first_list(),
        'latter_genres': Genre.latter_list(),
        'temps': {0: "No", 1: "Yes"},
        'checked': {0: "No", 1: "Yes"},
    }
    content.update(queryContent)
    return render(request, 'web/search.html', content)
