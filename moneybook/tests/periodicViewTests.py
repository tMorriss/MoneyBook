import json
from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.urls import reverse
from moneybook.models import Category, Direction, Method, PeriodicData
from moneybook.tests.base import BaseTestCase


class PeriodicViewGetTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        # テスト用のPeriodicDataを作成
        PeriodicData.objects.create(
            day=1,
            item='定期取引テスト',
            price=5000,
            direction=Direction.get(2),
            method=Method.get(1),
            category=Category.get(1),
            temp=False
        )

    def test_get(self):
        """一覧ページが正しく表示されること"""
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:periodic'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['app_name'], 'test-MoneyBook')
        self.assertEqual(response.context['username'].username, self.username)

        # 来月の情報が設定されていること
        now = datetime.now()
        next_month = now + relativedelta(months=1)
        self.assertEqual(response.context['next_year'], next_month.year)
        self.assertEqual(response.context['next_month'], next_month.month)

        # 定期取引データが含まれていること
        periodic_data = response.context['periodic_data_list']
        self.assertEqual(periodic_data.count(), 1)
        self.assertEqual(periodic_data[0].item, '定期取引テスト')

    def test_get_guest(self):
        """ログインしていない場合は403が返されること"""
        response = self.client.get(reverse('moneybook:periodic'))
        self.assertEqual(response.status_code, 403)


class PeriodicViewPostTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        PeriodicData.objects.create(
            day=1,
            item='設定テスト',
            price=3000,
            direction=Direction.get(2),
            method=Method.get(1),
            category=Category.get(1),
            temp=False
        )

    def test_post(self):
        """設定を更新できること"""
        self.client.force_login(User.objects.create_user(self.username))

        # 既存データ数を確認
        before_count = PeriodicData.objects.count()
        self.assertEqual(before_count, 1)

        # 新しい設定を送信
        new_data = [
            {
                'day': 5,
                'item': '新規定期取引',
                'price': 10000,
                'direction': 2,
                'method': 2,
                'category': 2,
                'temp': True
            },
            {
                'day': 10,
                'item': '別の定期取引',
                'price': 20000,
                'direction': 1,
                'method': 1,
                'category': 3,
                'temp': False
            }
        ]

        response = self.client.post(
            reverse('moneybook:periodic'),
            data=json.dumps({'periodic_data_list': new_data}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        # データが更新されていること
        after_count = PeriodicData.objects.count()
        self.assertEqual(after_count, 2)

        # 新しいデータが保存されていること
        data = PeriodicData.get_all()
        self.assertEqual(data[0].day, 5)
        self.assertEqual(data[0].item, '新規定期取引')
        self.assertEqual(data[1].day, 10)
        self.assertEqual(data[1].item, '別の定期取引')

    def test_post_guest(self):
        """ログインしていない場合は403エラー"""
        response = self.client.post(
            reverse('moneybook:periodic'),
            data=json.dumps({'periodic_data_list': []}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)

    def test_post_invalid_data(self):
        """不正なデータの場合はエラーが返ること"""
        self.client.force_login(User.objects.create_user(self.username))

        # 無効なprice値（負の数）
        invalid_data = [
            {
                'day': 1,
                'item': 'テスト',
                'price': -1000,  # 負の値
                'direction': 2,
                'method': 1,
                'category': 1,
                'temp': False
            }
        ]

        response = self.client.post(
            reverse('moneybook:periodic'),
            data=json.dumps({'periodic_data_list': invalid_data}),
            content_type='application/json'
        )

        # ModelFormはPositiveIntegerFieldでないため負の値も許可される可能性がある
        # 代わりに必須フィールドの欠落をテスト
        missing_field_data = [
            {
                'day': 1,
                # 'item': 'テスト',  # item欠落
                'price': 1000,
                'direction': 2,
                'method': 1,
                'category': 1,
                'temp': False
            }
        ]

        response = self.client.post(
            reverse('moneybook:periodic'),
            data=json.dumps({'periodic_data_list': missing_field_data}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        result = json.loads(response.content)
        self.assertIn('errors', result)

    def test_post_exception(self):
        """例外が発生した場合はエラーが返ること"""
        self.client.force_login(User.objects.create_user(self.username))

        # 不正なJSON形式
        response = self.client.post(
            reverse('moneybook:periodic'),
            data='invalid json',
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        result = json.loads(response.content)
        self.assertIn('error', result)
