from django.db import models


class Method(models.Model):
    show_order = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    chargeable = models.BooleanField(default=0)

    def __str__(self):
        return self.name

    @staticmethod
    def get(pk):
        return Method.objects.get(pk=pk)

    @staticmethod
    def list():
        return Method.objects.filter(show_order__gt=0).order_by('show_order')

    @staticmethod
    def un_used_list():
        return Method.objects.filter(show_order__lte=0).order_by('-show_order', 'id')

    @staticmethod
    def chargeable_list():
        return Method.objects.filter(show_order__gt=0, chargeable=1).order_by(
            'show_order'
        )

    @staticmethod
    def get_bank():
        return Method.objects.get(name='銀行')

    @staticmethod
    def get_paypay():
        return Method.objects.get(name='PayPay')
