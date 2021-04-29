import json
from datetime import date

from django.contrib.auth.models import User
from django.urls import reverse
from moneybook.models import Data
from moneybook.tests.common import CommonTestCase


class EditViewTestCase(CommonTestCase):
    fixtures = ['data_test_case']
    username = 'tester'

    def test_get(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:edit', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['app_name'], 'test-MoneyBook')
        self.assertEqual(response.context['username'].username, self.username)
        data = response.context['data']
        self.assertEqual(data.item, '松屋')
        self._assert_all_directions(response)
        self._assert_all_methods(response)
        self._assert_all_first_categories(response)
        self._assert_all_latter_categories(response)
        self._assert_all_temps(response)
        self._assert_all_checkeds(response)

        expects = ['edit.html', '_base.html', '_result_message.html', ]
        self._assert_templates(response.templates, expects)

    def test_get_invalid_pk(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:edit', kwargs={'pk': 10000}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:index'))

    def test_get_guest(self):
        response = self.client.get(reverse('moneybook:edit', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:login'))

    def test_post(self):
        self.client.force_login(User.objects.create_user(self.username))
        # 更新前の値を確認
        data = Data.get(1)
        self.assertEqual(data.date, date(1999, 12, 31))
        self.assertEqual(data.item, '松屋')
        self.assertEqual(data.price, 500)
        self.assertEqual(data.direction.pk, 2)
        self.assertEqual(data.method.pk, 1)
        self.assertEqual(data.category.pk, 1)
        self.assertEqual(data.temp, False)
        self.assertEqual(data.checked, True)

        response = self.client.post(
            reverse('moneybook:edit', kwargs={'pk': 1}),
            {
                'date': '2000-4-1',
                'item': 'テスト項目1',
                'price': 10000,
                'direction': 1,
                'method': 2,
                'category': 2,
                'temp': True,
                'checked': False
            }
        )
        self.assertEqual(response.status_code, 200)

        # 更新されていることを確認
        data = Data.get(1)
        self.assertEqual(data.date, date(2000, 4, 1))
        self.assertEqual(data.item, 'テスト項目1')
        self.assertEqual(data.price, 10000)
        self.assertEqual(data.direction.pk, 1)
        self.assertEqual(data.method.pk, 2)
        self.assertEqual(data.category.pk, 2)
        self.assertEqual(data.temp, True)
        self.assertEqual(data.checked, False)

    def test_post_missing_date_price(self):
        self.client.force_login(User.objects.create_user(self.username))
        # 更新前の値を確認
        data = Data.get(1)
        self.assertEqual(data.date, date(1999, 12, 31))
        self.assertEqual(data.item, '松屋')
        self.assertEqual(data.price, 500)
        self.assertEqual(data.direction.pk, 2)
        self.assertEqual(data.method.pk, 1)
        self.assertEqual(data.category.pk, 1)
        self.assertEqual(data.temp, False)
        self.assertEqual(data.checked, True)

        response = self.client.post(
            reverse('moneybook:edit', kwargs={'pk': 1}),
            {
                'item': 'テスト項目1',
                'direction': 1,
                'method': 2,
                'category': 2,
                'temp': True,
                'checked': False
            }
        )
        self.assertEqual(response.status_code, 400)
        content_json = json.loads(response.content.decode())
        self.assertEqual(content_json['ErrorList'], ['date', 'price'])

        # 更新されていないことを確認
        data = Data.get(1)
        self.assertEqual(data.date, date(1999, 12, 31))
        self.assertEqual(data.item, '松屋')
        self.assertEqual(data.price, 500)
        self.assertEqual(data.direction.pk, 2)
        self.assertEqual(data.method.pk, 1)
        self.assertEqual(data.category.pk, 1)
        self.assertEqual(data.temp, False)
        self.assertEqual(data.checked, True)

    def test_post_invalid_pk(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.post(
            reverse('moneybook:edit', kwargs={'pk': 10000}),
            {
                'date': '2000-4-1',
                'item': 'テスト項目1',
                'price': 10000,
                'direction': 1,
                'method': 2,
                'category': 2,
                'temp': True,
                'checked': False
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_post_guest(self):
        response = self.client.post(
            reverse('moneybook:edit', kwargs={'pk': 1}),
            {
                'date': '2000-4-1',
                'item': 'テスト項目1',
                'price': 10000,
                'direction': 1,
                'method': 2,
                'category': 2,
                'temp': True,
                'checked': False
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:login'))


class CheckViewTestCase(CommonTestCase):
    fixtures = ['data_test_case']
    username = 'tester'

    def test_get(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:edit_check'))
        self.assertEqual(response.status_code, 405)

    def test_post(self):
        self.client.force_login(User.objects.create_user(self.username))
        # もともとfalseであることを確認
        data = Data.get(4)
        self.assertEqual(data.checked, False)

        response = self.client.post(reverse('moneybook:edit_check'), {'id': 4})
        self.assertEqual(response.status_code, 200)

        # 更新されていることを確認
        data = Data.get(4)
        self.assertEqual(data.checked, True)

    def test_post_missing_id(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.post(reverse('moneybook:edit_check'))
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_id(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.post(reverse('moneybook:edit_check'), {'id': 10000})
        self.assertEqual(response.status_code, 400)

    def test_post_guest(self):
        response = self.client.post(reverse('moneybook:edit_check'), {'id': 3})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:login'))
