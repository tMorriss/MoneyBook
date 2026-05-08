from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views import View
from moneybook.forms import PeriodicDataForm
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

    def post(self, request, *args, **kwargs):
        """設定を更新してperiodicにリダイレクト"""
        # 既存のデータを全削除
        PeriodicData.objects.all().delete()

        for key in request.POST.keys():
            if key.startswith('day_') and not key.startswith('csrfmiddlewaretoken'):
                id_part = key[4:]  # 'day_' を除く

                day = request.POST.get(f'day_{id_part}')
                item = request.POST.get(f'item_{id_part}')
                price = request.POST.get(f'price_{id_part}')
                direction = request.POST.get(f'direction_{id_part}')
                method = request.POST.get(f'method_{id_part}')
                category = request.POST.get(f'category_{id_part}')
                temp = request.POST.get(f'temp_{id_part}')

                if day and item and price:  # 必須フィールドのチェック
                    form_data = {
                        'day': day,
                        'item': item,
                        'price': price,
                        'direction': direction,
                        'method': method,
                        'category': category,
                        'temp': temp == '1'
                    }
                    form = PeriodicDataForm(form_data)
                    if form.is_valid():
                        form.save()

        return HttpResponseRedirect(reverse('moneybook:periodic'))
