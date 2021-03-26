from django.contrib.auth.models import User
from django.urls import reverse
from moneybook.models import Data
from moneybook.tests.commonTests import CommonTestCase


class AddIntraMoveViewTestCase(CommonTestCase):
    fixtures = ['data_test_case']
    username = 'tester'

    def test_get(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:add_intra_move'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:add'))

    def test_get_guest(self):
        response = self.client.get(reverse('moneybook:add'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:login'))

    def test_post(self):
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
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), '')
        after_count = Data.get_all_data().count()
        self.assertEqual(after_count, before_count + 2)

    def test_post_month_range(self):
        self.client.force_login(User.objects.create_user(self.username))
        before_count = Data.get_all_data().count()
        response = self.client.post(
            reverse('moneybook:add_intra_move'),
            {
                'year': 2000,
                'month': 13,
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

    def test_post_day_range(self):
        self.client.force_login(User.objects.create_user(self.username))
        before_count = Data.get_all_data().count()
        response = self.client.post(
            reverse('moneybook:add_intra_move'),
            {
                'year': 2000,
                'month': 2,
                'day': 31,
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
                'price': 20000,
                'before_method': 2,
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), '')
        after_count = Data.get_all_data().count()
        self.assertEqual(after_count, before_count)

    def test_post_guest(self):
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
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:login'))
