import calendar
from datetime import date

from django.db import models
from django.db.models import Sum


class Direction(models.Model):
    name = models.CharField(max_length=2)

    def __str__(self):
        return self.name

    @staticmethod
    def get(pk):
        return Direction.objects.get(pk=pk)

    @staticmethod
    def list():
        return Direction.objects.order_by('pk')


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
    @staticmethod
    def get_all_data():
        return Data.objects.all()

    # 指定期間のデータを持ってくる
    @staticmethod
    def get_range_data(start, end):
        data = Data.get_all_data()
        if start is not None:
            data = data.filter(date__gte=start)
        if end is not None:
            data = data.filter(date__lte=end)
        return data

    # 指定月のデータを持ってくる
    @staticmethod
    def get_month_data(year, month):
        try:
            start = date(year, month, 1)
            end = date(year, month, calendar.monthrange(year, month)[1])
            return Data.get_range_data(start, end)
        except ValueError:
            return Data.objects.none()

    # 収入や支出の合計
    @staticmethod
    def get_sum(data, direction):
        v = data.filter(direction=direction).aggregate(
            Sum('price'))['price__sum']
        if v is None:
            v = 0
        return v

    # 収入の合計
    @staticmethod
    def get_income_sum(data):
        return Data.get_sum(data, 1)

    # 支出の合計
    @staticmethod
    def get_outgo_sum(data):
        return Data.get_sum(data, 2)

    # methodでフィルタ
    @staticmethod
    def get_method_data(data, method_id):
        return data.filter(method=method_id)

    # categoryでフィルタ
    @staticmethod
    def get_category_data(data, category_id):
        return data.filter(category=category_id)

    # 立替合計
    @staticmethod
    def get_temp_sum(data):
        temp = data.filter(temp=1).aggregate(Sum('price'))['price__sum']
        if temp is None:
            temp = 0
        return temp

    # 立替と貯金をフィルタ
    @staticmethod
    def get_temp_and_deposit_sum(data):
        category = Category.objects.get(name="貯金")
        deposit = data.filter(category=category).aggregate(
            Sum('price'))['price__sum']
        if deposit is None:
            deposit = 0
        return Data.get_temp_sum(data) + deposit

    # 内部移動だけを排除
    @staticmethod
    def get_data_without_intra_move(data):
        category = Category.objects.get(name="内部移動")
        return data.exclude(category=category)

    # 計算外と内部移動を排除
    @staticmethod
    def get_normal_data(data):
        return data.exclude(
            category=Category.objects.get(name="計算外")
        ).exclude(
            category=Category.objects.get(name="内部移動")
        )

    # 使った生活費
    @staticmethod
    def get_living_cost(data):
        categories = Category.objects.filter(is_living_cost=True)
        data = data.filter(category__in=categories)
        return Data.get_outgo_sum(data) - Data.get_temp_sum(data)

    # 使った変動費
    @staticmethod
    def get_variable_cost(data):
        categories = Category.objects.filter(is_variable_cost=True)
        data = data.filter(category__in=categories)
        return Data.get_outgo_sum(data) - Data.get_temp_sum(data)

    # 食費
    @staticmethod
    def get_food_costs(data):
        data = Data.get_category_data(
            data, Category.objects.get(name="食費")
        )
        i = Data.get_income_sum(data.filter(temp=1))
        o = Data.get_outgo_sum(data)
        return o - i

    # 日付順にソート
    @staticmethod
    def sort_data_ascending(data):
        return data.order_by('date', 'id')

    # 日付の逆にソート
    @staticmethod
    def sort_data_descending(data):
        return data.order_by('-date', '-id')

    # キーワード検索
    @staticmethod
    def get_keyword_data(data, keyword):
        return data.filter(item__contains=keyword)

    # 現金のデータを取得
    @staticmethod
    def get_cash_data(data):
        method = Method.objects.get(name="現金")
        return Data.get_method_data(data, method)

    # 銀行のデータを取得
    @staticmethod
    def get_bank_data(data):
        method = Method.objects.get(name="銀行")
        return Data.get_method_data(data, method)

    # チェック済みのデータを取得
    @staticmethod
    def get_checked_data(data):
        return Data.sort_data_ascending(data.filter(checked=True))

    # 未チェックのデータを取得
    @staticmethod
    def get_unchecked_data(data):
        return Data.sort_data_ascending(data.filter(checked=False))

    # 指定データを取得
    @staticmethod
    def get(pk):
        return Data.objects.get(pk=pk)

    # 金額でフィルタ
    @staticmethod
    def filter_price(data, lower, upper):
        if lower is not None:
            data = data.filter(price__gte=lower)
        if upper is not None:
            data = data.filter(price__lte=upper)
        return data

    # directionリストでフィルタ
    @staticmethod
    def filter_directions(data, directions):
        return data.filter(direction__in=directions)

    # methodリストでフィルタ
    @staticmethod
    def filter_methods(data, methods):
        return data.filter(method__in=methods)

    # categoryリストでフィルタ
    @staticmethod
    def filter_categories(data, categories):
        return data.filter(category__in=categories)

    # tempリストでフィルタ
    @staticmethod
    def filter_temps(data, temps):
        return data.filter(temp__in=temps)

    # checkedリストでフィルタ
    @staticmethod
    def filter_checkeds(data, checkeds):
        return data.filter(checked__in=checkeds)


class CheckedDate(models.Model):
    method = models.OneToOneField(Method, on_delete=models.CASCADE)
    date = models.DateField()

    @staticmethod
    def get(pk):
        return CheckedDate.objects.get(pk=pk)

    @staticmethod
    def set(pk, new_date):
        obj = CheckedDate.objects.get(pk=pk)
        obj.date = new_date
        obj.save()


class CreditCheckedDate(models.Model):
    show_order = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    date = models.DateField()
    price = models.IntegerField(default=0)

    @staticmethod
    def get_all():
        return CreditCheckedDate.objects.all().order_by("show_order")

    @staticmethod
    def set_date(pk, new_date):
        obj = CreditCheckedDate.objects.get(pk=pk)
        obj.date = new_date
        obj.save()

    @staticmethod
    def set_price(pk, price):
        obj = CreditCheckedDate.objects.get(pk=pk)
        obj.price = price
        obj.save()


class BankBalance(models.Model):
    show_order = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)

    @staticmethod
    def get_all():
        return BankBalance.objects.all().order_by("show_order")

    @staticmethod
    def set(pk, price):
        obj = BankBalance.objects.get(pk=pk)
        obj.price = price
        obj.save()


class SeveralCosts(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)

    @staticmethod
    def get_living_cost_mark():
        try:
            price = SeveralCosts.objects.get(name="LivingCostMark").price
            if price is None:
                price = 0
            return price
        except SeveralCosts.DoesNotExist:
            return 0

    @staticmethod
    def set_living_cost_mark(price):
        try:
            obj = SeveralCosts.objects.get(name="LivingCostMark")
            obj.price = price
            obj.save()
        except SeveralCosts.DoesNotExist:
            SeveralCosts.objects.create(name="LivingCostMark", price=price)

    @staticmethod
    def get_actual_cash_balance():
        try:
            price = SeveralCosts.objects.get(name="ActualCashBalance").price
            if price is None:
                price = 0
            return price
        except SeveralCosts.DoesNotExist:
            return 0

    @staticmethod
    def set_actual_cash_balance(price):
        try:
            obj = SeveralCosts.objects.get(name="ActualCashBalance")
            obj.price = price
            obj.save()
        except SeveralCosts.DoesNotExist:
            SeveralCosts.objects.create(name="ActualCashBalance", price=price)


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
