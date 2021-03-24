from datetime import datetime

from django.contrib.auth.models import User
from django.urls import reverse
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
