from datetime import date

from moneybook.models import BankBalance, Category, CheckedDate, CreditCheckedDate, Data, Direction, Method, SeveralCosts
from moneybook.tests.common import CommonTestCase


class DirectionTestCase(CommonTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Direction.objects.create(name="収入")
        Direction.objects.create(name="支出")

    def test_get(self):
        self.assertEqual(str(Direction.get(1)), "収入")
        self.assertEqual(str(Direction.get(2)), "支出")

    def test_list(self):
        ls = Direction.list()
        self.assertEqual(ls.count(), 2)
        self.assertEqual(str(ls[0]), "収入")
        self.assertEqual(str(ls[1]), "支出")


class MethodTestCase(CommonTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Method.objects.create(show_order=1, name="1", chargeable=True)
        Method.objects.create(show_order=2, name="2", chargeable=False)
        Method.objects.create(show_order=0, name="0", chargeable=False)
        Method.objects.create(show_order=-2, name="-2", chargeable=False)
        Method.objects.create(show_order=-1, name="-1", chargeable=True)

    def test_get(self):
        self.assertEqual(str(Method.get(1)), "1")
        self.assertEqual(str(Method.get(4)), "-2")

    def test_list(self):
        ls = Method.list()
        self.assertEqual(ls.count(), 2)
        self.assertEqual(str(ls[0]), "1")
        self.assertEqual(str(ls[1]), "2")

    def test_unused_list(self):
        ls = Method.un_used_list()
        self.assertEqual(ls.count(), 3)
        self.assertEqual(str(ls[0]), "0")
        self.assertEqual(str(ls[1]), "-1")
        self.assertEqual(str(ls[2]), "-2")

    def test_chargeable_list(self):
        ls = Method.chargeable_list()
        self.assertEqual(ls.count(), 1)
        self.assertEqual(str(ls[0]), "1")


class CategoryTestCase(CommonTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Category.objects.create(show_order=1, name="1", is_living_cost=True, is_variable_cost=False)
        Category.objects.create(show_order=2, name="2", is_living_cost=False, is_variable_cost=True)
        Category.objects.create(show_order=0, name="0", is_living_cost=False, is_variable_cost=False)
        Category.objects.create(show_order=-1, name="-1", is_living_cost=False, is_variable_cost=False)
        Category.objects.create(show_order=-2, name="-2", is_living_cost=False, is_variable_cost=False)

    def test_get(self):
        self.assertEqual(str(Category.get(1)), "1")
        self.assertEqual(str(Category.get(4)), "-1")

    def test_list(self):
        ls = Category.list()
        self.assertEqual(ls.count(), 5)
        self.assertEqual(str(ls[0]), "-2")
        self.assertEqual(str(ls[4]), "2")

    def test_first_list(self):
        ls = Category.first_list()
        self.assertEqual(ls.count(), 2)
        self.assertEqual(str(ls[0]), "1")
        self.assertEqual(str(ls[1]), "2")

    def test_latter_list(self):
        ls = Category.latter_list()
        self.assertEqual(ls.count(), 3)
        self.assertEqual(str(ls[0]), "0")
        self.assertEqual(str(ls[2]), "-2")


class DataTestCase(CommonTestCase):
    fixtures = ['data_test_case']

    def test_get_all_data(self):
        self.assertEqual(Data.get_all_data().count(), 23)

    def test_get_range_data(self):
        start = date(2000, 1, 1)
        end = date(2000, 1, 10)
        data = Data.get_range_data(start, end)
        expects = [
            "給与",
            "コンビニ",
            "その他1",
            "必需品1",
            "必需品2",
            "現金収入"
        ]
        self._assert_list(data, expects)

    def test_get_range_data_nothing(self):
        start = date(1999, 1, 1)
        end = date(1999, 12, 30)
        data = Data.get_range_data(start, end)
        self.assertEqual(data.count(), 0)

    def test_get_month_data(self):
        data = Data.get_month_data(2000, 1)
        expects = [
            "給与",
            "コンビニ",
            "その他1",
            "必需品1",
            "必需品2",
            "現金収入",
            "銀行収入",
            "スーパー",
            "計算外",
            "貯金",
            "PayPayチャージ",
            "PayPayチャージ",
            "電気代",
            "ガス代",
            "水道代",
            "立替分1",
            "立替分2"
        ]
        self._assert_list(data, expects)

    def test_get_month_data_nothing(self):
        data = Data.get_month_data(1999, 1)
        self.assertEqual(data.count(), 0)

    def test_get_month_data_out(self):
        data = Data.get_month_data(2000, 13)
        self.assertEqual(data.count(), 0)

    def test_get_sum_one(self):
        data = Data.get_month_data(2000, 1)
        self.assertEqual(Data.get_sum(data, 1), 35123)

    def test_get_sum_one_empty(self):
        data = Data.get_month_data(1999, 1)
        self.assertEqual(Data.get_sum(data, 1), 0)

    def test_get_sum_two(self):
        data = Data.get_month_data(2000, 1)
        self.assertEqual(Data.get_sum(data, 2), 10550)

    def test_get_sum_two_empty(self):
        data = Data.get_month_data(1999, 1)
        self.assertEqual(Data.get_sum(data, 2), 0)

    def test_get_sum_nothing(self):
        data = Data.get_month_data(2000, 1)
        self.assertEqual(Data.get_sum(data, 3), 0)

    def test_get_income_sum(self):
        data = Data.get_month_data(2000, 1)
        self.assertEqual(Data.get_income_sum(data), 35123)

    def test_get_income_sum_nothing(self):
        data = Data.get_month_data(1999, 1)
        self.assertEqual(Data.get_income_sum(data), 0)

    def test_get_outgo_sum(self):
        data = Data.get_month_data(2000, 1)
        self.assertEqual(Data.get_outgo_sum(data), 10550)

    def test_get_outgo_sum_nothing(self):
        data = Data.get_month_data(1999, 1)
        self.assertEqual(Data.get_outgo_sum(data), 0)

    def test_get_method_data(self):
        month_data = Data.get_month_data(2000, 1)
        data = Data.get_method_data(month_data, 3)
        expects = [
            "PayPayチャージ",
            "立替分1"
        ]
        self._assert_list(data, expects)

    def test_get_method_data_nothing(self):
        month_data = Data.get_month_data(2000, 1)
        data = Data.get_method_data(month_data, 100)
        self.assertEqual(data.count(), 0)

    def test_get_method_data_empty(self):
        month_data = Data.get_month_data(1999, 1)
        data = Data.get_method_data(month_data, 3)
        self.assertEqual(data.count(), 0)

    def test_get_category_data(self):
        month_data = Data.get_month_data(2000, 1)
        data = Data.get_category_data(month_data, 1)
        expects = [
            "コンビニ",
            "スーパー",
            "立替分1"
        ]
        self._assert_list(data, expects)

    def test_get_category_data_nothing(self):
        month_data = Data.get_month_data(2000, 1)
        data = Data.get_category_data(month_data, 1000)
        self.assertEqual(data.count(), 0)

    def test_get_category_data_empty(self):
        month_data = Data.get_month_data(1999, 1)
        data = Data.get_category_data(month_data, 1)
        self.assertEqual(data.count(), 0)

    def test_get_temp_sum(self):
        data = Data.get_month_data(2000, 1)
        self.assertEqual(Data.get_temp_sum(data), 1000)

    def test_get_temp_sum_nothing(self):
        data = Data.get_month_data(2000, 2)
        self.assertEqual(Data.get_temp_sum(data), 0)

    def test_get_temp_sum_empty(self):
        data = Data.get_month_data(1999, 1)
        self.assertEqual(Data.get_temp_sum(data), 0)

    def test_get_temp_and_deposit_sum(self):
        data = Data.get_month_data(2000, 1)
        self.assertEqual(Data.get_temp_and_deposit_sum(data), 1130)

    def test_get_temp_and_deposit_sum_nothing(self):
        data = Data.get_month_data(2000, 2)
        self.assertEqual(Data.get_temp_and_deposit_sum(data), 0)

    def test_get_temp_and_deposit_sum_empty(self):
        data = Data.get_month_data(1999, 1)
        self.assertEqual(Data.get_temp_and_deposit_sum(data), 0)

    def test_filter_without_intra_move(self):
        base_data = Data.get_month_data(2000, 1)
        data = Data.filter_without_intra_move(base_data)
        expects = [
            "給与",
            "コンビニ",
            "その他1",
            "必需品1",
            "必需品2",
            "現金収入",
            "銀行収入",
            "スーパー",
            "計算外",
            "貯金",
            "電気代",
            "ガス代",
            "水道代",
            "立替分1",
            "立替分2"
        ]
        self._assert_list(data, expects)

    def test_filter_without_intra_move_nothing(self):
        base_data = Data.get_month_data(2000, 4)
        data = Data.filter_without_intra_move(base_data)
        self.assertEqual(data.count(), 0)

    def test_filter_without_intra_move_empty(self):
        base_data = Data.get_month_data(1999, 1)
        data = Data.filter_without_intra_move(base_data)
        self.assertEqual(data.count(), 0)

    def test_get_normal_data(self):
        '''計算外と内部移動を除く'''
        base_data = Data.get_month_data(2000, 1)
        data = Data.get_normal_data(base_data)
        expects = [
            "給与",
            "コンビニ",
            "その他1",
            "必需品1",
            "必需品2",
            "現金収入",
            "銀行収入",
            "スーパー",
            "貯金",
            "電気代",
            "ガス代",
            "水道代",
            "立替分1",
            "立替分2"
        ]
        self._assert_list(data, expects)

    def test_get_normal_data_nothing(self):
        base_data = Data.get_month_data(2000, 4)
        data = Data.get_normal_data(base_data)
        self.assertEqual(data.count(), 0)

    def test_get_normal_data_empty(self):
        base_data = Data.get_month_data(1999, 1)
        data = Data.get_normal_data(base_data)
        self.assertEqual(data.count(), 0)

    def test_get_living_cost(self):
        data = Data.get_month_data(2000, 1)
        self.assertEqual(Data.get_living_cost(data), 2500)

    def test_get_living_cost_nothing(self):
        data = Data.get_month_data(1999, 1)
        self.assertEqual(Data.get_living_cost(data), 0)

    def test_get_variable_cost(self):
        data = Data.get_month_data(2000, 1)
        self.assertEqual(Data.get_variable_cost(data), 5390)

    def test_get_variable_data_nothing(self):
        data = Data.get_month_data(1999, 1)
        self.assertEqual(Data.get_variable_cost(data), 0)

    def test_get_food_costs(self):
        data = Data.get_month_data(2000, 1)
        self.assertEqual(Data.get_food_costs(data), 2500)

    def test_get_food_costs_nothing(self):
        data = Data.get_month_data(1999, 1)
        self.assertEqual(Data.get_food_costs(data), 0)

    def test_sort_ascending(self):
        base_data = Data.get_month_data(2000, 1)
        data = Data.sort_ascending(base_data)
        expects = [
            "給与",
            "コンビニ",
            "その他1",
            "必需品1",
            "必需品2",
            "現金収入",
            "銀行収入",
            "スーパー",
            "計算外",
            "貯金",
            "PayPayチャージ",
            "PayPayチャージ",
            "電気代",
            "ガス代",
            "水道代",
            "立替分1",
            "立替分2"
        ]
        self._assert_list(data, expects)

    def test_sort_ascending_nothing(self):
        data = Data.get_month_data(1999, 1)
        sorted_data = Data.sort_ascending(data)
        self.assertEqual(sorted_data.count(), 0)

    def test_sort_descending(self):
        base_data = Data.get_month_data(2000, 1)
        data = Data.sort_descending(base_data)
        expects = [
            "立替分2",
            "立替分1",
            "水道代",
            "ガス代",
            "電気代",
            "PayPayチャージ",
            "PayPayチャージ",
            "貯金",
            "計算外",
            "スーパー",
            "銀行収入",
            "現金収入",
            "必需品2",
            "必需品1",
            "その他1",
            "コンビニ",
            "給与"
        ]
        self._assert_list(data, expects)

    def test_sort_descending_nothing(self):
        data = Data.get_month_data(1999, 1)
        sorted_data = Data.sort_descending(data)
        self.assertEqual(sorted_data.count(), 0)

    def test_get_keyword_data_part(self):
        base_data = Data.get_month_data(2000, 1)
        data = Data.get_keyword_data(base_data, "分")
        expects = [
            "立替分1",
            "立替分2"
        ]
        self._assert_list(data, expects)

    def test_get_keyword_data_same(self):
        base_data = Data.get_month_data(2000, 1)
        data = Data.get_keyword_data(base_data, "必需品1")
        self.assertEqual(data.count(), 1)
        self.assertEqual(str(data[0]), "必需品1")

    def test_get_keyword_data_nothing(self):
        base_data = Data.get_month_data(2000, 1)
        data = Data.get_keyword_data(base_data, "カレーライス")
        self.assertEqual(data.count(), 0)

    def test_get_keyword_data_empty(self):
        base_data = Data.get_month_data(1999, 1)
        data = Data.get_keyword_data(base_data, "カレーライス")
        self.assertEqual(data.count(), 0)

    def test_get_cash_data(self):
        base_data = Data.get_month_data(2000, 1)
        data = Data.get_cash_data(base_data)
        expects = [
            "コンビニ",
            "その他1",
            "必需品2",
            "現金収入",
            "スーパー"
        ]
        self._assert_list(data, expects)

    def test_get_cash_data_nothing(self):
        base_data = Data.get_month_data(2000, 2)
        data = Data.get_cash_data(base_data)
        self.assertEqual(data.count(), 0)

    def test_get_cash_data_empty(self):
        base_data = Data.get_month_data(1999, 1)
        data = Data.get_cash_data(base_data)
        self.assertEqual(data.count(), 0)

    def test_get_bank_data(self):
        base_data = Data.get_month_data(2000, 1)
        data = Data.get_bank_data(base_data)
        expects = [
            "給与",
            "必需品1",
            "銀行収入",
            "計算外",
            "貯金",
            "PayPayチャージ",
            "電気代",
            "ガス代",
            "水道代",
            "立替分2"
        ]
        self._assert_list(data, expects)

    def test_get_bank_data_nothing(self):
        base_data = Data.get_month_data(2000, 4)
        data = Data.get_bank_data(base_data)
        self.assertEqual(data.count(), 0)

    def test_get_bank_data_empty(self):
        base_data = Data.get_month_data(1999, 1)
        data = Data.get_bank_data(base_data)
        self.assertEqual(data.count(), 0)

    def test_get_checked_data(self):
        base_data = Data.get_month_data(2000, 1)
        data = Data.get_checked_data(base_data)
        expects = [
            "給与",
            "コンビニ",
            "その他1",
            "必需品2",
            "現金収入",
            "銀行収入",
            "PayPayチャージ",
            "電気代",
            "ガス代",
            "水道代",
            "立替分2"
        ]
        self._assert_list(data, expects)

    def test_get_checked_data_nothing(self):
        base_data = Data.get_month_data(2000, 4)
        data = Data.get_checked_data(base_data)
        self.assertEqual(data.count(), 0)

    def test_get_checked_data_empty(self):
        base_data = Data.get_month_data(1999, 1)
        data = Data.get_checked_data(base_data)
        self.assertEqual(data.count(), 0)

    def test_get_unchecked_data(self):
        base_data = Data.get_month_data(2000, 1)
        data = Data.get_unchecked_data(base_data)
        expects = [
            "必需品1",
            "スーパー",
            "計算外",
            "貯金",
            "PayPayチャージ",
            "立替分1"
        ]
        self._assert_list(data, expects)

    def test_get_unchecked_data_nothing(self):
        base_data = Data.get_month_data(2000, 2)
        data = Data.get_unchecked_data(base_data)
        self.assertEqual(data.count(), 0)

    def test_get_unchecked_data_empty(self):
        base_data = Data.get_month_data(1999, 1)
        data = Data.get_unchecked_data(base_data)
        self.assertEqual(data.count(), 0)

    def test_get(self):
        self.assertEqual(str(Data.get(1)), "松屋")
        self.assertEqual(str(Data.get(6)), "必需品2")

    def test_get_nothing(self):
        self.assertRaises(Data.DoesNotExist, Data.get, 100)

    def test_filter_price(self):
        base_data = Data.get_month_data(2000, 1)
        data = Data.filter_price(base_data, 100, 400)
        expects = [
            "コンビニ",
            "貯金",
            "ガス代",
            "立替分1"
        ]
        self._assert_list(data, expects)

    def test_filter_price_lower(self):
        base_data = Data.get_month_data(2000, 1)
        data = Data.filter_price(base_data, 3000, None)
        expects = [
            "給与",
            "必需品2",
            "現金収入",
            "銀行収入"
        ]
        self._assert_list(data, expects)

    def test_filter_price_upper(self):
        base_data = Data.get_month_data(2000, 1)
        data = Data.filter_price(base_data, None, 130)
        expects = [
            "コンビニ",
            "その他1",
            "貯金"
        ]
        self._assert_list(data, expects)

    def test_filter_price_nothing(self):
        base_data = Data.get_month_data(2000, 1)
        data = Data.filter_price(base_data, None, 10)
        self.assertEqual(data.count(), 0)

    def test_filter_price_empty(self):
        base_data = Data.get_month_data(1999, 1)
        data = Data.filter_price(base_data, 10, 1000)
        self.assertEqual(data.count(), 0)

    def test_filter_directions(self):
        base_data = Data.get_month_data(2000, 1)
        data = Data.filter_directions(base_data, [1])
        expects = [
            "給与",
            "現金収入",
            "銀行収入",
            "PayPayチャージ",
            "立替分1",
            "立替分2"
        ]
        self._assert_list(data, expects)

    def test_filter_directions_nothing(self):
        base_data = Data.get_month_data(2000, 1)
        data = Data.filter_directions(base_data, [1000])
        self.assertEqual(data.count(), 0)

    def test_filter_directions_empty(self):
        base_data = Data.get_month_data(1999, 1)
        data = Data.filter_directions(base_data, [1])
        self.assertEqual(data.count(), 0)

    def test_filter_methods(self):
        base_data = Data.get_month_data(2000, 1)
        data = Data.filter_methods(base_data, [1, 3])
        expects = [
            "コンビニ",
            "その他1",
            "必需品2",
            "現金収入",
            "スーパー",
            "PayPayチャージ",
            "立替分1",
        ]
        self._assert_list(data, expects)

    def test_filter_methods_nothing(self):
        base_data = Data.get_month_data(2000, 1)
        data = Data.filter_methods(base_data, [1000])
        self.assertEqual(data.count(), 0)

    def test_filter_methods_empty(self):
        base_data = Data.get_month_data(1999, 1)
        data = Data.filter_methods(base_data, [1, 3])
        self.assertEqual(data.count(), 0)

    def test_filter_categories(self):
        base_data = Data.get_month_data(2000, 1)
        data = Data.filter_categories(base_data, [1])
        expects = [
            "コンビニ",
            "スーパー",
            "立替分1"
        ]
        self._assert_list(data, expects)

    def test_filter_categories_nothing(self):
        base_data = Data.get_month_data(2000, 1)
        data = Data.filter_categories(base_data, [100])
        self.assertEqual(data.count(), 0)

    def test_filter_categories_empty(self):
        base_data = Data.get_month_data(1999, 1)
        data = Data.filter_categories(base_data, [1])
        self.assertEqual(data.count(), 0)

    def test_filter_temps(self):
        base_data = Data.get_month_data(2000, 1)
        data = Data.filter_temps(base_data, [True])
        expects = [
            "立替分1",
            "立替分2"
        ]
        self._assert_list(data, expects)

    def test_filter_temps_nothing(self):
        base_data = Data.get_month_data(2000, 2)
        data = Data.filter_temps(base_data, [True])
        self.assertEqual(data.count(), 0)

    def test_filter_temps_empty(self):
        base_data = Data.get_month_data(1999, 1)
        data = Data.filter_temps(base_data, [True])
        self.assertEqual(data.count(), 0)

    def test_filter_checkeds(self):
        base_data = Data.get_month_data(2000, 1)
        data = Data.filter_checkeds(base_data, [False])
        expects = [
            "必需品1",
            "スーパー",
            "計算外",
            "貯金",
            "PayPayチャージ",
            "立替分1"
        ]
        self._assert_list(data, expects)

    def test_filter_checkeds_nothing(self):
        base_data = Data.get_month_data(2000, 2)
        data = Data.filter_checkeds(base_data, [False])
        self.assertEqual(data.count(), 0)

    def test_filter_checkeds_empty(self):
        base_data = Data.get_month_data(1999, 1)
        data = Data.filter_checkeds(base_data, [True])
        self.assertEqual(data.count(), 0)


class CheckedDateTestCase(CommonTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        method1 = Method.objects.create(
            show_order=1, name="1", chargeable=True)
        method2 = Method.objects.create(
            show_order=2, name="2", chargeable=False)

        CheckedDate.objects.create(method=method1, date=date(2000, 1, 1))
        CheckedDate.objects.create(method=method2, date=date(2000, 2, 1))

    def test_get(self):
        self.assertEqual(CheckedDate.get(1).date, date(2000, 1, 1))
        self.assertEqual(CheckedDate.get(2).date, date(2000, 2, 1))

    def test_set(self):
        CheckedDate.set(1, date(2001, 1, 1))
        self.assertEqual(CheckedDate.get(1).date, date(2001, 1, 1))


class CreditCheckedDateTestCase(CommonTestCase):
    def setUp(self):
        super().setUp()
        CreditCheckedDate.objects.create(
            show_order=2, name="テスト2", date=date(2000, 2, 1), price=2000)
        CreditCheckedDate.objects.create(
            show_order=1, name="テスト1", date=date(2000, 1, 1), price=1000)

    def test_get_all(self):
        data = CreditCheckedDate.get_all()
        self.assertEqual(data[0].name, "テスト1")
        self.assertEqual(data[0].date, date(2000, 1, 1))
        self.assertEqual(data[0].price, 1000)
        self.assertEqual(data[1].name, "テスト2")
        self.assertEqual(data[1].price, 2000)

    def test_get_price(self):
        self.assertEqual(CreditCheckedDate.get_price(1), 2000)
        self.assertEqual(CreditCheckedDate.get_price(2), 1000)

    def test_get_price_invalid_pk(self):
        self.assertEqual(CreditCheckedDate.get_price(10000), 0)

    def test_set_date(self):
        CreditCheckedDate.set_date(2, date(2000, 1, 2))
        data = CreditCheckedDate.get_all()
        self.assertEqual(data[0].name, "テスト1")
        self.assertEqual(data[0].date, date(2000, 1, 2))

    def test_set_price(self):
        CreditCheckedDate.set_price(2, 2001)
        data = CreditCheckedDate.get_all()
        self.assertEqual(data[0].name, "テスト1")
        self.assertEqual(data[0].price, 2001)


class BankBalanceTestCase(CommonTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        BankBalance.objects.create(show_order=2, name="テスト2", price=2000)
        BankBalance.objects.create(show_order=1, name="テスト1", price=1000)

    def test_get_all(self):
        data = BankBalance.get_all()
        self.assertEqual(data[0].name, "テスト1")
        self.assertEqual(data[0].price, 1000)
        self.assertEqual(data[1].name, "テスト2")
        self.assertEqual(data[1].price, 2000)

    def test_get_price(self):
        self.assertEqual(BankBalance.get_price(1), 2000)
        self.assertEqual(BankBalance.get_price(2), 1000)

    def test_get_price_invalid_pk(self):
        self.assertEqual(BankBalance.get_price(10000), 0)

    def test_set(self):
        BankBalance.set(2, 1001)
        data = BankBalance.get_all()
        self.assertEqual(data[0].name, "テスト1")
        self.assertEqual(data[0].price, 1001)


class SeveralCostsTestCase(CommonTestCase):
    def test_get_living_cost_mark(self):
        SeveralCosts.objects.create(name="LivingCostMark", price=1000)
        self.assertEqual(SeveralCosts.get_living_cost_mark(), 1000)

    def test_get_living_cost_mark_nothing(self):
        self.assertEqual(SeveralCosts.get_living_cost_mark(), 0)

    def test_set_living_cost_mark(self):
        SeveralCosts.objects.create(name="LivingCostMark", price=1000)
        SeveralCosts.set_living_cost_mark(1001)
        self.assertEqual(SeveralCosts.get_living_cost_mark(), 1001)

    def test_set_living_cost_mark_nothing(self):
        SeveralCosts.set_living_cost_mark(1001)
        self.assertEqual(SeveralCosts.get_living_cost_mark(), 1001)

    def test_get_actual_cash_balance(self):
        SeveralCosts.objects.create(name="ActualCashBalance", price=2000)
        self.assertEqual(SeveralCosts.get_actual_cash_balance(), 2000)

    def test_get_actual_cash_balance_nothing(self):
        self.assertEqual(SeveralCosts.get_actual_cash_balance(), 0)

    def test_set_actual_cash_balance(self):
        SeveralCosts.objects.create(name="ActualCashBalance", price=2000)
        SeveralCosts.set_actual_cash_balance(2001)
        self.assertEqual(SeveralCosts.get_actual_cash_balance(), 2001)

    def test_set_actual_cash_balance_nothing(self):
        SeveralCosts.set_actual_cash_balance(2001)
        self.assertEqual(SeveralCosts.get_actual_cash_balance(), 2001)
