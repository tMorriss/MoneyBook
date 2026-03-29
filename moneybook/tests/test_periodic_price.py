from django.contrib.auth.models import User
from django.urls import reverse
from moneybook.models import Category, Direction, Method, PeriodicData
from moneybook.tests.base import BaseTestCase

class PeriodicPriceTestCase(BaseTestCase):
    def test_post_price_without_comma(self):
        """金額が正常に保存されることを確認"""
        self.client.force_login(User.objects.create_user(self.username))

        post_data = {
            'day_new_0': '10',
            'item_new_0': 'テスト',
            'price_new_0': '1000',
            'direction_new_0': '2',
            'method_new_0': '1',
            'category_new_0': '1',
            'temp_new_0': '0',
        }

        self.client.post(reverse('moneybook:periodic_edit'), data=post_data)

        pd = PeriodicData.objects.get(item='テスト')
        self.assertEqual(pd.price, 1000)
