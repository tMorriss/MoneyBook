from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from moneybook.forms import PeriodicDataForm
from moneybook.models import PeriodicData


class PeriodicEditApiView(View):
    """定期取引編集API"""

    def post(self, request, *args, **kwargs):
        """設定を更新"""
        try:
            # 既存のデータを全削除
            PeriodicData.objects.all().delete()

            # POSTデータから新しいデータを登録
            processed_ids = set()

            for key in request.POST.keys():
                if key.startswith('day_') and not key.startswith('csrfmiddlewaretoken'):
                    id_part = key[4:]  # 'day_' を除く

                    if id_part in processed_ids:
                        continue
                    processed_ids.add(id_part)

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
                            'temp': temp
                        }
                        form = PeriodicDataForm(form_data)
                        if form.is_valid():
                            form.save()

            return HttpResponse()
        except Exception:
            return HttpResponseBadRequest()
