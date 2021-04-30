from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        api_list = [
            reverse('moneybook:actual_cash'),
            reverse('moneybook:add'),
            reverse('moneybook:add_intra_move'),
            reverse('moneybook:balance_statistic_mini'),
            reverse('moneybook:chart_container_data'),
            reverse('moneybook:checked_date'),
            reverse('moneybook:credit_checked_date'),
            reverse('moneybook:data_table'),
            reverse('moneybook:edit_check'),
            reverse('moneybook:living_cost_mark'),
            reverse('moneybook:now_bank'),
            reverse('moneybook:several_checked_date'),
            reverse('moneybook:unchecked_data'),
        ]
        if not request.user.is_authenticated and request.path != reverse('moneybook:login'):
            if request.path in api_list:
                return HttpResponseForbidden({'message': 'login is required'})
            return HttpResponseRedirect(reverse('moneybook:login'))

        return self.get_response(request)
