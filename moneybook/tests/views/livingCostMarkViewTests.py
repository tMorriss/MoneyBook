from datetime import date
from django.contrib.auth.models import User
from django.urls import reverse
from moneybook.models import LivingCostMark
from moneybook.tests.base import BaseTestCase


class LivingCostMarkViewTestCase(BaseTestCase):
    def test_get(self):
        self.client.force_login(User.objects.create_user(self.username))
        LivingCostMark.objects.create(start_date=date(2024, 1, 1), price=100000)

        response = self.client.get(reverse('moneybook:living_cost_mark'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['living_cost_marks']), 1)
        self._assert_templates(response.templates, ['living_cost_mark.html', '_base.html', '_tools_task_bar.html'])

    def test_get_guest(self):
        response = self.client.get(reverse('moneybook:living_cost_mark'))
        self.assertEqual(response.status_code, 302)


class LivingCostMarkEditViewTestCase(BaseTestCase):
    def test_get(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:living_cost_mark_edit'))
        self.assertEqual(response.status_code, 200)
        self._assert_templates(response.templates, ['living_cost_mark_edit.html', '_base.html', '_tools_task_bar.html'])

    def test_post_success(self):
        self.client.force_login(User.objects.create_user(self.username))
        data = {
            'start_date_1': '2024-01-01',
            'end_date_1': '2024-03-31',
            'price_1': '100,000',
            'start_date_2': '2024-04-01',
            'end_date_2': '',
            'price_2': '120000',
        }
        response = self.client.post(reverse('moneybook:living_cost_mark_edit'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:living_cost_mark'))

        marks = LivingCostMark.get_all()
        self.assertEqual(len(marks), 2)
        self.assertEqual(marks[0].start_date, date(2024, 1, 1))
        self.assertEqual(marks[0].end_date, date(2024, 3, 31))
        self.assertEqual(marks[0].price, 100000)
        self.assertEqual(marks[1].start_date, date(2024, 4, 1))
        self.assertIsNone(marks[1].end_date)
        self.assertEqual(marks[1].price, 120000)

    def test_post_invalid_start_day(self):
        self.client.force_login(User.objects.create_user(self.username))
        data = {
            'start_date_1': '2024-01-02',
            'price_1': '100,000',
        }
        response = self.client.post(reverse('moneybook:living_cost_mark_edit'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '開始日は1日に設定してください')
        self.assertEqual(LivingCostMark.objects.count(), 0)

    def test_post_gap(self):
        self.client.force_login(User.objects.create_user(self.username))
        data = {
            'start_date_1': '2024-01-01',
            'end_date_1': '2024-01-31',
            'price_1': '100,000',
            'start_date_2': '2024-03-01',
            'price_2': '120,000',
        }
        response = self.client.post(reverse('moneybook:living_cost_mark_edit'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '期間に隙間または重複があります')
