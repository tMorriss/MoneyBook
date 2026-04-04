from datetime import date

from moneybook.models import LivingCostMark
from moneybook.tests.base import BaseTestCase


class LivingCostMarkTestCase(BaseTestCase):
    def test_get_mark(self):
        LivingCostMark.objects.create(start_date=date(2024, 1, 1), end_date=date(2024, 3, 31), price=100000)
        LivingCostMark.objects.create(start_date=date(2024, 4, 1), price=120000)

        self.assertEqual(LivingCostMark.get_mark(2024, 1), 100000)
        self.assertEqual(LivingCostMark.get_mark(2024, 2), 100000)
        self.assertEqual(LivingCostMark.get_mark(2024, 3), 100000)
        self.assertEqual(LivingCostMark.get_mark(2024, 4), 120000)
        self.assertEqual(LivingCostMark.get_mark(2024, 12), 120000)
        self.assertEqual(LivingCostMark.get_mark(2023, 12), 0)
