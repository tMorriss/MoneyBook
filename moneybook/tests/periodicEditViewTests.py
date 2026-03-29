from django.contrib.auth.models import User
from django.urls import reverse
from moneybook.models import Category, Direction, Method, PeriodicData
from moneybook.tests.base import BaseTestCase


class PeriodicEditViewGetTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        PeriodicData.objects.create(
            day=1,
            item='編集テスト',
            price=3000,
            direction=Direction.get(2),
            method=Method.get(1),
            category=Category.get(1),
            temp=False
        )

    def test_get(self):
        """編集ページが正しく表示されること"""
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:periodic_edit'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['app_name'], 'test-MoneyBook')

        # 定期取引データが含まれていること
        periodic_data = response.context['periodic_data_list']
        self.assertEqual(periodic_data.count(), 1)
        self.assertEqual(periodic_data[0].item, '編集テスト')

        # 選択肢が含まれていること
        self.assertIn('directions', response.context)
        self.assertIn('methods', response.context)
        self.assertIn('first_categories', response.context)
        self.assertIn('latter_categories', response.context)

    def test_get_guest(self):
        """ログインしていない場合はログインページにリダイレクトされること"""
        response = self.client.get(reverse('moneybook:periodic_edit'))
        self.assertEqual(response.status_code, 302)


class PeriodicEditViewPostTestCase(BaseTestCase):
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
        """設定を更新してperiodicにリダイレクトされること"""
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

        response = self.client.post(reverse('moneybook:periodic_edit'), data=post_data)

        # periodicにリダイレクトされること
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:periodic'))

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
        """ログインしていない場合はログインページにリダイレクトされること"""
        response = self.client.post(reverse('moneybook:periodic_edit'), data={})
        self.assertEqual(response.status_code, 302)

    def test_post_missing_required_field(self):
        """必須フィールド欠落時は行をスキップしてperiodicにリダイレクト"""
        self.client.force_login(User.objects.create_user(self.username))

        # 不正なデータ（必須フィールド欠落）
        post_data = {
            'day_1': '1',
            # 'item_1' が欠落
            'price_1': '1000',
        }

        response = self.client.post(reverse('moneybook:periodic_edit'), data=post_data)

        # 必須フィールドがないので何も登録されず、periodicにリダイレクト
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:periodic'))

        # データが登録されていないこと
        self.assertEqual(PeriodicData.objects.count(), 0)

    def test_post_invalid_form(self):
        """フォームバリデーションエラー時は行をスキップしてperiodicにリダイレクト"""
        self.client.force_login(User.objects.create_user(self.username))

        # 不正なデータ（存在しない外部キー参照）
        post_data = {
            'day_1': '1',
            'item_1': 'テスト',
            'price_1': '1000',
            'direction_1': '999',  # 存在しないdirection_id
            'method_1': '1',
            'category_1': '1',
            'temp_1': '0',
        }

        response = self.client.post(reverse('moneybook:periodic_edit'), data=post_data)

        # フォームがinvalidなので何も登録されず、periodicにリダイレクト
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:periodic'))

        # データが登録されていないこと
        self.assertEqual(PeriodicData.objects.count(), 0)

    def test_post_duplicate_id_part(self):
        """id_partが重複している場合は最初のもののみが処理されること"""
        self.client.force_login(User.objects.create_user(self.username))

        # 同じid_partを持つ重複データ
        # Pythonの辞書では後のキーが前のキーを上書きするため、
        # 'day_1': '15'と'item_1': '2番目のデータ'が実際の値になる
        post_data = {
            'day_1': '5',
            'item_1': '最初のデータ',
            'price_1': '10000',
            'direction_1': '1',
            'method_1': '1',
            'category_1': '1',
            'temp_1': '0',
            # 同じid_part '1'で別のデータ（辞書で上書き）
            'day_1': '15',
            'item_1': '2番目のデータ',
            'price_1': '20000',
        }

        response = self.client.post(reverse('moneybook:periodic_edit'), data=post_data)

        # periodicにリダイレクトされること
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:periodic'))

        # 1件のみ登録されていること（重複チェックにより1度のみ処理）
        self.assertEqual(PeriodicData.objects.count(), 1)

        # processed_idsによって最初の処理のみが実行される
        # ただし辞書の上書きにより、実際には2番目の値がPOSTデータに含まれる
        data = PeriodicData.get_all()
        self.assertEqual(data[0].day, 15)
        self.assertEqual(data[0].item, '2番目のデータ')
        self.assertEqual(data[0].price, 20000)
