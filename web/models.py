from django.db import models, connection
from django.db.models import Sum
from datetime import date, datetime
import calendar

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

    def get(pk):
        return Direction.objects.get(pk=pk)

    def list():
        return Direction.objects.order_by('pk')

class Method(models.Model):
    show_order = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    chargeable = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get(pk):
        return Method.objects.get(pk=pk)

    def list():
        return Method.objects.filter(show_order__gt=0).order_by('show_order')

    def unUsedList():
        return Method.objects.filter(show_order__lte=0).order_by('id')

class Genre(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    def get(pk):
        return Genre.objects.get(pk=pk)

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
    checked = models.BooleanField(default=False)

    def __str__(self):
        return self.item

    # 全データを持ってくる
    def getAllData():
        return Data.objects.all()

    # 指定期間のデータを持ってくる
    def getRangeData(start, end):
        data = Data.getAllData()
        if start != None:
            data = data.filter(date__gte=start)
        if end != None:
            data = data.filter(date__lte=end)
        return data

    # 指定月のデータを持ってくる
    def getMonthData(year, month):
        start = date(year, month, 1)
        end = date(year, month, calendar.monthrange(year, month)[1])
        return Data.getRangeData(start, end)

    # 収入や支出の合計
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
        return data.filter(method=methodId)
    # genreでフィルタ
    def getGenreData(data, genreId):
        return data.filter(genre=genreId)

    # 立替と貯金をフィルタ
    def getTempAndDeposit(data):
        temp = data.filter(temp=1).aggregate(Sum('price'))['price__sum']
        if temp == None:
            temp = 0
        deposit = data.filter(genre=-3).aggregate(Sum('price'))['price__sum']
        if deposit == None:
            deposit = 0
        return temp + deposit

    # 内部移動だけを排除
    def getDataWithoutInmove(data):
        return data.exclude(genre=-2)

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

    def getFoodCosts(data):
        i = Data.getSum(Data.getGenreData(data, 1).filter(temp=1), 0)
        o = Data.getSum(Data.getGenreData(data, 1), 1)
        return o - i

    # 日付順にソート
    def sortDateAscending(data):
        return data.order_by('date', 'id')
    # 日付の逆にソート
    def sortDateDescending(data):
        return data.order_by('-date', '-id')

    # キーワード検索
    def getKeywordData(data, keyword):
        return data.filter(item__contains=keyword)

    # 現金のデータを取得
    def getCashData(data):
        return Data.getMethodData(data, 1)

    # 銀行のデータを取得
    def getBankData(data):
        return Data.getMethodData(data, 2)

    # 未チェックのデータを取得
    def getUncheckedData(data):
        return Data.sortDateAscending(data.filter(checked=0))

    # 指定データを取得
    def get(pk):
        return Data.objects.get(pk=pk)

    # 金額でフィルタ
    def filterPrice(data, lower, upper):
        if lower != None:
            data = data.filter(price__gte=lower)
        if upper != None:
            data = data.filter(price__lte=upper)
        return data

    # directionリストでフィルタ
    def filterDirections(data, directions):
        return data.filter(direction__in=directions)

    # methodリストでフィルタ
    def filterMethods(data, methods):
        return data.filter(method__in=methods)

    # genreリストでフィルタ
    def filterGenres(data, genres):
        return data.filter(genre__in=genres)

    # tempリストでフィルタ
    def filterTemps(data, temps):
        return data.filter(temp__in=temps)

    # checkedリストでフィルタ
    def filterCheckeds(data, checkeds):
        return data.filter(checked__in=checkeds)

class CheckedDate(models.Model):
    method = models.ForeignKey(Method, on_delete=models.CASCADE)
    date = models.DateField()

    def get(pk):
        return CheckedDate.objects.get(pk=pk)

class CreditCheckedDate(models.Model):
    show_order = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    date = models.DateField()
    price = models.IntegerField(default=0)

    def getAll():
        return CreditCheckedDate.objects.all().order_by("show_order")

class CachebackCheckedDate(models.Model):
    show_order = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    date = models.DateField()

    def getAll():
        return CachebackCheckedDate.objects.all().order_by("show_order")

class BankBalance(models.Model):
    show_order = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)

    def getAll():
        return BankBalance.objects.all().order_by("show_order")

class SeveralCosts(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)

    def getFixedCostMark():
        return SeveralCosts.objects.get(name="FixedCostMark").price

    def getActualCashBalance():
        return SeveralCosts.objects.get(name="ActualCashBalance").price

class InOutBalance:
    def __init__(self, l, i, o, b):
        self.label = l
        self.income = i
        self.outgo = o
        self.balance = b

class BalanceDate:
    def __init__(self, m, b, d):
        self.method = m
        self.balance = b
        self.date = d

class LabelValue:
    def __init__(self, l, v):
        self.label = l
        self.value = v

class InfraCost:
    def __init__(self, l, t, e, g, w):
        self.label = l
        self.total = t
        self.electricity = e
        self.gus = g
        self.water = w