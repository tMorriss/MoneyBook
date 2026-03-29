from django.db import models

from .category import Category
from .direction import Direction
from .method import Method


class PeriodicData(models.Model):
    day = models.IntegerField()
    item = models.CharField(max_length=100)
    price = models.IntegerField()
    direction = models.ForeignKey(Direction, on_delete=models.RESTRICT)
    method = models.ForeignKey(Method, on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    temp = models.BooleanField()

    def __str__(self):
        return self.item

    @staticmethod
    def get_all():
        """全データを取得"""
        return PeriodicData.objects.all().order_by('day', 'id')

    @staticmethod
    def get(pk):
        """指定データを取得"""
        return PeriodicData.objects.get(pk=pk)
