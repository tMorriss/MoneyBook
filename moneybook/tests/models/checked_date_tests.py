from datetime import date

from moneybook.models import CheckedDate
from moneybook.tests.base import BaseTestCase


class CheckedDateTestCase(BaseTestCase):
    def test_str(self):
        self.assertEqual(str(CheckedDate.get(1)), '現金')
        self.assertEqual(str(CheckedDate.get(2)), '銀行')

    def test_get(self):
        self.assertEqual(CheckedDate.get(1).date, date(2000, 1, 2))
        self.assertEqual(CheckedDate.get(2).date, date(2000, 1, 5))
        self.assertEqual(CheckedDate.get(3).date, date(2000, 2, 2))

    def test_set(self):
        CheckedDate.set(1, date(2001, 1, 1))
        self.assertEqual(CheckedDate.get(1).date, date(2001, 1, 1))
