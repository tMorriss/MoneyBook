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
