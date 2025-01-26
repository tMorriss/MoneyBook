import json
from datetime import datetime

from django.contrib.auth.models import User
from django.urls import reverse
from moneybook.models import Data
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
        self.assertEqual(response.status_code, 403)

    def test_post(self):
        self.client.force_login(User.objects.create_user(self.username))
        before_count = Data.get_all_data().count()
        response = self.client.post(
            reverse('moneybook:add'),
            {
                'date': '2000-4-1',
                'item': 'テスト項目1',
                'price': 10000,
                'direction': 2,
                'method': 2,
                'category': 1,
                'temp': False,
                'checked': False
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), '')
        after_count = Data.get_all_data().count()
        self.assertEqual(after_count, before_count + 1)

    def test_post_invalid(self):
        self.client.force_login(User.objects.create_user(self.username))
        before_count = Data.get_all_data().count()
        response = self.client.post(
            reverse('moneybook:add'),
            {
                'item': 'テスト項目1',
                'direction': 2,
                'method': 2,
                'category': 1,
                'temp': False,
                'checked': False
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), json.dumps({'ErrorList': ['date', 'price']}))
        after_count = Data.get_all_data().count()
        self.assertEqual(after_count, before_count)

    def test_post_guest(self):
        before_count = Data.get_all_data().count()
        response = self.client.post(
            reverse('moneybook:add'),
            {
                'date': '2000-4-1',
                'item': 'テスト項目1',
                'price': 10000,
                'direction': 2,
                'method': 2,
                'category': 1,
                'temp': False,
                'checked': False
            }
        )
        self.assertEqual(response.status_code, 403)
        after_count = Data.get_all_data().count()
        self.assertEqual(after_count, before_count)


class SuggestViewTestCase(BaseTestCase):
    def test_get(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:suggest'), {'item': '必需品'})

        self.assertEqual(response.status_code, 200, response.content)
        body = json.loads(response.content.decode())

        expects = [{'date': '2000-02-01', 'item': '必需品3', 'price': 400},
                   {'date': '2000-01-08', 'item': '必需品2', 'price': 3500},
                   {'date': '2000-01-05', 'item': '必需品1', 'price': 1000}]
        self.assertEqual(body.count(), len(expects))
        for i in range(len(expects)):
            with self.subTest(i=i):
                self.assertEqual(body[i], expects[i])

    def test_get_distinct(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:suggest'), {'item': 'PayPayチャージ'})

        self.assertEqual(response.status_code, 200, response.content)
        body = json.loads(response.content.decode())

        expects = [{'date': '2000-01-25', 'item': 'PayPayチャージ', 'price': 1000},
                   {'date': '2000-01-25', 'item': 'PayPayチャージ', 'price': 1000}]
        self.assertEqual(body.count(), len(expects))
        for i in range(len(expects)):
            with self.subTest(i=i):
                self.assertEqual(body[i], expects[i])

    def test_get_missing_item(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:suggest'))

        self.assertEqual(response.status_code, 400, response.content)
        body = json.loads(response.content.decode())
        self.assertEqual(body, {"message": "missing item"})

    def test_get_empty_item(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:suggest'), {'item': ''})

        self.assertEqual(response.status_code, 400, response.content)
        body = json.loads(response.content.decode())
        self.assertEqual(body, {"message": "empty item"})
