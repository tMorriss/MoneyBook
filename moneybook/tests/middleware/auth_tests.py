from http import HTTPStatus

from django.contrib.auth.models import User
from django.urls import reverse
from moneybook.tests.base import BaseTestCase


class AuthMiddlewareTestCase(BaseTestCase):
    def test_guest_access_rules_for_views(self):
        login_url = reverse('moneybook:login')
        cases = [
            ('moneybook:health', HTTPStatus.OK, None),
            ('moneybook:index', HTTPStatus.FOUND, login_url),
            ('moneybook:login', HTTPStatus.OK, None),
        ]

        for url_name, expected_status, expected_redirect in cases:
            with self.subTest(url_name=url_name):
                if url_name == 'moneybook:health':
                    with self.assertNumQueries(0):
                        response = self.client.get(reverse(url_name))
                else:
                    response = self.client.get(reverse(url_name))

                self.assertEqual(response.status_code, expected_status)
                if expected_redirect:
                    self.assertEqual(response.url, expected_redirect)

    def test_health_view_is_accessible_to_authenticated_user(self):
        self.client.force_login(User.objects.create_user(self.username))

        response = self.client.get(reverse('moneybook:health'))

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_api_forbids_guest(self):
        response = self.client.get(reverse('moneybook:add_api'))

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unmatched_path_is_not_auth_exempt(self):
        response = self.client.get('/unknown')

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, reverse('moneybook:login'))
