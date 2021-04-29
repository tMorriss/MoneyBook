from datetime import datetime
from unittest.mock import patch

from django.contrib.auth.models import User
from django.urls import reverse
from moneybook.tests.common import CommonTestCase
from moneybook.views import AllInoutMonthView


class AllInoutViewTestCase(CommonTestCase):
    fixtures = ['data_test_case']
    username = 'tester'

    @patch.object(AllInoutMonthView, 'get', return_value=True)
    def test_get(self, statistics_month):
        now = datetime.now()
        self.client.get(reverse('moneybook:all_inout'))
        kwargs = AllInoutMonthView.get.call_args.kwargs
        self.assertEqual(kwargs['year'], now.year)

    def test_get_guest(self):
        response = self.client.get(reverse('moneybook:statistics'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:login'))


class AllInoutMonthViewTestCase(CommonTestCase):
    fixtures = ['data_test_case']
    username = 'tester'

    def test_get(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:all_inout_month', kwargs={'year': 2000}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['app_name'], 'test-MoneyBook')
        self.assertEqual(response.context['username'].username, self.username)
        self.assertEqual(response.context['year'], 2000)

        month_all_io_list = response.context['month_all_io_list']
        self.assertEqual(len(month_all_io_list), 12)
        january = month_all_io_list[0]
        self.assertEqual(january.label, 1)
        self.assertEqual(january.income, 33123)
        self.assertEqual(january.outgo, 8550)
        self.assertEqual(january.balance, 33123 - 8550)
        february = month_all_io_list[1]
        self.assertEqual(february.label, 2)
        self.assertEqual(february.income, 24321)
        self.assertEqual(february.outgo, 400)
        self.assertEqual(february.balance, 24321 - 400)
        march = month_all_io_list[2]
        self.assertEqual(march.label, 3)
        self.assertEqual(march.income, 0)
        self.assertEqual(march.outgo, 500)
        self.assertEqual(march.balance, -500)
        zero_list = list(range(3, 12))
        for i in zero_list:
            with self.subTest(i=i):
                m = month_all_io_list[i]
                self.assertEqual(m.label, i + 1)
                self.assertEqual(m.income, 0)
                self.assertEqual(m.outgo, 0)
                self.assertEqual(m.balance, 0)

        # 途中残高
        period_balances = response.context['period_balances']
        self.assertEqual(period_balances[0].label, 1)
        self.assertEqual(period_balances[0].value, 24073)
        self.assertEqual(period_balances[1].label, 2)
        self.assertEqual(period_balances[1].value, 47994)
        self.assertEqual(period_balances[2].label, 3)
        self.assertEqual(period_balances[2].value, 47094)
        zero_list = list(range(3, 12))
        for i in zero_list:
            with self.subTest(i=i):
                m = period_balances[i]
                self.assertEqual(m.label, i + 1)
                self.assertEqual(m.value, 46694)

        expects = ['all_inout.html', '_base.html', '_statistics_task_bar.html']
        self._assert_templates(response.templates, expects)
