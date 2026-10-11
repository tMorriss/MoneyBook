from http import HTTPStatus

from django.test import RequestFactory
from moneybook.tests.base import BaseTestCase
from moneybook.views import HealthView


class HealthViewTestCase(BaseTestCase):
    def test_get_returns_ok(self):
        request = RequestFactory().get('/healthz')

        with self.assertNumQueries(0):
            response = HealthView.as_view()(request)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.content, b'ok')
        self.assertEqual(response['Content-Type'], 'text/plain')
