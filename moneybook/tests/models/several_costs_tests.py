from moneybook.models import SeveralCosts
from moneybook.tests.base import BaseTestCase


class SeveralCostsTestCase(BaseTestCase):
    def test_str(self):
        self.assertEqual(str(SeveralCosts.objects.get(name='ActualCashBalance')), 'ActualCashBalance')

    def test_get_actual_cash_balance(self):
        self.assertEqual(SeveralCosts.get_actual_cash_balance(), 2000)

    def test_get_actual_cash_balance_nothing(self):
        SeveralCosts.objects.get(name='ActualCashBalance').delete()
        self.assertEqual(SeveralCosts.get_actual_cash_balance(), 0)

    def test_set_actual_cash_balance(self):
        SeveralCosts.set_actual_cash_balance(2001)
        self.assertEqual(SeveralCosts.get_actual_cash_balance(), 2001)

    def test_set_actual_cash_balance_nothing(self):
        SeveralCosts.objects.get(name='ActualCashBalance').delete()
        SeveralCosts.set_actual_cash_balance(2001)
        self.assertEqual(SeveralCosts.get_actual_cash_balance(), 2001)
