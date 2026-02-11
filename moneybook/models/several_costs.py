from django.db import models


class SeveralCosts(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)

    @staticmethod
    def get_living_cost_mark():
        try:
            return SeveralCosts.objects.get(name='LivingCostMark').price
        except SeveralCosts.DoesNotExist:
            return 0

    @staticmethod
    def set_living_cost_mark(price):
        try:
            obj = SeveralCosts.objects.get(name='LivingCostMark')
            obj.price = price
            obj.save()
        except SeveralCosts.DoesNotExist:
            SeveralCosts.objects.create(name='LivingCostMark', price=price)

    @staticmethod
    def get_actual_cash_balance():
        try:
            return SeveralCosts.objects.get(name='ActualCashBalance').price
        except SeveralCosts.DoesNotExist:
            return 0

    @staticmethod
    def set_actual_cash_balance(price):
        try:
            obj = SeveralCosts.objects.get(name='ActualCashBalance')
            obj.price = price
            obj.save()
        except SeveralCosts.DoesNotExist:
            SeveralCosts.objects.create(name='ActualCashBalance', price=price)
