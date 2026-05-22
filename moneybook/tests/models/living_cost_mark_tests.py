from datetime import date

from moneybook.models import LivingCostMark
from moneybook.tests.base import BaseTestCase


class LivingCostMarkTestCase(BaseTestCase):
    def test_get_mark(self):
        LivingCostMark.objects.all().delete()
        # Null start date row
        LivingCostMark.objects.create(start_date=None, end_date=date(2023, 12, 31), price=90000)
        LivingCostMark.objects.create(start_date=date(2024, 1, 1), end_date=date(2024, 3, 31), price=100000)
        LivingCostMark.objects.create(start_date=date(2024, 4, 1), price=120000)

        self.assertEqual(LivingCostMark.get_mark(2023, 1), 90000)
        self.assertEqual(LivingCostMark.get_mark(2023, 12), 90000)
        self.assertEqual(LivingCostMark.get_mark(2024, 1), 100000)
        self.assertEqual(LivingCostMark.get_mark(2024, 2), 100000)
        self.assertEqual(LivingCostMark.get_mark(2024, 3), 100000)
        self.assertEqual(LivingCostMark.get_mark(2024, 4), 120000)
        self.assertEqual(LivingCostMark.get_mark(2024, 12), 120000)

    def test_get_mark_no_data(self):
        LivingCostMark.objects.all().delete()
        self.assertEqual(LivingCostMark.get_mark(2024, 1), 0)

    def test_str(self):
        mark1 = LivingCostMark(start_date=date(2024, 1, 1), end_date=date(2024, 3, 31), price=100000)
        self.assertEqual(str(mark1), '2024-01-01 - 2024-03-31: 100000')

        mark2 = LivingCostMark(start_date=None, end_date=date(2023, 12, 31), price=90000)
        self.assertEqual(str(mark2), 'None - 2023-12-31: 90000')

        mark3 = LivingCostMark(start_date=date(2024, 4, 1), end_date=None, price=120000)
        self.assertEqual(str(mark3), '2024-04-01 - None: 120000')
