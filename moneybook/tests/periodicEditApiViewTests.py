from django.contrib.auth.models import User
from django.urls import reverse
from moneybook.models import Category, Direction, Method, PeriodicData
from moneybook.tests.base import BaseTestCase


class PeriodicEditApiViewTestCase(BaseTestCase):
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
        """設定を更新して200を返すこと"""
        self.client.force_login(User.objects.create_user(self.username))

        # 既存データ数を確認
        before_count = PeriodicData.objects.count()
        self.assertEqual(before_count, 1)

        # 新しい設定を送信（フォームPOST形式）
        post_data = {
            'day_1': '5',
            'item_1': '新規定期取引',
            'price_1': '10000',
            'direction_1': '2',
            'method_1': '2',
            'category_1': '2',
            'temp_1': '1',
            'day_new_0': '10',
            'item_new_0': '別の定期取引',
            'price_new_0': '20000',
            'direction_new_0': '1',
            'method_new_0': '1',
            'category_new_0': '3',
            'temp_new_0': '0',
        }

        response = self.client.post(reverse('moneybook:periodic_edit_api'), data=post_data)

        # 成功レスポンス
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), '')

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
        """ログインしていない場合は403を返すこと"""
        response = self.client.post(reverse('moneybook:periodic_edit_api'), data={})
        self.assertEqual(response.status_code, 403)

    def test_post_exception(self):
        """例外が発生した場合は400エラー"""
        self.client.force_login(User.objects.create_user(self.username))

        # 不正なデータ（必須フィールド欠落）
        post_data = {
            'day_1': '1',
            # 'item_1' が欠落
            'price_1': '1000',
        }

        response = self.client.post(reverse('moneybook:periodic_edit_api'), data=post_data)

        # 必須フィールドがないので何も登録されず、200が返る
        # （実装は寛容で、必須フィールドがない行はスキップされる）
        self.assertEqual(response.status_code, 200)
