from moneybook.models import BankBalance
from moneybook.tests.base import BaseTestCase


class BankBalanceTestCase(BaseTestCase):
    def test_str(self):
        self.assertEqual(str(BankBalance.objects.get(pk=1)), 'みずほ')
        self.assertEqual(str(BankBalance.objects.get(pk=2)), '三井住友')

    def test_get_all(self):
        data = BankBalance.get_all()
        self.assertEqual(data[0].name, '三井住友')
        self.assertEqual(data[0].price, 20000)
        self.assertEqual(data[1].name, 'みずほ')
        self.assertEqual(data[1].price, 40000)

    def test_get_price(self):
        self.assertEqual(BankBalance.get_price(1), 40000)
        self.assertEqual(BankBalance.get_price(2), 20000)

    def test_get_price_invalid_pk(self):
        self.assertEqual(BankBalance.get_price(10000), 0)

    def test_set(self):
        BankBalance.set(2, 10001)
        data = BankBalance.get_all()
        self.assertEqual(data[0].name, '三井住友')
        self.assertEqual(data[0].price, 10001)
