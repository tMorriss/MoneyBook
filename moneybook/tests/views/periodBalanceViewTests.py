from datetime import datetime

from django.contrib.auth.models import User
from django.urls import reverse
from moneybook.tests.base import BaseTestCase


class PeriodBalanceViewTestCase(BaseTestCase):
    def _assert_without_draw(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertFalse('period_balances' in response.context)
        self.assertFalse(response.context['draw_graph'])
        self.assertFalse('start_year' in response.context)
        self.assertFalse('start_month' in response.context)
        self.assertFalse('end_year' in response.context)
        self.assertFalse('end_month' in response.context)

        expects = [
            'period_balances.html',
            '_base.html',
            '_statistics_task_bar.html'
        ]
        self._assert_templates(response.templates, expects)

    def _assert_now(self, response):
        now = datetime.now()
        self.assertEqual(response.status_code, 200)
        period_balances = response.context['period_balances']
        expects = []
        for i in range(12):
            expects.append({'label': str(now.year - 1) + '-' + str(i + 1).zfill(2), 'value': 46694})
        for i in range(now.month):
            expects.append({'label': str(now.year) + '-' + str(i + 1).zfill(2), 'value': 46694})
        self.assertEqual(len(period_balances), len(expects))
        for i in range(len(expects)):
            self.assertEqual(period_balances[i].label, expects[i]['label'])
            self.assertEqual(period_balances[i].value, expects[i]['value'])
        self.assertTrue(response.context['draw_graph'])
        self.assertEqual(response.context['start_year'], now.year - 1)
        self.assertEqual(response.context['start_month'], 1)
        self.assertEqual(response.context['end_year'], now.year)
        self.assertEqual(response.context['end_month'], now.month)

        expects = [
            'period_balances.html',
            '_base.html',
            '_statistics_task_bar.html'
        ]
        self._assert_templates(response.templates, expects)

    def test_get(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:period_balances'),
            {
                'start_year': 2000, 'start_month': 1,
                'end_year': 2000, 'end_month': 5
            }
        )
        self.assertEqual(response.status_code, 200)
        period_balances = response.context['period_balances']
        expects = [
            {'label': '2000-01', 'value': 24073},
            {'label': '2000-02', 'value': 47994},
            {'label': '2000-03', 'value': 47094},
            {'label': '2000-04', 'value': 46694},
            {'label': '2000-05', 'value': 46694},
        ]
        self.assertEqual(len(period_balances), len(expects))
        for i in range(len(expects)):
            self.assertEqual(period_balances[i].label, expects[i]['label'])
            self.assertEqual(period_balances[i].value, expects[i]['value'])
        self.assertTrue(response.context['draw_graph'])
        self.assertEqual(response.context['start_year'], 2000)
        self.assertEqual(response.context['start_month'], 1)
        self.assertEqual(response.context['end_year'], 2000)
        self.assertEqual(response.context['end_month'], 5)

        expects = [
            'period_balances.html',
            '_base.html',
            '_statistics_task_bar.html'
        ]
        self._assert_templates(response.templates, expects)

    def test_get_start_zero(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:period_balances'),
            {
                'start_year': 1999, 'start_month': 10,
                'end_year': 2000, 'end_month': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        period_balances = response.context['period_balances']
        expects = [
            {'label': '1999-10', 'value': 0},
            {'label': '1999-11', 'value': 0},
            {'label': '1999-12', 'value': -500},
            {'label': '2000-01', 'value': 24073},
        ]
        self.assertEqual(len(period_balances), len(expects))
        for i in range(len(expects)):
            self.assertEqual(period_balances[i].label, expects[i]['label'])
            self.assertEqual(period_balances[i].value, expects[i]['value'])
        self.assertTrue(response.context['draw_graph'])
        self.assertEqual(response.context['start_year'], 1999)
        self.assertEqual(response.context['start_month'], 10)
        self.assertEqual(response.context['end_year'], 2000)
        self.assertEqual(response.context['end_month'], 1)

        expects = [
            'period_balances.html',
            '_base.html',
            '_statistics_task_bar.html'
        ]
        self._assert_templates(response.templates, expects)

    def test_get_without_draw(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:period_balances'))
        self._assert_now(response)

    def test_get_missing_param(self):
        self.client.force_login(User.objects.create_user(self.username))
        body = [
            {'start_month': 1, 'end_year': 2000, 'end_month': 5},
            {'start_year': 2000, 'end_year': 2000, 'end_month': 5},
            {'start_year': 2000, 'start_month': 1, 'end_month': 5},
            {'start_year': 2000, 'start_month': 1, 'end_year': 2000}
        ]
        for b in body:
            with self.subTest(b=b):
                response = self.client.get(reverse('moneybook:period_balances'), b)
                self._assert_now(response)

    def test_get_str_param(self):
        self.client.force_login(User.objects.create_user(self.username))
        body = [
            {
                'start_year': 'a', 'start_month': 1,
                'end_year': 2000, 'end_month': 5
            }, {
                'start_year': 2000, 'start_month': 'a',
                'end_year': 2000, 'end_month': 5
            }, {
                'start_year': 2000, 'start_month': 1,
                'end_year': 'a', 'end_month': 5
            }, {
                'start_year': 2000, 'start_month': 1,
                'end_year': 2000, 'end_month': 'a'
            }
        ]
        for b in body:
            with self.subTest(b=b):
                response = self.client.get(reverse('moneybook:period_balances'), b)
                self._assert_without_draw(response)
