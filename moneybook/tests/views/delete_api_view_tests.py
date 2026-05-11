from http import HTTPStatus

from django.contrib.auth.models import User
from django.urls import reverse
from moneybook.models import Data
from moneybook.tests.base import BaseTestCase


class DeleteApiViewTestCase(BaseTestCase):
    def test_get(self):
        self.client.force_login(User.objects.create_user(self.username))
        before_count = Data.get_all_data().count()
        response = self.client.get(reverse('moneybook:delete_api'), {'pk': 1})
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        after_count = Data.get_all_data().count()
        self.assertEqual(after_count, before_count)

    def test_post(self):
        self.client.force_login(User.objects.create_user(self.username))
        before_count = Data.get_all_data().count()
        response = self.client.post(reverse('moneybook:delete_api'), {'pk': 1})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.content.decode(), '{}')
        after_count = Data.get_all_data().count()
        self.assertEqual(after_count, before_count - 1)

    def test_post_not_exist(self):
        self.client.force_login(User.objects.create_user(self.username))
        before_count = Data.get_all_data().count()
        response = self.client.post(reverse('moneybook:delete_api'), {'pk': 100000})
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        after_count = Data.get_all_data().count()
        self.assertEqual(after_count, before_count)

    def test_post_guest(self):
        before_count = Data.get_all_data().count()
        response = self.client.post(reverse('moneybook:delete_api'), {'pk': 1})
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        after_count = Data.get_all_data().count()
        self.assertEqual(after_count, before_count)
