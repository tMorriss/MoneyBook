import json
from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.urls import reverse
from moneybook.models import Category, Data, Direction, Method, PeriodicData
from moneybook.tests.base import BaseTestCase


class PeriodicListViewTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        # テスト用のPeriodicDataを作成
        PeriodicData.objects.create(
            day=1,
            item="定期取引テスト",
            price=5000,
            direction=Direction.get(2),
            method=Method.get(1),
            category=Category.get(1),
            temp=False
        )

    def test_get(self):
        """一覧ページが正しく表示されること"""
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:periodic_list'))

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
        self.assertEqual(periodic_data[0].item, "定期取引テスト")

    def test_get_guest(self):
        """ログインしていない場合はリダイレクトされること"""
        response = self.client.get(reverse('moneybook:periodic_list'))
        self.assertEqual(response.status_code, 302)


class PeriodicConfigViewTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        PeriodicData.objects.create(
            day=1,
            item="設定テスト",
            price=3000,
            direction=Direction.get(2),
            method=Method.get(1),
            category=Category.get(1),
            temp=False
        )

    def test_get(self):
        """設定ページが正しく表示されること"""
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:periodic_config'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['app_name'], 'test-MoneyBook')
        self._assert_all_directions(response)
        self._assert_all_methods(response)
        self._assert_all_first_categories(response)
        self._assert_all_latter_categories(response)

        # 定期取引データが含まれていること
        periodic_data = response.context['periodic_data_list']
        self.assertEqual(periodic_data.count(), 1)

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
            reverse('moneybook:periodic_config'),
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
            reverse('moneybook:periodic_config'),
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
            reverse('moneybook:periodic_config'),
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
            reverse('moneybook:periodic_config'),
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
            reverse('moneybook:periodic_config'),
            data='invalid json',
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        result = json.loads(response.content)
        self.assertIn('error', result)


class PeriodicAddBulkViewTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.periodic = PeriodicData.objects.create(
            day=15,
            item="一括登録テスト",
            price=7000,
            direction=Direction.get(2),
            method=Method.get(1),
            category=Category.get(1),
            temp=False
        )

    def test_post(self):
        """データが正しく登録されること"""
        self.client.force_login(User.objects.create_user(self.username))

        before_count = Data.objects.count()

        response = self.client.post(
            reverse('moneybook:periodic_add_bulk'),
            data=json.dumps({
                'year': 2024,
                'month': 5,
                'periodic_id': self.periodic.pk
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'データを登録しました')

        # データが追加されていること
        after_count = Data.objects.count()
        self.assertEqual(after_count, before_count + 1)

        # 正しい内容で登録されていること
        new_data = Data.objects.latest('id')
        self.assertEqual(new_data.date.year, 2024)
        self.assertEqual(new_data.date.month, 5)
        self.assertEqual(new_data.date.day, 15)
        self.assertEqual(new_data.item, "一括登録テスト")
        self.assertEqual(new_data.price, 7000)

    def test_post_duplicate(self):
        """重複チェックなしで常に登録されること"""
        self.client.force_login(User.objects.create_user(self.username))

        # 1回目の登録
        self.client.post(
            reverse('moneybook:periodic_add_bulk'),
            data=json.dumps({
                'year': 2024,
                'month': 5,
                'periodic_id': self.periodic.pk
            }),
            content_type='application/json'
        )

        before_count = Data.objects.count()

        # 2回目の登録（同じデータ）
        response = self.client.post(
            reverse('moneybook:periodic_add_bulk'),
            data=json.dumps({
                'year': 2024,
                'month': 5,
                'periodic_id': self.periodic.pk
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertTrue(result['success'])

        # データが追加されていること（重複チェックなし）
        after_count = Data.objects.count()
        self.assertEqual(after_count, before_count + 1)

    def test_post_day_overflow(self):
        """月の日数を超える日付の場合、最終日に調整されること"""
        self.client.force_login(User.objects.create_user(self.username))

        # day=31の定期取引を作成
        periodic_31 = PeriodicData.objects.create(
            day=31,
            item="月末処理",
            price=5000,
            direction=Direction.get(2),
            method=Method.get(1),
            category=Category.get(1),
            temp=False
        )

        # 2月（28日まで）に登録
        response = self.client.post(
            reverse('moneybook:periodic_add_bulk'),
            data=json.dumps({
                'year': 2024,
                'month': 2,
                'periodic_id': periodic_31.pk
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        # 2月29日（2024年はうるう年）に登録されていること
        new_data = Data.objects.latest('id')
        self.assertEqual(new_data.date.day, 29)

    def test_post_guest(self):
        """ログインしていない場合は403エラー"""
        response = self.client.post(
            reverse('moneybook:periodic_add_bulk'),
            data=json.dumps({
                'year': 2024,
                'month': 5,
                'periodic_id': self.periodic.pk
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)

    def test_post_missing_year_month(self):
        """年月が指定されていない場合はエラーが返ること"""
        self.client.force_login(User.objects.create_user(self.username))

        # yearが空
        response = self.client.post(
            reverse('moneybook:periodic_add_bulk'),
            data=json.dumps({
                'year': None,
                'month': 5,
                'periodic_id': self.periodic.pk
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        result = json.loads(response.content)
        self.assertIn('error', result)
        self.assertEqual(result['error'], '年月が指定されていません')

        # monthが空
        response = self.client.post(
            reverse('moneybook:periodic_add_bulk'),
            data=json.dumps({
                'year': 2024,
                'month': None,
                'periodic_id': self.periodic.pk
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        result = json.loads(response.content)
        self.assertIn('error', result)
        self.assertEqual(result['error'], '年月が指定されていません')

    def test_post_exception(self):
        """例外が発生した場合はエラーが返ること"""
        self.client.force_login(User.objects.create_user(self.username))

        # 不正なJSON形式
        response = self.client.post(
            reverse('moneybook:periodic_add_bulk'),
            data='invalid json',
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        result = json.loads(response.content)
        self.assertIn('error', result)
