from django.conf import settings
from django.shortcuts import redirect, render
from django.views import View
from moneybook.models import Category, Data, Direction, Method


class EditView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']

        try:
            data = Data.get(pk)
        except:
            return redirect('moneybook:index')

        context = {
            'app_name': settings.APP_NAME,
            'username': request.user,
            'data': data,
            'directions': Direction.list(),
            'methods': Method.list(),
            'unused_methods': Method.un_used_list(),
            'first_categories': Category.first_list(),
            'latter_categories': Category.latter_list(),
            'temps': {0: 'No', 1: 'Yes'},
            'checkeds': {0: 'No', 1: 'Yes'},
        }
        return render(request, 'edit.html', context)
