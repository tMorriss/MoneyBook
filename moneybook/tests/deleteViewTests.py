from django.contrib.auth.models import User
from django.urls import reverse
from moneybook.models import Data
from moneybook.tests.common import CommonTestCase


class DeleteViewTestCase(CommonTestCase):
    def test_get(self):
        self.client.force_login(User.objects.create_user(self.username))
        before_count = Data.get_all_data().count()
        response = self.client.get(reverse('moneybook:delete'), {'pk': 1})
        self.assertEqual(response.status_code, 405)
        after_count = Data.get_all_data().count()
        self.assertEqual(after_count, before_count)

    def test_post(self):
        self.client.force_login(User.objects.create_user(self.username))
        before_count = Data.get_all_data().count()
        response = self.client.post(reverse('moneybook:delete'), {'pk': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), '')
        after_count = Data.get_all_data().count()
        self.assertEqual(after_count, before_count - 1)

    def test_post_not_exist(self):
        self.client.force_login(User.objects.create_user(self.username))
        before_count = Data.get_all_data().count()
        response = self.client.post(reverse('moneybook:delete'), {'pk': 100000})
        self.assertEqual(response.status_code, 400)
        after_count = Data.get_all_data().count()
        self.assertEqual(after_count, before_count)

    def test_post_guest(self):
        response = self.client.post(reverse('moneybook:delete'), {'pk': 1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:login'))
