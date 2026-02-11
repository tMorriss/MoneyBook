from django.db import models

from .direction import Direction


class Category(models.Model):
    show_order = models.IntegerField(default=-100)
    name = models.CharField(max_length=10)
    is_living_cost = models.BooleanField(default=False)
    is_variable_cost = models.BooleanField(default=False)
    default_direction = models.ForeignKey(
        Direction, on_delete=models.RESTRICT, null=True, blank=True
    )

    def __str__(self):
        return self.name

    @staticmethod
    def get(pk):
        return Category.objects.get(pk=pk)

    @staticmethod
    def list():
        return Category.objects.order_by('show_order')

    @staticmethod
    def first_list():
        return Category.objects.filter(show_order__gt=0).order_by('show_order')

    @staticmethod
    def latter_list():
        return Category.objects.filter(show_order__lte=0).order_by('-show_order')

    @staticmethod
    def get_intra_move():
        return Category.objects.get(name='内部移動')

    @staticmethod
    def get_deposit():
        return Category.objects.get(name='貯金')

    @staticmethod
    def get_income():
        return Category.objects.get(name='収入')

    @staticmethod
    def get_traffic_cost():
        return Category.objects.get(name='交通費')
