from datetime import date, datetime
from unittest.mock import patch

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse
from moneybook.tests.base import BaseTestCase
from moneybook.views import StatisticsMonthView


class StatisticsViewTestCase(BaseTestCase):
    @patch.object(StatisticsMonthView, 'get', return_value=HttpResponse())
    def test_get(self, statistics_month):
        now = datetime.now()
        self.client.force_login(User.objects.create_user(self.username))
        self.client.get(reverse('moneybook:statistics'))
        kwargs = StatisticsMonthView.get.call_args.kwargs
        self.assertEqual(kwargs['year'], now.year)

    def test_get_guest(self):
        response = self.client.get(reverse('moneybook:statistics'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:login'))


class StatisticsMonthViewTestCase(BaseTestCase):
    def test_get(self):
        self.client.force_login(User.objects.create_user(self.username))
        # January
        self._create_data(date=date(2000, 1, 1), item='給与', price=25123, direction_id=1, category_id=3)
        self._create_data(date=date(2000, 1, 5), item='食費1', price=2500, direction_id=2, category_id=1)
        self._create_data(date=date(2000, 1, 28), item='電気代', price=630, direction_id=2, category_id=2)
        self._create_data(date=date(2000, 1, 28), item='ガス代', price=260, direction_id=2, category_id=2)
        self._create_data(date=date(2000, 1, 28), item='水道代', price=600, direction_id=2, category_id=2)

        # February
        self._create_data(date=date(2000, 2, 1), item='給与', price=24321, direction_id=1, category_id=3)
        self._create_data(date=date(2000, 2, 28), item='水道代', price=500, direction_id=2, category_id=2)

        # March
        self._create_data(date=date(2000, 3, 1), item='Outgo', price=500, direction_id=2, category_id=2)
        self._create_data(date=date(2000, 3, 28), item='水道代', price=500, direction_id=2, category_id=2)

        response = self.client.get(
            reverse('moneybook:statistics_month', kwargs={'year': 2000}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['app_name'], 'test-MoneyBook')
        self.assertEqual(response.context['username'].username, self.username)
        self.assertEqual(response.context['year'], 2000)

        monthly_context = response.context['monthly_context']
        self.assertEqual(len(monthly_context), 12)

        january = monthly_context[0]
        self.assertEqual(january['label'], 1)
        self.assertEqual(january['income'], 25123)
        self.assertEqual(january['outgo'], 3990)
        self.assertEqual(january['balance'], 25123 - 3990)
        self.assertEqual(january['salary'], 25123)
        self.assertEqual(january['living_cost'], 2500)
        self.assertEqual(january['electricity_cost'], 630)
        self.assertEqual(january['gus_cost'], 260)
        self.assertEqual(january['water_cost'], 300)
        self.assertEqual(january['infra_cost'], 1190)
        self.assertEqual(january['food_cost'], 2500)
        self.assertEqual(january['all_income'], 25123)
        self.assertEqual(january['all_outgo'], 3990)
        self.assertEqual(january['all_balance'], 25123 - 3990)
        self.assertEqual(january['period_balance'], 21133)

        february = monthly_context[1]
        self.assertEqual(february['label'], 2)
        self.assertEqual(february['income'], 24321)
        self.assertEqual(february['outgo'], 500)
        self.assertEqual(february['balance'], 24321 - 500)
        self.assertEqual(february['salary'], 24321)
        self.assertEqual(february['living_cost'], 0)
        self.assertEqual(february['electricity_cost'], 0)
        self.assertEqual(february['gus_cost'], 0)
        self.assertEqual(february['water_cost'], 250)
        self.assertEqual(february['infra_cost'], 250)
        self.assertEqual(february['food_cost'], 0)
        self.assertEqual(february['all_income'], 24321)
        self.assertEqual(february['all_outgo'], 500)
        self.assertEqual(february['all_balance'], 24321 - 500)
        self.assertEqual(february['period_balance'], 21133 + (24321 - 500))

        march = monthly_context[2]
        self.assertEqual(march['label'], 3)
        self.assertEqual(march['income'], 0)
        self.assertEqual(march['outgo'], 1000)
        self.assertEqual(march['balance'], -1000)
        self.assertEqual(march['salary'], 0)
        self.assertEqual(march['living_cost'], 0)
        self.assertEqual(march['electricity_cost'], 0)
        self.assertEqual(march['gus_cost'], 0)
        self.assertEqual(march['water_cost'], 250)
        self.assertEqual(march['infra_cost'], 250)
        self.assertEqual(march['food_cost'], 0)
        self.assertEqual(march['all_income'], 0)
        self.assertEqual(march['all_outgo'], 1000)
        self.assertEqual(march['all_balance'], -1000)
        expected_march_period_balance = 21133 + (24321 - 500) - 1000
        self.assertEqual(march['period_balance'], expected_march_period_balance)

        zero_list = list(range(3, 12))
        for i in zero_list:
            with self.subTest(i=i):
                m = monthly_context[i]
                self.assertEqual(m['label'], i + 1)
                self.assertEqual(m['income'], 0)
                self.assertEqual(m['outgo'], 0)
                self.assertEqual(m['balance'], 0)
                self.assertEqual(m['salary'], 0)
                self.assertEqual(m['living_cost'], 0)
                self.assertEqual(m['electricity_cost'], 0)
                self.assertEqual(m['gus_cost'], 0)
                self.assertEqual(m['water_cost'], 0)
                self.assertEqual(m['infra_cost'], 0)
                self.assertEqual(m['food_cost'], 0)
                self.assertEqual(m['all_income'], 0)
                self.assertEqual(m['all_outgo'], 0)
                self.assertEqual(m['all_balance'], 0)
                self.assertEqual(m['period_balance'], expected_march_period_balance)

        expects = [
            'statistics.html',
            '_base.html',
            '_statistics_task_bar.html'
        ]
        self._assert_templates(response.templates, expects)

    def test_get_december_water(self):
        self.client.force_login(User.objects.create_user(self.username))
        self._create_data(date=date(1999, 12, 28), item='水道代', price=600, direction_id=2, category_id=2)
        # StatisticsMonthView checks next month if water is 0, so we create it for 1999-12
        response = self.client.get(reverse('moneybook:statistics_month', kwargs={'year': 1999}))
        self.assertEqual(response.status_code, 200)

        monthly_context = response.context['monthly_context']
        self.assertEqual(len(monthly_context), 12)
        self.assertEqual(monthly_context[11]['water_cost'], 300)

    def test_get_guest(self):
        response = self.client.get(reverse('moneybook:statistics_month', kwargs={'year': 2000}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:login'))
