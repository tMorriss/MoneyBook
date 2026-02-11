from django.db import models


class CreditCheckedDate(models.Model):
    show_order = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    date = models.DateField()
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @staticmethod
    def get_all():
        return CreditCheckedDate.objects.all().order_by('show_order')

    @staticmethod
    def set_date(pk, new_date):
        obj = CreditCheckedDate.objects.get(pk=pk)
        obj.date = new_date
        obj.save()

    @staticmethod
    def get_price(pk):
        try:
            return CreditCheckedDate.objects.get(pk=pk).price
        except CreditCheckedDate.DoesNotExist:
            return 0

    @staticmethod
    def set_price(pk, price):
        obj = CreditCheckedDate.objects.get(pk=pk)
        obj.price = price
        obj.save()
