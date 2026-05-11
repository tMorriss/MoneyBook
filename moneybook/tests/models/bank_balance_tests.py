from moneybook.models import BankBalance
from moneybook.tests.base import BaseTestCase


class BankBalanceTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        BankBalance.objects.all().delete()
        BankBalance.objects.create(pk=1, name='B1', price=40000, show_order=2)
        BankBalance.objects.create(pk=2, name='B2', price=20000, show_order=1)

    def test_str(self):
        self.assertEqual(str(BankBalance.objects.get(pk=1)), 'B1')
        self.assertEqual(str(BankBalance.objects.get(pk=2)), 'B2')

    def test_get_all(self):
        data = BankBalance.get_all()
        self.assertEqual(data[0].name, 'B2')
        self.assertEqual(data[0].price, 20000)
        self.assertEqual(data[1].name, 'B1')
        self.assertEqual(data[1].price, 40000)

    def test_get_price(self):
        self.assertEqual(BankBalance.get_price(1), 40000)
        self.assertEqual(BankBalance.get_price(2), 20000)

    def test_get_price_invalid_pk(self):
        self.assertEqual(BankBalance.get_price(10000), 0)

    def test_set(self):
        BankBalance.set(2, 10001)
        data = BankBalance.get_all()
        self.assertEqual(data[0].name, 'B2')
        self.assertEqual(data[0].price, 10001)
