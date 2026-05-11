from datetime import date

from moneybook.models import Category, Data, Direction, Method
from moneybook.tests.base import BaseTestCase


class DataTestCase(BaseTestCase):
    def test_get_all_data(self):
        self._create_data(item='item 1')
        self._create_data(item='item 2')
        self.assertEqual(Data.get_all_data().count(), 2)

    def test_get_range_data(self):
        self._create_data(date='2000-01-01', item='A')
        self._create_data(date='2000-01-05', item='B')
        self._create_data(date='2000-01-10', item='C')
        self._create_data(date='2000-01-11', item='D')

        start = date(2000, 1, 1)
        end = date(2000, 1, 10)
        data = Data.get_range_data(start, end)
        expects = [
            'A',
            'B',
            'C'
        ]
        self._assert_list(data, expects)

    def test_get_range_data_nothing(self):
        start = date(1999, 1, 1)
        end = date(1999, 12, 30)
        data = Data.get_range_data(start, end)
        self.assertEqual(data.count(), 0)

    def test_get_month_data(self):
        self._create_data(date='2000-01-01', item='Jan')
        self._create_data(date='2000-02-01', item='Feb')
        data = Data.get_month_data(2000, 1)
        expects = [
            'Jan'
        ]
        self._assert_list(data, expects)

    def test_get_month_data_nothing(self):
        data = Data.get_month_data(1999, 1)
        self.assertEqual(data.count(), 0)

    def test_get_month_data_out(self):
        data = Data.get_month_data(2000, 13)
        self.assertEqual(data.count(), 0)

    def test_get_sum_one(self):
        self._create_data(date='2000-01-01', price=100, direction_id=1)
        self._create_data(date='2000-01-02', price=200, direction_id=1)
        self._create_data(date='2000-01-03', price=300, direction_id=2)
        data = Data.get_month_data(2000, 1)
        self.assertEqual(Data.get_sum(data, 1), 300)

    def test_get_sum_one_empty(self):
        data = Data.get_month_data(1999, 1)
        self.assertEqual(Data.get_sum(data, 1), 0)

    def test_get_sum_two(self):
        self._create_data(date='2000-01-01', price=100, direction_id=1)
        self._create_data(date='2000-01-02', price=200, direction_id=2)
        self._create_data(date='2000-01-03', price=300, direction_id=2)
        data = Data.get_month_data(2000, 1)
        self.assertEqual(Data.get_sum(data, 2), 500)

    def test_get_sum_two_empty(self):
        data = Data.get_month_data(1999, 1)
        self.assertEqual(Data.get_sum(data, 2), 0)

    def test_get_sum_nothing(self):
        self._create_data(date='2000-01-01', price=100, direction_id=1)
        data = Data.get_month_data(2000, 1)
        self.assertEqual(Data.get_sum(data, 3), 0)

    def test_get_income_sum(self):
        self._create_data(date='2000-01-01', price=100, direction_id=1)
        self._create_data(date='2000-01-02', price=200, direction_id=2)
        data = Data.get_month_data(2000, 1)
        self.assertEqual(Data.get_income_sum(data), 100)

    def test_get_income_sum_nothing(self):
        data = Data.get_month_data(1999, 1)
        self.assertEqual(Data.get_income_sum(data), 0)

    def test_get_outgo_sum(self):
        self._create_data(date='2000-01-01', price=100, direction_id=1)
        self._create_data(date='2000-01-02', price=200, direction_id=2)
        data = Data.get_month_data(2000, 1)
        self.assertEqual(Data.get_outgo_sum(data), 200)

    def test_get_outgo_sum_nothing(self):
        data = Data.get_month_data(1999, 1)
        self.assertEqual(Data.get_outgo_sum(data), 0)

    def test_get_income(self):
        self._create_data(date='2000-01-01', item='Income', direction_id=1)
        self._create_data(date='2000-01-02', item='Outgo', direction_id=2)
        data = Data.get_month_data(2000, 1)
        income_data = Data.get_income(data)
        expects = ['Income']
        self._assert_list(income_data, expects)

    def test_get_outgo(self):
        self._create_data(date='2000-01-01', item='Income', direction_id=1)
        self._create_data(date='2000-01-02', item='Outgo', direction_id=2)
        data = Data.get_month_data(2000, 1)
        outgo_data = Data.get_outgo(data)
        expects = ['Outgo']
        self._assert_list(outgo_data, expects)

    def test_get_pre_checked_data(self):
        self._create_data(item='A', checked=False, pre_checked=False)
        self._create_data(item='B', checked=False, pre_checked=True)
        all_data = Data.get_all_data()
        unchecked_data = Data.get_unchecked_data(all_data)
        pre_checked_data = Data.get_pre_checked_data(unchecked_data)
        self.assertEqual(len(pre_checked_data), 1)
        self.assertEqual(pre_checked_data[0].item, 'B')

    def test_get_method_data(self):
        self._create_data(date='2000-01-01', item='M1', method_id=1)
        self._create_data(date='2000-01-02', item='M2', method_id=2)
        month_data = Data.get_month_data(2000, 1)
        data = Data.get_method_data(month_data, 1)
        expects = [
            'M1'
        ]
        self._assert_list(data, expects)

    def test_get_method_data_nothing(self):
        self._create_data(date='2000-01-01', item='M1', method_id=1)
        month_data = Data.get_month_data(2000, 1)
        data = Data.get_method_data(month_data, 100)
        self.assertEqual(data.count(), 0)

    def test_get_method_data_empty(self):
        month_data = Data.get_month_data(1999, 1)
        data = Data.get_method_data(month_data, 1)
        self.assertEqual(data.count(), 0)

    def test_get_category_data(self):
        self._create_data(date='2000-01-01', item='C1', category_id=1)
        self._create_data(date='2000-01-02', item='C2', category_id=2)
        month_data = Data.get_month_data(2000, 1)
        data = Data.get_category_data(month_data, 1)
        expects = [
            'C1'
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
        self._create_data(date='2000-01-01', price=400, temp=True)
        self._create_data(date='2000-01-02', price=600, temp=True)
        self._create_data(date='2000-01-03', price=100, temp=False)
        data = Data.get_month_data(2000, 1)
        self.assertEqual(Data.get_temp_sum(data), 1000)

    def test_get_temp_sum_nothing(self):
        self._create_data(date='2000-02-01', price=100, temp=False)
        data = Data.get_month_data(2000, 2)
        self.assertEqual(Data.get_temp_sum(data), 0)

    def test_get_temp_sum_empty(self):
        data = Data.get_month_data(1999, 1)
        self.assertEqual(Data.get_temp_sum(data), 0)

    def test_get_deposit_sum(self):
        Data.objects.create(
            date=date(2100, 1, 1),
            item='貯金',
            price=1000,
            direction=Direction.get(2),
            method=Method.get(1),
            category=Category.get(5),
            temp=False)
        Data.objects.create(
            date=date(2100, 1, 1),
            item='貯金代',
            price=500,
            direction=Direction.get(1),
            method=Method.get(1),
            category=Category.get(5),
            temp=True)
        data = Data.get_month_data(2100, 1)
        self.assertEqual(Data.get_deposit_sum(data), 500)

    def test_get_deposit_sum_nothing(self):
        data = Data.get_month_data(2000, 2)
        self.assertEqual(Data.get_deposit_sum(data), 0)

    def test_get_deposit_sum_empty(self):
        data = Data.get_month_data(1999, 1)
        self.assertEqual(Data.get_deposit_sum(data), 0)

    def test_filter_without_intra_move(self):
        self._create_data(date='2000-01-01', item='Normal')
        self._create_data(date='2000-01-02', item='Intra', category_id=4)
        base_data = Data.get_month_data(2000, 1)
        data = Data.filter_without_intra_move(base_data)
        expects = [
            'Normal'
        ]
        self._assert_list(data, expects)

    def test_filter_without_intra_move_nothing(self):
        self._create_data(date='2000-04-01', item='Intra', category_id=4)
        base_data = Data.get_month_data(2000, 4)
        data = Data.filter_without_intra_move(base_data)
        self.assertEqual(data.count(), 0)

    def test_filter_without_intra_move_empty(self):
        base_data = Data.get_month_data(1999, 1)
        data = Data.filter_without_intra_move(base_data)
        self.assertEqual(data.count(), 0)

    def test_get_normal_data(self):
        """計算外と内部移動を除く"""
        self._create_data(date='2000-01-01', item='Normal')
        self._create_data(date='2000-01-02', item='Intra', category_id=4)
        self._create_data(date='2000-01-03', item='Excl', category_id=6)
        base_data = Data.get_month_data(2000, 1)
        data = Data.get_normal_data(base_data)
        expects = [
            'Normal'
        ]
        self._assert_list(data, expects)

    def test_get_normal_data_nothing(self):
        self._create_data(date='2000-04-01', item='Intra', category_id=4)
        base_data = Data.get_month_data(2000, 4)
        data = Data.get_normal_data(base_data)
        self.assertEqual(data.count(), 0)

    def test_get_normal_data_empty(self):
        base_data = Data.get_month_data(1999, 1)
        data = Data.get_normal_data(base_data)
        self.assertEqual(data.count(), 0)

    def test_get_living_cost(self):
        # Category 1 is living cost (食費)
        self._create_data(date='2000-01-01', price=2500, category_id=1)
        self._create_data(date='2000-01-02', price=1000, category_id=2)   # Not living cost
        data = Data.get_month_data(2000, 1)
        self.assertEqual(Data.get_living_cost(data), 2500)

    def test_get_living_cost_nothing(self):
        data = Data.get_month_data(1999, 1)
        self.assertEqual(Data.get_living_cost(data), 0)

    def test_get_variable_cost(self):
        # Category 2 and 8 are variable costs (必需品, 交通費)
        self._create_data(date='2000-01-01', price=5000, category_id=2)
        self._create_data(date='2000-01-02', price=390, category_id=8)
        self._create_data(date='2000-01-03', price=100, category_id=1)   # Not variable cost
        data = Data.get_month_data(2000, 1)
        self.assertEqual(Data.get_variable_cost(data), 5390)

    def test_get_variable_data_nothing(self):
        data = Data.get_month_data(1999, 1)
        self.assertEqual(Data.get_variable_cost(data), 0)

    def test_get_food_costs(self):
        # Category 1 is food cost
        self._create_data(date='2000-01-01', price=2500, category_id=1)
        self._create_data(date='2000-01-02', price=1000, category_id=2)
        data = Data.get_month_data(2000, 1)
        self.assertEqual(Data.get_food_costs(data), 2500)

    def test_get_food_costs_nothing(self):
        data = Data.get_month_data(1999, 1)
        self.assertEqual(Data.get_food_costs(data), 0)

    def test_sort_ascending(self):
        self._create_data(date='2000-01-02', item='Second')
        self._create_data(date='2000-01-01', item='First')
        base_data = Data.get_month_data(2000, 1)
        data = Data.sort_ascending(base_data)
        expects = [
            'First',
            'Second'
        ]
        self._assert_list(data, expects)

    def test_sort_ascending_nothing(self):
        data = Data.get_month_data(1999, 1)
        sorted_data = Data.sort_ascending(data)
        self.assertEqual(sorted_data.count(), 0)

    def test_sort_descending(self):
        self._create_data(date='2000-01-01', item='First')
        self._create_data(date='2000-01-02', item='Second')
        base_data = Data.get_month_data(2000, 1)
        data = Data.sort_descending(base_data)
        expects = [
            'Second',
            'First'
        ]
        self._assert_list(data, expects)

    def test_sort_descending_nothing(self):
        data = Data.get_month_data(1999, 1)
        sorted_data = Data.sort_descending(data)
        self.assertEqual(sorted_data.count(), 0)

    def test_get_keyword_data_part(self):
        self._create_data(date='2000-01-01', item='Apple')
        self._create_data(date='2000-01-02', item='Pineapple')
        self._create_data(date='2000-01-03', item='Banana')
        base_data = Data.get_month_data(2000, 1)
        data = Data.get_keyword_data(base_data, 'Apple')
        expects = [
            'Apple',
            'Pineapple'
        ]
        self._assert_list(data, expects)

    def test_get_keyword_data_same(self):
        self._create_data(date='2000-01-01', item='Apple')
        base_data = Data.get_month_data(2000, 1)
        data = Data.get_keyword_data(base_data, 'Apple')
        self.assertEqual(data.count(), 1)
        self.assertEqual(str(data[0]), 'Apple')

    def test_get_keyword_data_nothing(self):
        self._create_data(date='2000-01-01', item='Apple')
        base_data = Data.get_month_data(2000, 1)
        data = Data.get_keyword_data(base_data, 'カレーライス')
        self.assertEqual(data.count(), 0)

    def test_get_keyword_data_empty(self):
        base_data = Data.get_month_data(1999, 1)
        data = Data.get_keyword_data(base_data, 'カレーライス')
        self.assertEqual(data.count(), 0)

    def test_get_cash_data(self):
        self._create_data(date='2000-01-01', item='Cash', method_id=1)
        self._create_data(date='2000-01-02', item='Bank', method_id=2)
        base_data = Data.get_month_data(2000, 1)
        data = Data.get_cash_data(base_data)
        expects = [
            'Cash'
        ]
        self._assert_list(data, expects)

    def test_get_cash_data_nothing(self):
        self._create_data(date='2000-02-01', item='Cash', method_id=1)
        base_data = Data.get_month_data(2000, 1)
        data = Data.get_cash_data(base_data)
        self.assertEqual(data.count(), 0)

    def test_get_cash_data_empty(self):
        base_data = Data.get_month_data(1999, 1)
        data = Data.get_cash_data(base_data)
        self.assertEqual(data.count(), 0)

    def test_get_bank_data(self):
        self._create_data(date='2000-01-01', item='Bank', method_id=2)
        self._create_data(date='2000-01-02', item='Cash', method_id=1)
        base_data = Data.get_month_data(2000, 1)
        data = Data.get_bank_data(base_data)
        expects = [
            'Bank'
        ]
        self._assert_list(data, expects)

    def test_get_bank_data_nothing(self):
        self._create_data(date='2000-04-01', item='Cash', method_id=1)
        base_data = Data.get_month_data(2000, 4)
        data = Data.get_bank_data(base_data)
        self.assertEqual(data.count(), 0)

    def test_get_bank_data_empty(self):
        base_data = Data.get_month_data(1999, 1)
        data = Data.get_bank_data(base_data)
        self.assertEqual(data.count(), 0)

    def test_get_checked_data(self):
        self._create_data(date='2000-01-01', item='Checked', checked=True)
        self._create_data(date='2000-01-02', item='Unchecked', checked=False)
        base_data = Data.get_month_data(2000, 1)
        data = Data.get_checked_data(base_data)
        expects = [
            'Checked'
        ]
        self._assert_list(data, expects)

    def test_get_checked_data_nothing(self):
        self._create_data(date='2000-04-01', item='Unchecked', checked=False)
        base_data = Data.get_month_data(2000, 4)
        data = Data.get_checked_data(base_data)
        self.assertEqual(data.count(), 0)

    def test_get_checked_data_empty(self):
        base_data = Data.get_month_data(1999, 1)
        data = Data.get_checked_data(base_data)
        self.assertEqual(data.count(), 0)

    def test_get_unchecked_data(self):
        self._create_data(date='2000-01-01', item='Checked', checked=True)
        self._create_data(date='2000-01-02', item='Unchecked', checked=False)
        base_data = Data.get_month_data(2000, 1)
        data = Data.get_unchecked_data(base_data)
        expects = [
            'Unchecked'
        ]
        self._assert_list(data, expects)

    def test_get_unchecked_data_nothing(self):
        self._create_data(date='2000-02-01', item='Checked', checked=True)
        base_data = Data.get_month_data(2000, 2)
        data = Data.get_unchecked_data(base_data)
        self.assertEqual(data.count(), 0)

    def test_get_unchecked_data_empty(self):
        base_data = Data.get_month_data(1999, 1)
        data = Data.get_unchecked_data(base_data)
        self.assertEqual(data.count(), 0)

    def test_get(self):
        self._create_data(pk=1, item='A')
        self._create_data(pk=6, item='B')
        self.assertEqual(str(Data.get(1)), 'A')
        self.assertEqual(str(Data.get(6)), 'B')

    def test_get_nothing(self):
        self.assertRaises(Data.DoesNotExist, Data.get, 100)

    def test_filter_price(self):
        self._create_data(date='2000-01-01', item='P100', price=100)
        self._create_data(date='2000-01-02', item='P400', price=400)
        self._create_data(date='2000-01-03', item='P500', price=500)
        base_data = Data.get_month_data(2000, 1)
        data = Data.filter_price(base_data, 100, 400)
        expects = [
            'P100',
            'P400'
        ]
        self._assert_list(data, expects)

    def test_filter_price_lower(self):
        self._create_data(date='2000-01-01', item='P2999', price=2999)
        self._create_data(date='2000-01-02', item='P3000', price=3000)
        base_data = Data.get_month_data(2000, 1)
        data = Data.filter_price(base_data, 3000, None)
        expects = [
            'P3000'
        ]
        self._assert_list(data, expects)

    def test_filter_price_upper(self):
        self._create_data(date='2000-01-01', item='P130', price=130)
        self._create_data(date='2000-01-02', item='P131', price=131)
        base_data = Data.get_month_data(2000, 1)
        data = Data.filter_price(base_data, None, 130)
        expects = [
            'P130'
        ]
        self._assert_list(data, expects)

    def test_filter_price_nothing(self):
        self._create_data(date='2000-01-01', price=100)
        base_data = Data.get_month_data(2000, 1)
        data = Data.filter_price(base_data, None, 10)
        self.assertEqual(data.count(), 0)

    def test_filter_price_empty(self):
        base_data = Data.get_month_data(1999, 1)
        data = Data.filter_price(base_data, 10, 1000)
        self.assertEqual(data.count(), 0)

    def test_filter_directions(self):
        self._create_data(date='2000-01-01', item='D1', direction_id=1)
        self._create_data(date='2000-01-02', item='D2', direction_id=2)
        base_data = Data.get_month_data(2000, 1)
        data = Data.filter_directions(base_data, [1])
        expects = [
            'D1'
        ]
        self._assert_list(data, expects)

    def test_filter_directions_nothing(self):
        self._create_data(date='2000-01-01', direction_id=1)
        base_data = Data.get_month_data(2000, 1)
        data = Data.filter_directions(base_data, [1000])
        self.assertEqual(data.count(), 0)

    def test_filter_directions_empty(self):
        base_data = Data.get_month_data(1999, 1)
        data = Data.filter_directions(base_data, [1])
        self.assertEqual(data.count(), 0)

    def test_filter_methods(self):
        self._create_data(date='2000-01-01', item='M1', method_id=1)
        self._create_data(date='2000-01-02', item='M2', method_id=2)
        self._create_data(date='2000-01-03', item='M3', method_id=3)
        base_data = Data.get_month_data(2000, 1)
        data = Data.filter_methods(base_data, [1, 3])
        expects = [
            'M1',
            'M3'
        ]
        self._assert_list(data, expects)

    def test_filter_methods_nothing(self):
        self._create_data(date='2000-01-01', method_id=1)
        base_data = Data.get_month_data(2000, 1)
        data = Data.filter_methods(base_data, [1000])
        self.assertEqual(data.count(), 0)

    def test_filter_methods_empty(self):
        base_data = Data.get_month_data(1999, 1)
        data = Data.filter_methods(base_data, [1, 3])
        self.assertEqual(data.count(), 0)

    def test_filter_categories(self):
        self._create_data(date='2000-01-01', item='C1', category_id=1)
        self._create_data(date='2000-01-02', item='C2', category_id=2)
        base_data = Data.get_month_data(2000, 1)
        data = Data.filter_categories(base_data, [1])
        expects = [
            'C1'
        ]
        self._assert_list(data, expects)

    def test_filter_categories_nothing(self):
        self._create_data(date='2000-01-01', category_id=1)
        base_data = Data.get_month_data(2000, 1)
        data = Data.filter_categories(base_data, [100])
        self.assertEqual(data.count(), 0)

    def test_filter_categories_empty(self):
        base_data = Data.get_month_data(1999, 1)
        data = Data.filter_categories(base_data, [1])
        self.assertEqual(data.count(), 0)

    def test_filter_temps(self):
        self._create_data(date='2000-01-01', item='T1', temp=True)
        self._create_data(date='2000-01-02', item='T2', temp=False)
        base_data = Data.get_month_data(2000, 1)
        data = Data.filter_temps(base_data, [True])
        expects = [
            'T1'
        ]
        self._assert_list(data, expects)

    def test_filter_temps_nothing(self):
        self._create_data(date='2000-02-01', temp=False)
        base_data = Data.get_month_data(2000, 2)
        data = Data.filter_temps(base_data, [True])
        self.assertEqual(data.count(), 0)

    def test_filter_temps_empty(self):
        base_data = Data.get_month_data(1999, 1)
        data = Data.filter_temps(base_data, [True])
        self.assertEqual(data.count(), 0)

    def test_filter_checkeds(self):
        self._create_data(date='2000-01-01', item='CH1', checked=True)
        self._create_data(date='2000-01-02', item='CH2', checked=False)
        base_data = Data.get_month_data(2000, 1)
        data = Data.filter_checkeds(base_data, [False])
        expects = [
            'CH2'
        ]
        self._assert_list(data, expects)

    def test_filter_checkeds_nothing(self):
        self._create_data(date='2000-02-01', checked=True)
        base_data = Data.get_month_data(2000, 2)
        data = Data.filter_checkeds(base_data, [False])
        self.assertEqual(data.count(), 0)

    def test_filter_checkeds_empty(self):
        base_data = Data.get_month_data(1999, 1)
        data = Data.filter_checkeds(base_data, [True])
        self.assertEqual(data.count(), 0)
