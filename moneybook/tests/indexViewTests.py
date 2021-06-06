from datetime import datetime
from unittest.mock import patch

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse
from moneybook.tests.base import BaseTestCase
from moneybook.views import IndexMonthView


class IndexViewTestCase(BaseTestCase):
    @patch.object(IndexMonthView, 'get', return_value=HttpResponse())
    def test_get(self, index_month):
        now = datetime.now()
        self.client.force_login(User.objects.create_user(self.username))
        self.client.get(reverse('moneybook:index'))
        kwargs = IndexMonthView.get.call_args.kwargs
        self.assertEqual(kwargs['year'], now.year)
        self.assertEqual(kwargs['month'], now.month)

    def test_get_guest(self):
        response = self.client.get(reverse('moneybook:index'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:login'))


class IndexMonthViewTestCase(BaseTestCase):
    def test_get(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:index_month', kwargs={'year': 2000, 'month': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['app_name'], 'test-MoneyBook')
        self.assertEqual(
            response.context['username'].username, self.username)
        self.assertEqual(response.context['year'], 2000)
        self.assertEqual(response.context['month'], 1)
        self.assertEqual(response.context['next_year'], 2000)
        self.assertEqual(response.context['next_month'], 2)
        self.assertEqual(response.context['last_year'], 1999)
        self.assertEqual(response.context['last_month'], 12)
        self._assert_all_directions(response)
        self._assert_all_methods(response)
        self._assert_all_unused_methods(response)
        self._assert_all_first_categories(response)
        self._assert_all_latter_categories(response)

        expects = [
            'index.html',
            '_base.html',
            '_add_mini.html',
            '_filter_mini.html',
            '_result_message.html'
        ]
        self._assert_templates(response.templates, expects)

    def test_get_out_of_range(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:index_month', kwargs={'year': 2000, 'month': 13}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:index'))

    def test_get_guest(self):
        response = self.client.get(reverse('moneybook:index_month', kwargs={'year': 2000, 'month': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:login'))


class IndexBalanceStatisticMiniViewTestCase(BaseTestCase):
    def test_get(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:balance_statistic_mini'), {'year': 2000, 'month': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_balance'], 46694)
        self.assertEqual(response.context['monthly_income'], 32993)
        self.assertEqual(response.context['monthly_outgo'], 7920)
        self.assertEqual(response.context['monthly_inout'], 25073)
        self.assertEqual(response.context['variable_cost'], 5390)
        self.assertEqual(response.context['living_cost'], 2500)
        self.assertEqual(response.context['variable_remain'], 25103)
        self.assertEqual(response.context['monthly_all_income'], 34123)
        self.assertEqual(response.context['monthly_all_outgo'], 9550)

        expects = [
            {'label': '銀行', 'balance': 52424},
            {'label': '現金', 'balance': -3930},
            {'label': 'PayPay', 'balance': -1800}
        ]
        iobs = response.context['methods_iob']
        for i in range(len(iobs)):
            with self.subTest(i=i):
                self.assertEqual(iobs[i].label, expects[i]['label'])
                self.assertEqual(iobs[i].balance, expects[i]['balance'])

        expects = [
            {'label': '銀行', 'income': 31723, 'outgo': 3120},
            {'label': '現金', 'income': 3000, 'outgo': 6430},
            {'label': 'PayPay', 'income': 400, 'outgo': 1000}
        ]
        iobs = response.context['methods_monthly_iob']
        for i in range(len(iobs)):
            with self.subTest(i=i):
                self.assertEqual(iobs[i].label, expects[i]['label'])
                self.assertEqual(iobs[i].income, expects[i]['income'])
                self.assertEqual(iobs[i].outgo, expects[i]['outgo'])

        expects = ['_balance_statistic_mini.html']
        self._assert_templates(response.templates, expects)

    def test_get_without_year(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:balance_statistic_mini'), {'month': 1})
        self.assertEqual(response.status_code, 400)

    def test_get_without_month(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:balance_statistic_mini'), {'year': 2000})
        self.assertEqual(response.status_code, 400)

    def test_get_out_of_range(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:balance_statistic_mini'), {'year': 2000, 'month': 13})
        self.assertEqual(response.status_code, 400)

    def test_get_without_parameters(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:balance_statistic_mini'))
        self.assertEqual(response.status_code, 400)

    def test_get_guest(self):
        response = self.client.get(reverse('moneybook:balance_statistic_mini'), {'year': 2000, 'month': 1})
        self.assertEqual(response.status_code, 403)


class IndexChartDataViewTestCase(BaseTestCase):
    def test_get(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:chart_container_data'), {'year': 2000, 'month': 1})
        self.assertEqual(response.status_code, 200)
        positive_categories_outgo = response.context['categories_outgo']
        actials = [
            {'name': 'その他', 'value': 30},
            {'name': '食費', 'value': 2500},
            {'name': '必需品', 'value': 5390}
        ]
        keys = list(positive_categories_outgo.keys())
        for i in range(len(keys)):
            with self.subTest(i=i):
                self.assertEqual(keys[i], actials[i]['name'])
                self.assertEqual(
                    positive_categories_outgo[keys[i]], actials[i]['value'])

    def test_get_wituout_year(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:chart_container_data'), {'month': 1})
        self.assertEqual(response.status_code, 400)

    def test_get_wituout_month(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:chart_container_data'), {'year': 2000})
        self.assertEqual(response.status_code, 400)

    def test_get_without_parameters(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:chart_container_data'))
        self.assertEqual(response.status_code, 400)

    def test_get_out_of_range(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:chart_container_data'), {'year': 2000, 'month': 13})
        self.assertEqual(response.status_code, 400)

    def test_get_guest(self):
        response = self.client.get(reverse('moneybook:chart_container_data'), {'year': 2000, 'month': 1})
        self.assertEqual(response.status_code, 403)


class DataTableViewTestCase(BaseTestCase):
    def test_get(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:data_table'), {'year': 2000, 'month': 1})
        self.assertEqual(response.status_code, 200)
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
        data = response.context['show_data']
        self._assert_list(data, expects)

    def test_get_without_year(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:data_table'), {'month': 1})
        self.assertEqual(response.status_code, 400)

    def test_get_without_month(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:data_table'), {'year': 2000})
        self.assertEqual(response.status_code, 400)

    def test_get_without_parameters(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:data_table'))
        self.assertEqual(response.status_code, 400)

    def test_get_out_of_range(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:data_table'), {'year': 2000, 'month': 13})
        self.assertEqual(response.status_code, 400)

    def test_get_guest(self):
        response = self.client.get(reverse('moneybook:data_table'), {'year': 2000, 'month': 1})
        self.assertEqual(response.status_code, 403)
