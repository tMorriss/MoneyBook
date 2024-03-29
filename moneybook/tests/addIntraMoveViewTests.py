from datetime import date

from django.contrib.auth.models import User
from django.urls import reverse
from moneybook.models import Data
from moneybook.tests.base import BaseTestCase


class AddIntraMoveViewTestCase(BaseTestCase):
    def test_get(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:add_intra_move'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:add'))

    def test_get_guest(self):
        response = self.client.get(reverse('moneybook:add'))
        self.assertEqual(response.status_code, 403)

    def test_post(self):
        self.client.force_login(User.objects.create_user(self.username))
        before_count = Data.get_all_data().count()
        response = self.client.post(
            reverse('moneybook:add_intra_move'),
            {
                'year': 2000,
                'month': 4,
                'day': 1,
                'item': '内部移動テスト',
                'price': 20000,
                'before_method': 2,
                'after_method': 3,
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), '')
        after_count = Data.get_all_data().count()
        self.assertEqual(after_count, before_count + 2)
        before = Data.get_all_data()[after_count - 2]
        self.assertEqual(before.date, date(2000, 4, 1))
        self.assertEqual(before.item, '内部移動テスト')
        self.assertEqual(before.price, 20000)
        self.assertEqual(before.direction.pk, 2)
        self.assertEqual(before.method.pk, 2)
        self.assertEqual(before.category.pk, 4)
        self.assertEqual(before.temp, False)
        self.assertEqual(before.checked, False)
        after = Data.get_all_data()[after_count - 1]
        self.assertEqual(after.date, date(2000, 4, 1))
        self.assertEqual(after.item, '内部移動テスト')
        self.assertEqual(after.price, 20000)
        self.assertEqual(after.direction.pk, 1)
        self.assertEqual(after.method.pk, 3)
        self.assertEqual(after.category.pk, 4)
        self.assertEqual(after.temp, False)
        self.assertEqual(after.checked, False)

    def test_post_month_range(self):
        self.client.force_login(User.objects.create_user(self.username))
        before_count = Data.get_all_data().count()
        response = self.client.post(
            reverse('moneybook:add_intra_move'),
            {
                'year': 2000,
                'month': 13,
                'day': 1,
                'item': '内部移動テスト',
                'price': 20000,
                'before_method': 2,
                'after_method': 3,
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), '')
        after_count = Data.get_all_data().count()
        self.assertEqual(after_count, before_count)

    def test_post_day_range(self):
        self.client.force_login(User.objects.create_user(self.username))
        before_count = Data.get_all_data().count()
        response = self.client.post(
            reverse('moneybook:add_intra_move'),
            {
                'year': 2000,
                'month': 2,
                'day': 31,
                'item': '内部移動テスト',
                'price': 20000,
                'before_method': 2,
                'after_method': 3,
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), '')
        after_count = Data.get_all_data().count()
        self.assertEqual(after_count, before_count)

    def test_post_missing_item(self):
        self.client.force_login(User.objects.create_user(self.username))
        before_count = Data.get_all_data().count()
        response = self.client.post(
            reverse('moneybook:add_intra_move'),
            {
                'year': 2000,
                'month': 4,
                'day': 1,
                'price': 20000,
                'before_method': 2,
                'after_method': 3,
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), '')
        after_count = Data.get_all_data().count()
        self.assertEqual(after_count, before_count)

    def test_post_missing_price(self):
        self.client.force_login(User.objects.create_user(self.username))
        before_count = Data.get_all_data().count()
        response = self.client.post(
            reverse('moneybook:add_intra_move'),
            {
                'year': 2000,
                'month': 4,
                'day': 1,
                'item': '内部移動テスト',
                'before_method': 2,
                'after_method': 3,
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), '')
        after_count = Data.get_all_data().count()
        self.assertEqual(after_count, before_count)

    def test_post_missing_before_method(self):
        self.client.force_login(User.objects.create_user(self.username))
        before_count = Data.get_all_data().count()
        response = self.client.post(
            reverse('moneybook:add_intra_move'),
            {
                'year': 2000,
                'month': 4,
                'day': 1,
                'item': '内部移動テスト',
                'price': 20000,
                'after_method': 3,
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), '')
        after_count = Data.get_all_data().count()
        self.assertEqual(after_count, before_count)

    def test_post_missing_after_method(self):
        self.client.force_login(User.objects.create_user(self.username))
        before_count = Data.get_all_data().count()
        response = self.client.post(
            reverse('moneybook:add_intra_move'),
            {
                'year': 2000,
                'month': 4,
                'day': 1,
                'item': '内部移動テスト',
                'price': 20000,
                'before_method': 2,
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), '')
        after_count = Data.get_all_data().count()
        self.assertEqual(after_count, before_count)

    def test_post_guest(self):
        before_count = Data.get_all_data().count()
        response = self.client.post(
            reverse('moneybook:add_intra_move'),
            {
                'year': 2000,
                'month': 4,
                'day': 1,
                'item': '内部移動テスト',
                'price': 20000,
                'before_method': 2,
                'after_method': 3,
            }
        )
        self.assertEqual(response.status_code, 403)
        after_count = Data.get_all_data().count()
        self.assertEqual(after_count, before_count)
