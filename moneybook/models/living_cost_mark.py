from datetime import date

from django.db import models


class LivingCostMark(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.start_date} - {self.end_date}: {self.price}'

    @staticmethod
    def get_mark(year, month):
        target_date = date(int(year), int(month), 1)
        mark = LivingCostMark.objects.filter(
            start_date__lte=target_date
        ).filter(
            models.Q(end_date__isnull=True) | models.Q(end_date__gte=target_date)
        ).order_by('-start_date').first()
        return mark.price if mark else 0

    @staticmethod
    def get_all():
        return LivingCostMark.objects.all().order_by('start_date')
