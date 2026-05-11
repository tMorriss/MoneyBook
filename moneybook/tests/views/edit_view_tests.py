import json
from datetime import date

from django.contrib.auth.models import User
from django.urls import reverse
from moneybook.models import Data
from moneybook.tests.base import BaseTestCase


class EditViewTestCase(BaseTestCase):
    def test_get(self):
        self.client.force_login(User.objects.create_user(self.username))
        self._create_data(pk=1, item='松屋')

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


class EditApiViewTestCase(BaseTestCase):
    def test_post(self):
        self.client.force_login(User.objects.create_user(self.username))
        # 更新前の値を確認
        self._create_data(
            pk=1, date='1999-12-31', item='松屋', price=500, direction_id=2,
            method_id=1, category_id=1, temp=False, checked=True)
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
            reverse('moneybook:edit_api', kwargs={'pk': 1}),
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
        self._create_data(
            pk=1, date='1999-12-31', item='松屋', price=500, direction_id=2,
            method_id=1, category_id=1, temp=False, checked=True)
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
            reverse('moneybook:edit_api', kwargs={'pk': 1}),
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
            reverse('moneybook:edit_api', kwargs={'pk': 10000}),
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
        self.assertEqual(response.status_code, 404)

    def test_post_guest(self):
        # 更新前の値を確認
        self._create_data(
            pk=1, date='1999-12-31', item='松屋', price=500, direction_id=2,
            method_id=1, category_id=1, temp=False, checked=True)
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
            reverse('moneybook:edit_api', kwargs={'pk': 1}),
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
        self.assertEqual(response.status_code, 403)

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


class ApplyCheckApiViewTestCase(BaseTestCase):
    def test_post(self):
        self.client.force_login(User.objects.create_user(self.username))
        # まず事前チェック済みデータを作成
        d1 = self._create_data(pk=4, item='必需品1', checked=False, pre_checked=True)
        d2 = self._create_data(pk=8, item='スーパー', checked=False, pre_checked=True)
        test_pks = [d1.pk, d2.pk]

        # 事前チェック済みデータを確認
        all_data = Data.get_all_data()
        unchecked_data = Data.get_unchecked_data(all_data)
        pre_checked_data = Data.get_pre_checked_data(unchecked_data)
        self.assertEqual(len(pre_checked_data), 2)

        # ApplyCheckApiViewを実行
        response = self.client.post(reverse('moneybook:apply_check_api'))
        self.assertEqual(response.status_code, 200)

        # 事前チェック済みデータがチェック済みになっていることを確認
        for pk in test_pks:
            data = Data.get(pk)
            self.assertEqual(data.pre_checked, False)
            self.assertEqual(data.checked, True)

    def test_post_guest(self):
        response = self.client.post(reverse('moneybook:apply_check_api'))
        # apply_check_api is in the API list, so it should return 403
        self.assertEqual(response.status_code, 403)


class PreCheckApiViewTestCase(BaseTestCase):
    def test_post_set_true(self):
        self.client.force_login(User.objects.create_user(self.username))
        # pk=4 (必需品1) is unchecked
        self._create_data(pk=4, item='必需品1', checked=False, pre_checked=False)
        data = Data.get(4)
        self.assertEqual(data.pre_checked, False)

        response = self.client.post(
            reverse('moneybook:pre_check_api'),
            {'id': 4, 'status': '1'}
        )
        self.assertEqual(response.status_code, 200)

        data = Data.get(4)
        self.assertEqual(data.pre_checked, True)

    def test_post_set_false(self):
        self.client.force_login(User.objects.create_user(self.username))
        # まず事前チェック済みにする
        self._create_data(pk=4, item='必需品1', checked=False, pre_checked=True)

        response = self.client.post(
            reverse('moneybook:pre_check_api'),
            {'id': 4, 'status': '0'}
        )
        self.assertEqual(response.status_code, 200)

        data = Data.get(4)
        self.assertEqual(data.pre_checked, False)

    def test_post_invalid_id(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.post(
            reverse('moneybook:pre_check_api'),
            {'id': 99999, 'status': '1'}
        )
        self.assertEqual(response.status_code, 404)

    def test_post_guest(self):
        self._create_data(pk=4, item='必需品1', checked=False, pre_checked=False)
        response = self.client.post(
            reverse('moneybook:pre_check_api'),
            {'id': 4, 'status': '1'}
        )
        # pre_check_api is in the API list, so it should return 403
        self.assertEqual(response.status_code, 403)
