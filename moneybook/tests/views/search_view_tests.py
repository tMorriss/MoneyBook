from django.contrib.auth.models import User
from django.urls import reverse
from moneybook.tests.base import BaseTestCase


class SearchViewTestCase(BaseTestCase):
    def _search_common(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['app_name'], 'test-MoneyBook')
        self.assertEqual(response.context['username'].username, self.username)
        self._assert_all_directions(response)
        self._assert_all_methods(response)
        self._assert_all_unused_methods(response)
        self._assert_all_first_categories(response)
        self._assert_all_latter_categories(response)
        self._assert_all_temps(response)
        self._assert_all_checkeds(response)

    def _search_nothing_common(self, response):
        parameter_list = [
            'start_year',
            'start_month',
            'start_day',
            'end_year',
            'end_month',
            'end_day',
            'item',
            'lower_price',
            'upper_price',
            'direction',
            'method',
            'category',
            'temp',
            'checked'
        ]
        for p in parameter_list:
            with self.subTest(p=p):
                self.assertFalse(p in response.context)

    def _search_is_not_show_common(self, response):
        parameter_list = [
            'show_data',
            'income_sum',
            'outgo_sum'
        ]
        for p in parameter_list:
            with self.subTest(p=p):
                self.assertFalse(p in response.context)
        self.assertFalse(response.context['is_show'])

    def _search_all_data(self, response, expects=None, income_sum=0, outgo_sum=0):
        show_data = response.context['show_data']
        if expects is None:
            expects = []
        self._assert_list(show_data, expects)
        self.assertEqual(response.context['income_sum'], income_sum)
        self.assertEqual(response.context['outgo_sum'], outgo_sum)
        self.assertTrue(response.context['is_show'])

    def test_get_new(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:search'))
        self._search_common(response)
        self._search_nothing_common(response)
        self._search_is_not_show_common(response)

        expects = ['search.html', '_base.html']
        self._assert_templates(response.templates, expects)

    def test_get_guest(self):
        response = self.client.get(reverse('moneybook:search'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:login'))

    def test_get_new_only_is_query(self):
        """is_queryだけ指定すると全データ表示される"""
        self.client.force_login(User.objects.create_user(self.username))
        self._create_data(item='Item 1', price=100, direction_id=1)
        response = self.client.get(reverse('moneybook:search'), {'is_query': 1})
        self._search_common(response)
        self._search_nothing_common(response)
        self._search_all_data(response, expects=['Item 1'], income_sum=100, outgo_sum=0)

        expects = ['search.html', '_base.html', '_data_table.html']
        self._assert_templates(response.templates, expects)

    def test_get_empty_query(self):
        """is_query含め全部空"""
        self.client.force_login(User.objects.create_user(self.username))
        self._create_data(item='Item 1', price=100, direction_id=1)
        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': '',
                'start_year': '',
                'start_month': '',
                'start_day': '',
                'end_year': '',
                'end_month': '',
                'end_day': '',
                'item': '',
                'lower_price': '',
                'upper_price': '',
                'direction': '',
                'method': '',
                'category': '',
                'temp': '',
                'checked': ''
            }
        )

        self._search_common(response)

        # 前半部分は空として存在
        parameter_list = [
            'start_year',
            'start_month',
            'start_day',
            'end_year',
            'end_month',
            'end_day',
            'item',
            'lower_price',
            'upper_price'
        ]
        for p in parameter_list:
            with self.subTest(p=p):
                self.assertEqual(response.context[p], '')
        # 後半部分は存在しない
        parameter_list = [
            'direction',
            'method',
            'category',
            'temp',
            'checked'
        ]
        for p in parameter_list:
            with self.subTest(p=p):
                self.assertFalse(p in response.context)

        self._search_all_data(response, expects=['Item 1'], income_sum=100, outgo_sum=0)

        expects = ['search.html', '_base.html', '_data_table.html']
        self._assert_templates(response.templates, expects)

    def test_get_with_input_query(self):
        """全queryに正しい値を入れる"""
        self.client.force_login(User.objects.create_user(self.username))
        self._create_data(date='2000-01-08', item='必需品2', price=3500, direction_id=2)
        self._create_data(date='2000-01-05', item='必需品1', price=1000, direction_id=2)

        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': 1,
                'start_year': 2000,
                'start_month': 1,
                'start_day': 1,
                'end_year': 2000,
                'end_month': 1,
                'end_day': 31,
                'item': '品',
                'lower_price': 3000,
                'upper_price': 5000,
            }
        )
        self._search_common(response)
        expects = ['必需品2']
        self._assert_list(response.context['show_data'], expects)

        self.assertEqual(response.context['start_year'], '2000')
        self.assertEqual(response.context['start_month'], '1')
        self.assertEqual(response.context['start_day'], '1')
        self.assertEqual(response.context['end_year'], '2000')
        self.assertEqual(response.context['end_month'], '1')
        self.assertEqual(response.context['end_day'], '31')
        self.assertEqual(response.context['item'], '品')
        self.assertEqual(response.context['lower_price'], '3000')
        self.assertEqual(response.context['upper_price'], '5000')

        expects = ['search.html', '_base.html', '_data_table.html']
        self._assert_templates(response.templates, expects)
        self.assertEqual(response.context['income_sum'], 0)
        self.assertEqual(response.context['outgo_sum'], 3500)
        self.assertTrue(response.context['is_show'])

    def test_get_with_direction(self):
        self.client.force_login(User.objects.create_user(self.username))
        self._create_data(item='Income', price=100, direction_id=1)
        self._create_data(item='Outgo', price=200, direction_id=2)

        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': 1,
                'direction': 1
            }
        )
        self._search_common(response)
        self._search_all_data(response, expects=['Income'], income_sum=100, outgo_sum=0)

    def test_get_with_two_direction(self):
        self.client.force_login(User.objects.create_user(self.username))
        self._create_data(item='Income', price=100, direction_id=1)
        self._create_data(item='Outgo', price=200, direction_id=2)

        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': 1,
                'direction': [1, 2]
            }
        )
        self._search_common(response)
        self._search_all_data(response, expects=['Income', 'Outgo'], income_sum=100, outgo_sum=200)

    def test_get_with_method(self):
        self.client.force_login(User.objects.create_user(self.username))
        self._create_data(item='M2', price=100, method_id=2, direction_id=1)
        self._create_data(item='M1', price=200, method_id=1, direction_id=2)

        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': 1,
                'method': 2  # 銀行
            }
        )
        self._search_common(response)
        self._search_all_data(response, expects=['M2'], income_sum=100, outgo_sum=0)

    def test_get_with_two_method(self):
        self.client.force_login(User.objects.create_user(self.username))
        self._create_data(item='M2', price=100, method_id=2, direction_id=1)
        self._create_data(item='M1', price=200, method_id=1, direction_id=2)

        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': 1,
                'method': [1, 2]
            }
        )
        self._search_common(response)
        self._search_all_data(response, expects=['M2', 'M1'], income_sum=100, outgo_sum=200)

    def test_get_with_category(self):
        self.client.force_login(User.objects.create_user(self.username))
        self._create_data(item='C4', price=100, category_id=4, direction_id=2)
        self._create_data(item='C1', price=200, category_id=1, direction_id=2)

        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': 1,
                'category': 4
            }
        )
        self._search_common(response)
        self._search_all_data(response, expects=['C4'], income_sum=0, outgo_sum=100)

    def test_get_with_two_category(self):
        self.client.force_login(User.objects.create_user(self.username))
        self._create_data(item='C4', price=100, category_id=4, direction_id=2)
        self._create_data(item='C1', price=200, category_id=1, direction_id=2)

        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': 1,
                'category': [1, 4]
            }
        )
        self._search_common(response)
        self._search_all_data(response, expects=['C4', 'C1'], income_sum=0, outgo_sum=300)

    def test_get_with_tmp(self):
        self.client.force_login(User.objects.create_user(self.username))
        self._create_data(item='T', price=100, temp=True, direction_id=1)
        self._create_data(item='N', price=200, temp=False, direction_id=1)

        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': 1,
                'temp': 1
            }
        )
        self._search_common(response)
        self._search_all_data(response, expects=['T'], income_sum=100, outgo_sum=0)

    def test_get_with_two_tmp(self):
        self.client.force_login(User.objects.create_user(self.username))
        self._create_data(item='T', price=100, temp=True, direction_id=1)
        self._create_data(item='N', price=200, temp=False, direction_id=1)

        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': 1,
                'temp': [0, 1]
            }
        )
        self._search_common(response)
        self._search_all_data(response, expects=['T', 'N'], income_sum=300, outgo_sum=0)

    def test_get_with_checked(self):
        self.client.force_login(User.objects.create_user(self.username))
        self._create_data(item='C', price=100, checked=True, direction_id=1)
        self._create_data(item='U', price=200, checked=False, direction_id=1)

        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': 1,
                'checked': 0
            }
        )
        self._search_common(response)
        self._search_all_data(response, expects=['U'], income_sum=200, outgo_sum=0)

    def test_get_with_two_checked(self):
        self.client.force_login(User.objects.create_user(self.username))
        self._create_data(item='C', price=100, checked=True, direction_id=1)
        self._create_data(item='U', price=200, checked=False, direction_id=1)

        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': 1,
                'checked': [0, 1]
            }
        )
        self._search_common(response)
        self._search_all_data(response, expects=['C', 'U'], income_sum=300, outgo_sum=0)

    def test_get_with_invalid_start_date(self):
        self.client.force_login(User.objects.create_user(self.username))
        self._create_data(item='Item 1', price=100, direction_id=1)

        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': 1,
                'start_year': 2000,
                'start_month': 13,
                'start_day': 1,
            }
        )
        self._search_common(response)
        self._search_all_data(response, expects=['Item 1'], income_sum=100, outgo_sum=0)

    def test_get_with_invalid_end_date(self):
        self.client.force_login(User.objects.create_user(self.username))
        self._create_data(item='Item 1', price=100, direction_id=1)

        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': 1,
                'end_year': 2000,
                'end_month': 13,
                'end_day': 1,
            }
        )
        self._search_common(response)
        self._search_all_data(response, expects=['Item 1'], income_sum=100, outgo_sum=0)

    def test_get_with_invalid_lower_price(self):
        self.client.force_login(User.objects.create_user(self.username))
        self._create_data(item='Item 1', price=100, direction_id=1)

        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': 1,
                'lower_price': 'a',
            }
        )
        self._search_common(response)
        self._search_all_data(response, expects=['Item 1'], income_sum=100, outgo_sum=0)

    def test_get_with_invalid_upper_price(self):
        self.client.force_login(User.objects.create_user(self.username))
        self._create_data(item='Item 1', price=100, direction_id=1)

        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': 1,
                'upper_price': 'a',
            }
        )
        self._search_common(response)
        self._search_all_data(response, expects=['Item 1'], income_sum=100, outgo_sum=0)
