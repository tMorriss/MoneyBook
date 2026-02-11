import calendar
from datetime import date

from django.db import models
from django.db.models import Sum

from .category import Category
from .direction import Direction
from .method import Method


class Data(models.Model):
    date = models.DateField()
    item = models.CharField(max_length=100)
    price = models.IntegerField()
    direction = models.ForeignKey(Direction, on_delete=models.RESTRICT)
    method = models.ForeignKey(Method, on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
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
        v = data.filter(direction=direction).aggregate(Sum("price"))["price__sum"]
        if v is None:
            v = 0
        return v

    @staticmethod
    def get_income(data):
        """収入データ"""
        return data.filter(direction=1)

    @staticmethod
    def get_outgo(data):
        """支出データ"""
        return data.filter(direction=2)

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
        """貯金以外の立替合計"""
        deposit = Category.get_deposit()
        temp = data.filter(temp=1).exclude(category=deposit).aggregate(Sum("price"))[
            "price__sum"
        ]
        return temp if temp is not None else 0

    @staticmethod
    def get_deposit_outgo_sum(data):
        """貯金の支出分をフィルタ"""
        category = Category.get_deposit()
        deposit_out = (
            data.filter(category=category, direction=2).aggregate(Sum("price"))[
                "price__sum"
            ]
        )

        return deposit_out if deposit_out is not None else 0

    @staticmethod
    def get_deposit_sum(data):
        """貯金をフィルタ"""
        category = Category.get_deposit()
        deposit_out = (
            data.filter(category=category, direction=2).aggregate(Sum("price"))[
                "price__sum"
            ]
        )
        deposit_temp = (
            data.filter(category=category, temp=1).aggregate(Sum("price"))["price__sum"]
        )

        return (deposit_out if deposit_out is not None else 0) - (
            deposit_temp if deposit_temp is not None else 0
        )

    @staticmethod
    def filter_without_intra_move(data):
        """内部移動だけを排除"""
        category = Category.objects.get(name="内部移動")
        return Data.sort_ascending(data.exclude(category=category))

    @staticmethod
    def get_normal_data(data):
        """計算外と内部移動と立替を排除"""
        return (
            data.exclude(category=Category.objects.get(name="計算外"))
            .exclude(category=Category.objects.get(name="内部移動"))
        )

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
        return data.order_by("date", "id")

    @staticmethod
    def sort_descending(data):
        """日付の逆にソート"""
        return data.order_by("-date", "-id")

    @staticmethod
    def get_keyword_data(data, keyword):
        """キーワード検索"""
        return Data.sort_ascending(data.filter(item__contains=keyword))

    @staticmethod
    def get_startswith_keyword_data(data, keyword):
        """キーワード検索(前方一致)"""
        return Data.sort_ascending(data.filter(item__startswith=keyword))

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
