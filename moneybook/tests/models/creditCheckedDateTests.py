from datetime import date

from moneybook.models import CreditCheckedDate
from moneybook.tests.base import BaseTestCase


class CreditCheckedDateTestCase(BaseTestCase):
    def test_get_all(self):
        data = CreditCheckedDate.get_all()
        self.assertEqual(data[0].name, 'AmexGold')
        self.assertEqual(data[0].date, date(2000, 2, 4))
        self.assertEqual(data[0].price, 2000)
        self.assertEqual(data[1].name, 'センチュリオン')
        self.assertEqual(data[1].date, date(3000, 1, 1))
        self.assertEqual(data[1].price, 30000)

    def test_get_price(self):
        self.assertEqual(CreditCheckedDate.get_price(1), 30000)
        self.assertEqual(CreditCheckedDate.get_price(2), 2000)

    def test_get_price_invalid_pk(self):
        self.assertEqual(CreditCheckedDate.get_price(10000), 0)

    def test_set_date(self):
        CreditCheckedDate.set_date(2, date(2001, 1, 2))
        data = CreditCheckedDate.get_all()
        self.assertEqual(data[0].name, 'AmexGold')
        self.assertEqual(data[0].date, date(2001, 1, 2))

    def test_set_price(self):
        CreditCheckedDate.set_price(2, 2001)
        data = CreditCheckedDate.get_all()
        self.assertEqual(data[0].name, 'AmexGold')
        self.assertEqual(data[0].price, 2001)
