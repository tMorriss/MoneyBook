from datetime import date

from django.contrib.auth.models import User
from django.urls import reverse
from moneybook.models import Category, Data, Direction, Method, PeriodicData
from moneybook.tests.base import BaseTestCase


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
            day=31,
            item='月末払い',
            price=1000,
            direction=Direction.get(2),
            method=Method.get(1),
            category=Category.get(1),
            temp=False
        )

    def test_add_periodic(self):
        """定期取引データが一括で追加されること"""
        year = 2024
        month = 2

        # 実行前のデータ数
        initial_count = Data.objects.count()

        response = self.client.post(reverse('moneybook:add_periodic_api'), {
            'year': year,
            'month': month
        })

        self.assertEqual(response.status_code, 200)

        # データが2件追加されていること
        self.assertEqual(Data.objects.count(), initial_count + 2)

        # 追加されたデータの内容確認
        # 2024年2月は29日までなので、31日は29日に調整される
        data1 = Data.objects.get(item='家賃', date=date(2024, 2, 1))
        self.assertEqual(data1.price, 50000)

        data2 = Data.objects.get(item='月末払い', date=date(2024, 2, 29))
        self.assertEqual(data2.price, 1000)

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
