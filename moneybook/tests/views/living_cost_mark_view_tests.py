from datetime import date

from django.contrib.auth.models import User
from django.urls import reverse
from moneybook.models import LivingCostMark
from moneybook.tests.base import BaseTestCase


class LivingCostMarkViewTestCase(BaseTestCase):
    def test_get(self):
        self.client.force_login(User.objects.create_user(self.username))
        LivingCostMark.objects.all().delete()
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
            'start_year_1': '2024',
            'start_month_1': '1',
            'end_year_1': '2024',
            'end_month_1': '3',
            'price_1': '100,000',
            'start_year_2': '2024',
            'start_month_2': '4',
            'end_year_2': '',
            'end_month_2': '',
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

    def test_post_incomplete_start_date_year(self):
        self.client.force_login(User.objects.create_user(self.username))
        LivingCostMark.objects.all().delete()
        data = {
            'start_year_1': '',
            'start_month_1': '1',
            'price_1': '100,000',
        }
        response = self.client.post(reverse('moneybook:living_cost_mark_edit'), data)
        self.assertContains(response, '開始年月の入力が不完全です')

    def test_post_incomplete_start_date_month(self):
        self.client.force_login(User.objects.create_user(self.username))
        data = {
            'start_year_1': '2024',
            'start_month_1': '',
            'price_1': '100,000',
        }
        response = self.client.post(reverse('moneybook:living_cost_mark_edit'), data)
        self.assertContains(response, '開始年月の入力が不完全です')

    def test_post_incomplete_end_date_year(self):
        self.client.force_login(User.objects.create_user(self.username))
        data = {
            'start_year_1': '2024',
            'start_month_1': '1',
            'end_year_1': '',
            'end_month_1': '1',
            'price_1': '100,000',
        }
        response = self.client.post(reverse('moneybook:living_cost_mark_edit'), data)
        self.assertContains(response, '終了年月の入力が不完全です')

    def test_post_incomplete_end_date_month(self):
        self.client.force_login(User.objects.create_user(self.username))
        data = {
            'start_year_1': '2024',
            'start_month_1': '1',
            'end_year_1': '2024',
            'end_month_1': '',
            'price_1': '100,000',
        }
        response = self.client.post(reverse('moneybook:living_cost_mark_edit'), data)
        self.assertContains(response, '終了年月の入力が不完全です')

    def test_post_start_gte_end(self):
        self.client.force_login(User.objects.create_user(self.username))
        data = {
            'start_year_1': '2024',
            'start_month_1': '2',
            'end_year_1': '2024',
            'end_month_1': '1',
            'price_1': '100,000',
        }
        response = self.client.post(reverse('moneybook:living_cost_mark_edit'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '開始年月は終了年月より前に設定してください')

    def test_post_middle_no_end_date(self):
        self.client.force_login(User.objects.create_user(self.username))
        data = {
            'start_year_1': '2024',
            'start_month_1': '1',
            'end_year_1': '',
            'end_month_1': '',  # 途中のデータなのに終了日がない
            'price_1': '100,000',
            'start_year_2': '2024',
            'start_month_2': '2',
            'price_2': '120,000',
        }
        response = self.client.post(reverse('moneybook:living_cost_mark_edit'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '途中のデータの終了年月は必須です')

    def test_post_overlap(self):
        """期間が重複している場合はエラー"""
        self.client.force_login(User.objects.create_user(self.username))
        data = {
            'start_year_1': '2024',
            'start_month_1': '1',
            'end_year_1': '2024',
            'end_month_1': '2',  # 2月まで
            'price_1': '100,000',
            'start_year_2': '2024',
            'start_month_2': '2',  # 重複
            'price_2': '120,000',
        }
        response = self.client.post(reverse('moneybook:living_cost_mark_edit'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '期間に隙間または重複があります')

    def test_post_gap(self):
        """期間に隙間がある場合はエラー"""
        self.client.force_login(User.objects.create_user(self.username))
        data = {
            'start_year_1': '2024',
            'start_month_1': '1',
            'end_year_1': '2024',
            'end_month_1': '1',
            'price_1': '100,000',
            'start_year_2': '2024',
            'start_month_2': '3',  # 2月が抜けている
            'price_2': '120,000',
        }
        response = self.client.post(reverse('moneybook:living_cost_mark_edit'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '期間に隙間または重複があります')

    def test_post_null_start_multiple(self):
        """開始日がnullのデータが複数ある場合はエラー"""
        self.client.force_login(User.objects.create_user(self.username))
        data = {
            'start_year_1': '',
            'start_month_1': '',
            'price_1': '100,000',
            'start_year_2': '',
            'start_month_2': '',
            'price_2': '120,000',
        }
        response = self.client.post(reverse('moneybook:living_cost_mark_edit'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '開始年月が空のデータは1行だけ指定できます')

    def test_post_invalid_month_range(self):
        self.client.force_login(User.objects.create_user(self.username))
        data = {
            'start_year_1': '2024',
            'start_month_1': '13',
            'price_1': '100,000',
        }
        response = self.client.post(reverse('moneybook:living_cost_mark_edit'), data)
        self.assertContains(response, '開始年月の値が不正です')

    def test_post_invalid_end_month(self):
        self.client.force_login(User.objects.create_user(self.username))
        data = {
            'start_year_1': '2024',
            'start_month_1': '1',
            'end_year_1': '2024',
            'end_month_1': 'abc',
            'price_1': '100,000',
        }
        response = self.client.post(reverse('moneybook:living_cost_mark_edit'), data)
        self.assertContains(response, '終了年月の値が不正です')

    def test_post_invalid_price(self):
        self.client.force_login(User.objects.create_user(self.username))
        data = {
            'start_year_1': '2024',
            'start_month_1': '1',
            'price_1': 'abc',
        }
        response = self.client.post(reverse('moneybook:living_cost_mark_edit'), data)
        self.assertContains(response, '金額が不正です')

    def test_post_empty_price_skip(self):
        self.client.force_login(User.objects.create_user(self.username))
        data = {
            'start_year_1': '2024',
            'start_month_1': '1',
            'price_1': '',
        }
        response = self.client.post(reverse('moneybook:living_cost_mark_edit'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(LivingCostMark.objects.count(), 0)

    def test_str(self):
        mark = LivingCostMark(start_date=date(2024, 1, 1), price=100000)
        self.assertEqual(str(mark), '2024-01-01 - None: 100000')
