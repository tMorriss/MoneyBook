import calendar
from datetime import date

from django.db import models
from django.db.models import Sum


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

    def chargeableList():
        return Method.objects.filter(
            show_order__gt=0, chargeable=1
        ).order_by(
            'show_order')


class Category(models.Model):
    show_order = models.IntegerField(default=-100)
    name = models.CharField(max_length=10)
    is_living_cost = models.BooleanField(default=False)
    is_variable_cost = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get(pk):
        return Category.objects.get(pk=pk)

    def list():
        return Category.objects.order_by('show_order')

    def first_list():
        return Category.objects.filter(show_order__gt=0).order_by('show_order')

    def latter_list():
        return Category.objects.filter(show_order__lte=0).order_by('-show_order')


class Data(models.Model):
    date = models.DateField()
    item = models.CharField(max_length=100)
    price = models.IntegerField()
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
    method = models.ForeignKey(Method, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
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
        if start is not None:
            data = data.filter(date__gte=start)
        if end is not None:
            data = data.filter(date__lte=end)
        return data

    # 指定月のデータを持ってくる
    def getMonthData(year, month):
        start = date(year, month, 1)
        end = date(year, month, calendar.monthrange(year, month)[1])
        return Data.getRangeData(start, end)

    # 収入や支出の合計
    def getSum(data, direction):
        v = data.filter(direction=direction).aggregate(
            Sum('price'))['price__sum']
        if v is None:
            v = 0
        return v

    # 収入の合計
    def getIncomeSum(data):
        return Data.getSum(data, 1)

    # 支出の合計
    def getOutgoSum(data):
        return Data.getSum(data, 2)

    # methodでフィルタ
    def getMethodData(data, methodId):
        return data.filter(method=methodId)

    # categoryでフィルタ
    def getCategoryData(data, categoryId):
        return data.filter(category=categoryId)

    # 立替合計
    def getTempSum(data):
        temp = data.filter(temp=1).aggregate(Sum('price'))['price__sum']
        if temp is None:
            temp = 0
        return temp

    # 立替と貯金をフィルタ
    def getTempAndDeposit(data):
        deposit = data.filter(category=11).aggregate(
            Sum('price'))['price__sum']
        if deposit is None:
            deposit = 0
        return Data.getTempSum(data) + deposit

    # 内部移動だけを排除
    def getDataWithoutInmove(data):
        return data.exclude(category=10)

    # 計算外と内部移動を排除
    def getNormalData(data):
        return data.exclude(category=9).exclude(category=10)

    # 使った生活費
    def getLivingData(data):
        livingCategories = Category.objects.filter(is_living_cost=True)
        return data.filter(category__in=livingCategories)

    # 使った変動費
    def getVariableData(data):
        variableCategories = Category.objects.filter(is_variable_cost=True)
        return data.filter(category__in=variableCategories)

    def getFoodCosts(data):
        i = Data.getIncomeSum(Data.getCategoryData(data, 1).filter(temp=1))
        o = Data.getOutgoSum(Data.getCategoryData(data, 1))
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

    # チェック済みのデータを取得
    def getCheckedData(data):
        return Data.sortDateAscending(data.filter(checked=1))

    # 未チェックのデータを取得
    def getUncheckedData(data):
        return Data.sortDateAscending(data.filter(checked=0))

    # 指定データを取得
    def get(pk):
        return Data.objects.get(pk=pk)

    # 金額でフィルタ
    def filterPrice(data, lower, upper):
        if lower is not None:
            data = data.filter(price__gte=lower)
        if upper is not None:
            data = data.filter(price__lte=upper)
        return data

    # directionリストでフィルタ
    def filterDirections(data, directions):
        return data.filter(direction__in=directions)

    # methodリストでフィルタ
    def filterMethods(data, methods):
        return data.filter(method__in=methods)

    # categoryリストでフィルタ
    def filterCategories(data, categories):
        return data.filter(category__in=categories)

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

    def set(pk, newDate):
        obj = CheckedDate.objects.get(pk=pk)
        obj.date = newDate
        obj.save()


class CreditCheckedDate(models.Model):
    show_order = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    date = models.DateField()
    price = models.IntegerField(default=0)

    def getAll():
        return CreditCheckedDate.objects.all().order_by("show_order")

    def setDate(pk, newDate):
        obj = CreditCheckedDate.objects.get(pk=pk)
        obj.date = newDate
        obj.save()

    def setPrice(pk, price):
        obj = CreditCheckedDate.objects.get(pk=pk)
        obj.price = price
        obj.save()


class BankBalance(models.Model):
    show_order = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)

    def getAll():
        return BankBalance.objects.all().order_by("show_order")

    def set(pk, price):
        obj = BankBalance.objects.get(pk=pk)
        obj.price = price
        obj.save()


class SeveralCosts(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)

    def getLivingCostMark():
        return SeveralCosts.objects.get(name="LivingCostMark").price

    def setLivingCostMark(price):
        obj = SeveralCosts.objects.get(name="LivingCostMark")
        obj.price = price
        obj.save()

    def getActualCashBalance():
        return SeveralCosts.objects.get(name="ActualCashBalance").price

    def setActualCashBalance(price):
        obj = SeveralCosts.objects.get(name="ActualCashBalance")
        obj.price = price
        obj.save()


class InOutBalance:
    def __init__(self, label, income, outgo, balance):
        self.label = label
        self.income = income
        self.outgo = outgo
        self.balance = balance


class BalanceDate:
    def __init__(self, method, balance, date):
        self.method = method
        self.balance = balance
        self.date = date


class LabelValue:
    def __init__(self, label, value):
        self.label = label
        self.value = value


class InfraCost:
    def __init__(self, label, total, electricity, gus, water):
        self.label = label
        self.total = total
        self.electricity = electricity
        self.gus = gus
        self.water = water
