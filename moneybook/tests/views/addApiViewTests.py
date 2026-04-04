import json
from datetime import date

from django.contrib.auth.models import User
from django.urls import reverse
from moneybook.models import Category, Data, Direction, Method, PeriodicData
from moneybook.tests.base import BaseTestCase


class AddApiViewTestCase(BaseTestCase):
    def test_post(self):
        self.client.force_login(User.objects.create_user(self.username))
        before_count = Data.get_all_data().count()
        response = self.client.post(
            reverse('moneybook:add_api'),
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
        after_count = Data.get_all_data().count()
        self.assertEqual(after_count, before_count + 1)

    def test_post_invalid(self):
        self.client.force_login(User.objects.create_user(self.username))
        before_count = Data.get_all_data().count()
        response = self.client.post(
            reverse('moneybook:add_api'),
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
        self.assertEqual(response.content.decode(), json.dumps(
            {'ErrorList': ['date', 'price']}))
        after_count = Data.get_all_data().count()
        self.assertEqual(after_count, before_count)

    def test_post_guest(self):
        before_count = Data.get_all_data().count()
        response = self.client.post(
            reverse('moneybook:add_api'),
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
        self.assertEqual(response.status_code, 403)
        after_count = Data.get_all_data().count()
        self.assertEqual(after_count, before_count)


class SuggestApiViewTestCase(BaseTestCase):
    def test_get(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:suggest_api'), {'item': '必需品'})

        self.assertEqual(response.status_code, 200, response.content)
        body = json.loads(response.content.decode())

        expects = {'suggests': [
            {'date': '2000-02-01', 'item': '必需品3', 'price': 400},
            {'date': '2000-01-08', 'item': '必需品2', 'price': 3500},
            {'date': '2000-01-05', 'item': '必需品1', 'price': 1000}
        ]}
        self.assertEqual(body, expects)

    def test_get_distinct(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:suggest_api'), {'item': 'PayPayチャージ'})

        self.assertEqual(response.status_code, 200, response.content)
        body = json.loads(response.content.decode())

        expects = {'suggests': [
            {'date': '2000-01-25', 'item': 'PayPayチャージ', 'price': 1000},
            {'date': '2000-01-25', 'item': 'PayPayチャージ', 'price': 1000}
        ]}
        self.assertEqual(body, expects)

    def test_get_missing_item(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:suggest_api'))

        self.assertEqual(response.status_code, 400, response.content)
        body = json.loads(response.content.decode())
        self.assertEqual(body, {'message': 'missing item'})

    def test_get_empty_item(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:suggest_api'), {'item': ''})

        self.assertEqual(response.status_code, 400, response.content)
        body = json.loads(response.content.decode())
        self.assertEqual(body, {'message': 'empty item'})


class AddPeriodicApiViewTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(self.username)
        self.client.force_login(self.user)

        # テスト用のPeriodicDataを作成
        PeriodicData.objects.all().delete()
        PeriodicData.objects.create(
            day=1,
            item='家賃',
            price=50000,
            direction=Direction.get(2),
            method=Method.get(1),
            category=Category.get(1),
            temp=False
        )
        PeriodicData.objects.create(
            day=15,
            item='お小遣い',
            price=10000,
            direction=Direction.get(1),
            method=Method.get(2),
            category=Category.get(5),
            temp=True
        )

    def test_add_periodic(self):
        """定期取引データが一括で追加されること"""
        year = 2024
        month = 4

        # 実行前のデータ数
        initial_count = Data.objects.count()

        response = self.client.post(reverse('moneybook:add_periodic_api'), {
            'year': year,
            'month': month
        })

        self.assertEqual(response.status_code, 200)

        # データが2件追加されていること
        self.assertEqual(Data.objects.count(), initial_count + 2)

        # 追加されたデータの内容確認（全パラメータ）
        data1 = Data.objects.get(item='家賃', date=date(2024, 4, 1))
        self.assertEqual(data1.price, 50000)
        self.assertEqual(data1.direction.pk, 2)
        self.assertEqual(data1.method.pk, 1)
        self.assertEqual(data1.category.pk, 1)
        self.assertEqual(data1.temp, False)
        self.assertEqual(data1.checked, False)
        self.assertEqual(data1.pre_checked, False)

        data2 = Data.objects.get(item='お小遣い', date=date(2024, 4, 15))
        self.assertEqual(data2.price, 10000)
        self.assertEqual(data2.direction.pk, 1)
        self.assertEqual(data2.method.pk, 2)
        self.assertEqual(data2.category.pk, 5)
        self.assertEqual(data2.temp, True)
        self.assertEqual(data2.checked, False)
        self.assertEqual(data2.pre_checked, False)

    def test_add_periodic_day_clamping(self):
        """月の日数を超える日付が最終日に調整されること"""
        PeriodicData.objects.create(
            day=31,
            item='月末払い',
            price=1000,
            direction=Direction.get(2),
            method=Method.get(1),
            category=Category.get(1),
            temp=False
        )

        year = 2024
        month = 2  # 2024年2月は29日まで

        response = self.client.post(reverse('moneybook:add_periodic_api'), {
            'year': year,
            'month': month
        })
        self.assertEqual(response.status_code, 200)

        # 31日が29日に調整されていること
        data = Data.objects.get(item='月末払い', date=date(2024, 2, 29))
        self.assertEqual(data.price, 1000)

    def test_add_periodic_invalid_date(self):
        """不正な年月でエラーになること"""
        response = self.client.post(reverse('moneybook:add_periodic_api'), {
            'year': 'invalid',
            'month': 2
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.post(reverse('moneybook:add_periodic_api'), {
            'year': 2024,
            'month': 'invalid'
        })
        self.assertEqual(response.status_code, 400)

        # 13月などの範囲外
        response = self.client.post(reverse('moneybook:add_periodic_api'), {
            'year': 2024,
            'month': 13
        })
        self.assertEqual(response.status_code, 400)

    def test_add_periodic_missing_params(self):
        """パラメータ不足でエラーになること"""
        response = self.client.post(reverse('moneybook:add_periodic_api'), {
            'year': 2024
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.post(reverse('moneybook:add_periodic_api'), {
            'month': 2
        })
        self.assertEqual(response.status_code, 400)
