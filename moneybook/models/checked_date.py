from django.db import models

from .method import Method


class CheckedDate(models.Model):
    method = models.OneToOneField(Method, on_delete=models.RESTRICT)
    date = models.DateField()

    @staticmethod
    def get(pk):
        return CheckedDate.objects.get(pk=pk)

    @staticmethod
    def set(pk, new_date):
        obj = CheckedDate.objects.get(pk=pk)
        obj.date = new_date
        obj.save()
