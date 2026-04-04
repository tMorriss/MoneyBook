from datetime import datetime

from django.contrib.auth.models import User
from django.urls import reverse
from moneybook.tests.base import BaseTestCase


class AddViewTestCase(BaseTestCase):
    def test_get(self):
        now = datetime.now()
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:add'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['app_name'], 'test-MoneyBook')
        self.assertEqual(response.context['username'].username, self.username)
        self.assertEqual(response.context['year'], now.year)
        self.assertEqual(response.context['month'], now.month)
        self.assertEqual(response.context['day'], now.day)
        self._assert_all_directions(response)
        self._assert_all_methods(response)
        self._assert_all_chargeable_methods(response)
        self._assert_all_first_categories(response)
        self._assert_all_latter_categories(response)
        self._assert_all_temps(response)

        expects = [
            'add.html',
            '_base.html',
            '_result_message.html',
        ]
        self._assert_templates(response.templates, expects)

    def test_get_guest(self):
        response = self.client.get(reverse('moneybook:add'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('moneybook:login'))
