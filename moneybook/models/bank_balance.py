from django.db import models


class BankBalance(models.Model):
    show_order = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)

    @staticmethod
    def get_all():
        return BankBalance.objects.all().order_by("show_order")

    @staticmethod
    def get_price(pk):
        try:
            return BankBalance.objects.get(pk=pk).price
        except BankBalance.DoesNotExist:
            return 0

    @staticmethod
    def set(pk, price):
        obj = BankBalance.objects.get(pk=pk)
        obj.price = price
        obj.save()
