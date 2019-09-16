from django.db import models, connection
from django.db.models import Sum
from datetime import date
import calendar
from datetime import datetime

class FixedCostPlan(models.Model):
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.price

    def get():
        return FixedCostPlan.objects.all().first().price

class Direction(models.Model):
    name = models.CharField(max_length=2)

    def __str__(self):
        return self.name

    def list():
        return Direction.objects.order_by('pk')

class Method(models.Model):
    show_order = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    chargeable = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def list():
        return Method.objects.filter(show_order__gt=0).order_by('show_order')

class Genre(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    def list():
        return Genre.objects.order_by('pk')
    def first_list():
        return Genre.objects.filter(pk__gt=0).order_by('pk')
    def latter_list():
        return Genre.objects.filter(pk__lte=0).order_by('-pk')

class Data(models.Model):
    date = models.DateField()
    item = models.CharField(max_length=100)
    price = models.IntegerField()
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
    method = models.ForeignKey(Method, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    temp = models.BooleanField()
    checked = models.BooleanField()

    def __str__(self):
        return self.item

    # 全データを持ってくる
    def getAllData():
        return Data.objects.all()
    # 指定月のデータを持ってくる
    def getMonthData(year, month):
        y = str(year)
        m = '{0:02d}'.format(month)
        start = y + "-" + m + "-1"
        end = y + "-" + m + "-" + str(calendar.monthrange(year, month)[1])
        return Data.objects.filter(date__range=(start, end)).order_by('-date', '-id')

    def getSum(data, direction):
        v = data.filter(direction=direction).aggregate(Sum('price'))['price__sum']
        if v == None:
            v = 0
        return v
    # 収入の合計
    def getIncomeSum(data):
        return Data.getSum(data, 0)
    # 支出の合計
    def getOutgoSum(data):
        return Data.getSum(data, 1)

    # methodでフィルタ
    def getMethodData(data, methodId):
        return data.filter(method=methodId).order_by('date')
    # genreでフィルタ
    def getGenreData(data, genreId):
        return data.filter(genre=genreId).order_by('date')

    # 立替と貯金をフィルタ
    def getTempAndDeposit(data):
        temp = data.filter(temp=1).aggregate(Sum('price'))['price__sum']
        deposit = data.filter(genre=-3).aggregate(Sum('price'))['price__sum']
        return temp + deposit

    # 計算外と内部移動を排除
    def getNormalData(data):
        return data.exclude(genre=-1).exclude(genre=-2)

    # 使った固定費
    def getFixedData(data):
        fixedGenres = [1, 2, 7]
        return data.filter(genre__in=fixedGenres)
    # 使った変動費
    def getVariableData(data):
        variableGenres = [0, 3, 4, 5, 6]
        return data.filter(genre__in=variableGenres)

