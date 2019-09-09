from django.db import models
from datetime import date
import calendar
from datetime import datetime

class Direction(models.Model):
    name = models.CharField(max_length=2)

    def __str__(self):
        return self.name

class Method(models.Model):
    order = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    chargeable = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Data(models.Model):
    date = models.DateField()
    item = models.CharField(max_length=100)
    price = models.IntegerField()
    method = models.ForeignKey(Method, on_delete=models.CASCADE)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    temp = models.BooleanField()
    checked = models.BooleanField()

    def __str__(self):
        return self.item

    def monthData(year, month):
        y = str(year)
        m = '{0:02d}'.format(month)
        start = y + "-" + m + "-1"
        end = y + "-" + m + "-" + str(calendar.monthrange(year, month)[1])
        return Data.objects.filter(date__range=(start, end))

    def toMonthData():
        today = datetime.today()
        return Data.monthData(today.year, today.month)
