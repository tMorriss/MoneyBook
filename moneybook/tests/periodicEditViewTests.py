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

