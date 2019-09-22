from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from web.models import *

def edit(request, pk):
    try:
        data = Data.get(pk)
    except Data.DoesNotExist:
        raise Http404("Data does not exist")

    content = {
        'app_name': settings.APP_NAME,
        'data': data,
        'directions': Direction.list(),
        'methods': Method.list(),
        'first_genres': Genre.first_list(),
        'latter_genres': Genre.latter_list(),
        'temps': {0:"No", 1:"Yes"},
        'checked': {0: "No", 1: "Yes"},
    }
    return render(request, "web/edit.html", content)