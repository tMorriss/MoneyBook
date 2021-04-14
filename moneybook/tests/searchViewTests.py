from django.contrib.auth.models import User
from django.urls import reverse
from moneybook.tests.common import CommonTestCase


class SearchViewTestCase(CommonTestCase):
    fixtures = ['data_test_case']
    username = 'tester'

    def _search_common(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['app_name'], 'test-MoneyBook')
        self.assertEqual(
            response.context['username'].username, self.username)
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

    def _search_all_data(self, response):
        show_data = response.context['show_data']
        expects = [
            '松屋',
            '給与',
            'コンビニ',
            'その他1',
            '必需品1',
            '必需品2',
            '現金収入',
            '銀行収入',
            'スーパー',
            '計算外',
            '貯金',
            'PayPayチャージ',
            'PayPayチャージ',
            '電気代',
            'ガス代',
            '水道代',
            '立替分1',
            '立替分2',
            '給与',
            '必需品3',
            '内部移動1',
            '水道代',
            '内部移動2'
        ]
        self._assert_list(show_data, expects)
        self.assertEqual(response.context['income_sum'], 59444)
        self.assertEqual(response.context['outgo_sum'], 12750)
        self.assertTrue(response.context['is_show'])

    def test_search_new(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:search'))
        self._search_common(response)
        self._search_nothing_common(response)
        self._search_is_not_show_common(response)

        expects = ['search.html', '_base.html']
        self._assert_templates(response.templates, expects)

    def test_search_guest(self):
        response = self.client.get(reverse('moneybook:search'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:login'))

    def test_search_new_only_is_query(self):
        '''is_queryだけ指定すると全データ表示される'''
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:search'), {'is_query': 1})
        self._search_common(response)
        self._search_nothing_common(response)
        self._search_all_data(response)

        expects = ['search.html', '_base.html', '_data_table.html']
        self._assert_templates(response.templates, expects)

    def test_search_empty_query(self):
        '''is_query含め全部空'''
        self.client.force_login(User.objects.create_user(self.username))
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

        self._search_all_data(response)

        expects = ['search.html', '_base.html', '_data_table.html']
        self._assert_templates(response.templates, expects)

    def test_search_with_input_query(self):
        '''全queryに正しい値を入れる'''
        self.client.force_login(User.objects.create_user(self.username))
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

    def test_search_with_direction(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': 1,
                'direction': 1
            }
        )
        self._search_common(response)
        show_data = response.context['show_data']
        expects = ['給与', '現金収入', '銀行収入', 'PayPayチャージ', '立替分1', '立替分2', '給与']
        self._assert_list(show_data, expects)
        self.assertEqual(response.context['income_sum'], 59444)
        self.assertEqual(response.context['outgo_sum'], 0)
        self.assertTrue(response.context['is_show'])

    def test_search_with_two_direction(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': 1,
                'direction': [1, 2]
            }
        )
        self._search_common(response)
        self._search_all_data(response)

    def test_search_with_method(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': 1,
                'method': 2  # 銀行
            }
        )
        self._search_common(response)
        show_data = response.context['show_data']
        expects = ['給与', '必需品1', '銀行収入', '計算外', '貯金',
                   'PayPayチャージ', '電気代', 'ガス代', '水道代', '立替分2', '給与', '水道代']
        self._assert_list(show_data, expects)
        self.assertEqual(response.context['income_sum'], 56044)
        self.assertEqual(response.context['outgo_sum'], 3620)
        self.assertTrue(response.context['is_show'])

    def test_search_with_two_method(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': 1,
                'method': [2, 3]  # 銀行,PayPay
            }
        )
        self._search_common(response)
        show_data = response.context['show_data']
        expects = [
            '給与', '必需品1', '銀行収入', '計算外', '貯金', 'PayPayチャージ',
            'PayPayチャージ', '電気代', 'ガス代', '水道代', '立替分1', '立替分2', '給与', '必需品3', '内部移動1', '水道代', '内部移動2']
        self._assert_list(show_data, expects)
        self.assertEqual(response.context['income_sum'], 56444)
        self.assertEqual(response.context['outgo_sum'], 5820)
        self.assertTrue(response.context['is_show'])

    def test_search_with_category(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': 1,
                'category': 4
            }
        )
        self._search_common(response)
        show_data = response.context['show_data']
        expects = ['PayPayチャージ', 'PayPayチャージ', '内部移動1', '内部移動2']
        self._assert_list(show_data, expects)
        self.assertEqual(response.context['income_sum'], 1000)
        self.assertEqual(response.context['outgo_sum'], 1800)
        self.assertTrue(response.context['is_show'])

    def test_search_with_two_category(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': 1,
                'category': [4, 5]
            }
        )
        self._search_common(response)
        show_data = response.context['show_data']
        expects = ['貯金', 'PayPayチャージ', 'PayPayチャージ', '内部移動1', '内部移動2']
        self._assert_list(show_data, expects)
        self.assertEqual(response.context['income_sum'], 1000)
        self.assertEqual(response.context['outgo_sum'], 1930)
        self.assertTrue(response.context['is_show'])

    def test_search_with_tmp(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': 1,
                'temp': 1
            }
        )
        self._search_common(response)
        show_data = response.context['show_data']
        expects = ['立替分1', '立替分2']
        self._assert_list(show_data, expects)
        self.assertEqual(response.context['income_sum'], 1000)
        self.assertEqual(response.context['outgo_sum'], 0)
        self.assertTrue(response.context['is_show'])

    def test_search_with_two_tmp(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': 1,
                'temp': [1, 2]
            }
        )
        self._search_common(response)
        self._search_all_data(response)

    def test_search_with_checked(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': 1,
                'checked': 0
            }
        )
        self._search_common(response)
        show_data = response.context['show_data']
        expects = ['必需品1', 'スーパー', '計算外',  '貯金',
                   'PayPayチャージ', '立替分1', '内部移動1', '内部移動2']
        self._assert_list(show_data, expects)
        self.assertEqual(response.context['income_sum'], 400)
        self.assertEqual(response.context['outgo_sum'], 6230)
        self.assertTrue(response.context['is_show'])

    def test_search_with_two_checked(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': 1,
                'temp': [0, 1]
            }
        )
        self._search_common(response)
        self._search_all_data(response)
        self.assertTrue(response.context['is_show'])

    def test_search_with_invalid_start_date(self):
        self.client.force_login(User.objects.create_user(self.username))
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
        self._search_all_data(response)
        self.assertTrue(response.context['is_show'])

    def test_search_with_invalid_end_date(self):
        self.client.force_login(User.objects.create_user(self.username))
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
        self._search_all_data(response)

    def test_search_with_invalid_lower_price(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': 1,
                'lower_price': 'a',
            }
        )
        self._search_common(response)
        self._search_all_data(response)

    def test_search_with_invalid_upper_price(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:search'),
            {
                'is_query': 1,
                'upper_price': 'a',
            }
        )
        self._search_common(response)
        self._search_all_data(response)
