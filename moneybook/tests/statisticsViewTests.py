from datetime import datetime
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
        self.assertEqual(january['income'], 32993)
        self.assertEqual(january['outgo'], 7920)
        self.assertEqual(january['balance'], 32993 - 7920)
        self.assertEqual(january['salary'], 25123)
        self.assertEqual(january['living_cost'], 2500)
        self.assertEqual(january['electricity_cost'], 630)
        self.assertEqual(january['gus_cost'], 260)
        self.assertEqual(january['water_cost'], 300)
        self.assertEqual(january['infra_cost'], 1190)
        self.assertEqual(january['food_cost'], 2500)
        self.assertEqual(january['all_income'], 33123)
        self.assertEqual(january['all_outgo'], 8550)
        self.assertEqual(january['all_balance'], 33123 - 8550)
        self.assertEqual(january['period_balance'], 24073)
        february = monthly_context[1]
        self.assertEqual(february['label'], 2)
        self.assertEqual(february['income'], 24321)
        self.assertEqual(february['outgo'], 400)
        self.assertEqual(february['balance'], 24321 - 400)
        self.assertEqual(february['salary'], 24321)
        self.assertEqual(february['living_cost'], 0)
        self.assertEqual(february['electricity_cost'], 0)
        self.assertEqual(february['gus_cost'], 0)
        self.assertEqual(february['water_cost'], 250)
        self.assertEqual(february['infra_cost'], 250)
        self.assertEqual(february['food_cost'], 0)
        self.assertEqual(february['all_income'], 24321)
        self.assertEqual(february['all_outgo'], 400)
        self.assertEqual(february['all_balance'], 24321 - 400)
        self.assertEqual(february['period_balance'], 47994)
        march = monthly_context[2]
        self.assertEqual(march['label'], 3)
        self.assertEqual(march['income'], 0)
        self.assertEqual(march['outgo'], 500)
        self.assertEqual(march['balance'], -500)
        self.assertEqual(march['salary'], 0)
        self.assertEqual(march['living_cost'], 0)
        self.assertEqual(march['electricity_cost'], 0)
        self.assertEqual(march['gus_cost'], 0)
        self.assertEqual(march['water_cost'], 250)
        self.assertEqual(march['infra_cost'], 250)
        self.assertEqual(march['food_cost'], 0)
        self.assertEqual(march['all_income'], 0)
        self.assertEqual(march['all_outgo'], 500)
        self.assertEqual(march['all_balance'], -500)
        self.assertEqual(march['period_balance'], 47094)
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
                self.assertEqual(m['period_balance'], 46694)

        expects = [
            'statistics.html',
            '_base.html',
            '_statistics_task_bar.html'
        ]
        self._assert_templates(response.templates, expects)

    def test_get_december_water(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:statistics_month', kwargs={'year': 1999}))
        self.assertEqual(response.status_code, 200)

        monthly_context = response.context['monthly_context']
        self.assertEqual(len(monthly_context), 12)
        self.assertEqual(monthly_context[11]['water_cost'], 300)

    def test_get_guest(self):
        response = self.client.get(reverse('moneybook:statistics_month', kwargs={'year': 2000}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:login'))
