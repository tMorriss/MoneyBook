import json
from datetime import datetime

from django.contrib.auth.models import User
from django.urls import reverse
from moneybook.tests.commonTests import CommonTestCase


class AddViewTestCase(CommonTestCase):
    fixtures = ['data_test_case']
    username = 'tester'

    def test_get(self):
        now = datetime.now()
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:add'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['app_name'], 'test-MoneyBook')
        self.assertEqual(
            response.context['username'].username, self.username)
        self.assertEqual(response.context['year'], now.year)
        self.assertEqual(response.context['month'], now.month)
        data = response.context['directions']
        actuals = ['収入', '支出']
        self._assert_list(data, actuals)
        data = response.context['methods']
        actuals = ['銀行', "現金", "PayPay"]
        self._assert_list(data, actuals)
        data = response.context['chargeable_methods']
        actuals = ['PayPay']
        self._assert_list(data, actuals)
        data = response.context['first_categories']
        actuals = ['食費', '必需品']
        self._assert_list(data, actuals)
        data = response.context['latter_categories']
        actuals = ['その他', '内部移動', '貯金', '計算外']
        self._assert_list(data, actuals)
        data = response.context['temps']
        self.assertEqual(data, {0: "No", 1: "Yes"})

        actuals = [
            'add.html',
            '_base.html',
            '_result_message.html',
        ]
        self._assert_templates(response.templates, actuals)

    def test_get_guest(self):
        response = self.client.get(reverse('moneybook:add'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:login'))

    def test_post(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.post(
            reverse('moneybook:add'),
            {
                'date': '2000-4-1',
                'item': 'テスト項目1',
                'price': 10000,
                'direction': 2,
                'method': 2,
                'category': 1,
                'temp': False,
                'checked': False
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), '')

    def test_post_invalid(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.post(
            reverse('moneybook:add'),
            {
                'item': 'テスト項目1',
                'direction': 2,
                'method': 2,
                'category': 1,
                'temp': False,
                'checked': False
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(),
                         json.dumps({'ErrorList': ['date', 'price']}))

    def test_post_guest(self):
        response = self.client.post(
            reverse('moneybook:add'),
            {
                'date': '2000-4-1',
                'item': 'テスト項目1',
                'price': 10000,
                'direction': 2,
                'method': 2,
                'category': 1,
                'temp': False,
                'checked': False
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:login'))