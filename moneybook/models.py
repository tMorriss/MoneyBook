import calendar
from datetime import date

from django.db import models
from django.db.models import Q, Sum


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
        return Method.objects.filter(show_order__gt=0, chargeable=1).order_by('show_order')

    @staticmethod
    def get_bank():
        return Method.objects.get(name="銀行")

    @staticmethod
    def get_paypay():
        return Method.objects.get(name="PayPay")


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


class Data(models.Model):
    date = models.DateField()
    item = models.CharField(max_length=100)
    price = models.IntegerField()
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
    method = models.ForeignKey(Method, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    temp = models.BooleanField()
    checked = models.BooleanField(default=False)
    pre_checked = models.BooleanField(default=False)

    def __str__(self):
        return self.item

    @staticmethod
    def get_all_data():
        """全データを持ってくる"""
        return Data.sort_ascending(Data.objects.all())

    @staticmethod
    def get_range_data(start, end):
        """指定期間のデータを持ってくる"""
        data = Data.get_all_data()
        if start is not None:
            data = data.filter(date__gte=start)
        if end is not None:
            data = data.filter(date__lte=end)
        return Data.sort_ascending(data)

    @staticmethod
    def get_month_data(year, month):
        """指定月のデータを持ってくる"""
        try:
            start = date(year, month, 1)
            end = date(year, month, calendar.monthrange(year, month)[1])
            return Data.get_range_data(start, end)
        except ValueError:
            return Data.sort_ascending(Data.objects.none())

    @staticmethod
    def get_sum(data, direction):
        """収入や支出の合計"""
        v = data.filter(direction=direction).aggregate(Sum('price'))['price__sum']
        if v is None:
            v = 0
        return v

    @staticmethod
    def get_income_sum(data):
        """収入の合計"""
        return Data.get_sum(data, 1)

    @staticmethod
    def get_outgo_sum(data):
        """支出の合計"""
        return Data.get_sum(data, 2)

    @staticmethod
    def get_method_data(data, method_id):
        """methodでフィルタ"""
        return Data.sort_ascending(data.filter(method=method_id))

    @staticmethod
    def get_category_data(data, category_id):
        """categoryでフィルタ"""
        return Data.sort_ascending(data.filter(category=category_id))

    @staticmethod
    def get_temp_sum(data):
        """立替合計"""
        temp = data.filter(temp=1).aggregate(Sum('price'))['price__sum']
        if temp is None:
            temp = 0
        return temp

    @staticmethod
    def get_temp_and_deposit_sum(data):
        """立替と貯金をフィルタ"""
        category = Category.objects.get(name="貯金")
        deposit = data.filter(Q(category=category) | Q(temp=1)).aggregate(Sum('price'))['price__sum']
        if deposit is None:
            deposit = 0
        return deposit

    @staticmethod
    def filter_without_intra_move(data):
        """内部移動だけを排除"""
        category = Category.objects.get(name="内部移動")
        return Data.sort_ascending(data.exclude(category=category))

    @staticmethod
    def get_normal_data(data):
        """計算外と内部移動を排除"""
        return data.exclude(category=Category.objects.get(name="計算外")).exclude(category=Category.objects.get(name="内部移動"))

    @staticmethod
    def get_living_cost(data):
        """使った生活費"""
        categories = Category.objects.filter(is_living_cost=True)
        data = data.filter(category__in=categories)
        return Data.get_outgo_sum(data) - Data.get_temp_sum(data)

    @staticmethod
    def get_variable_cost(data):
        """使った変動費"""
        categories = Category.objects.filter(is_variable_cost=True)
        data = data.filter(category__in=categories)
        return Data.get_outgo_sum(data) - Data.get_temp_sum(data)

    @staticmethod
    def get_food_costs(data):
        """食費"""
        data = Data.get_category_data(data, Category.objects.get(name="食費"))
        i = Data.get_income_sum(data.filter(temp=1))
        o = Data.get_outgo_sum(data)
        return o - i

    @staticmethod
    def sort_ascending(data):
        """日付順にソート"""
        return data.order_by('date', 'id')

    @staticmethod
    def sort_descending(data):
        """日付の逆にソート"""
        return data.order_by('-date', '-id')

    @staticmethod
    def get_keyword_data(data, keyword):
        """キーワード検索"""
        return Data.sort_ascending(data.filter(item__contains=keyword))

    @staticmethod
    def get_cash_data(data):
        """現金のデータを取得"""
        method = Method.objects.get(name="現金")
        return Data.sort_ascending(Data.get_method_data(data, method))

    @staticmethod
    def get_bank_data(data):
        """銀行のデータを取得"""
        method = Method.objects.get(name="銀行")
        return Data.sort_ascending(Data.get_method_data(data, method))

    @staticmethod
    def get_checked_data(data):
        """チェック済みのデータを取得"""
        return Data.sort_ascending(data.filter(checked=True))

    @staticmethod
    def get_unchecked_data(data):
        """未チェックのデータを取得"""
        return Data.sort_ascending(data.filter(checked=False))

    @staticmethod
    def get_pre_checked_data(data):
        """チェック済みのデータを取得"""
        return Data.sort_ascending(data.filter(pre_checked=True))

    @staticmethod
    def get(pk):
        """指定データを取得"""
        return Data.objects.get(pk=pk)

    @staticmethod
    def filter_price(data, lower, upper):
        """金額でフィルタ"""
        if lower is not None:
            data = data.filter(price__gte=lower)
        if upper is not None:
            data = data.filter(price__lte=upper)
        return data

    @staticmethod
    def filter_directions(data, directions):
        """directionリストでフィルタ"""
        return Data.sort_ascending(data.filter(direction__in=directions))

    @staticmethod
    def filter_methods(data, methods):
        """methodリストでフィルタ"""
        return Data.sort_ascending(data.filter(method__in=methods))

    @staticmethod
    def filter_categories(data, categories):
        """categoryリストでフィルタ"""
        return Data.sort_ascending(data.filter(category__in=categories))

    @staticmethod
    def filter_temps(data, temps):
        """tempリストでフィルタ"""
        return Data.sort_ascending(data.filter(temp__in=temps))

    @staticmethod
    def filter_checkeds(data, checkeds):
        """checkedリストでフィルタ"""
        return Data.sort_ascending(data.filter(checked__in=checkeds))


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

    def __str__(self):
        return self.name

    @staticmethod
    def get_all():
        return CreditCheckedDate.objects.all().order_by("show_order")

    @staticmethod
    def set_date(pk, new_date):
        obj = CreditCheckedDate.objects.get(pk=pk)
        obj.date = new_date
        obj.save()

    @staticmethod
    def get_price(pk):
        try:
            return CreditCheckedDate.objects.get(pk=pk).price
        except CreditCheckedDate.DoesNotExist:
            return 0

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
    def get_price(pk):
        try:
            return BankBalance.objects.get(pk=pk).price
        except BankBalance.DoesNotExist:
            return 0

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
            return SeveralCosts.objects.get(name="LivingCostMark").price
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
            return SeveralCosts.objects.get(name="ActualCashBalance").price
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


class LabelValue:
    def __init__(self, label, value):
        self.label = label
        self.value = value
