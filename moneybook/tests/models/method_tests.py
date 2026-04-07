from moneybook.models import Method
from moneybook.tests.base import BaseTestCase


class MethodTestCase(BaseTestCase):
    def test_get(self):
        self.assertEqual(str(Method.get(1)), '現金')
        self.assertEqual(str(Method.get(4)), 'nanaco')

    def test_list(self):
        ls = Method.list()
        expects = ['銀行', '現金', 'Kyash', 'PayPay']
        self._assert_list(ls, expects)

    def test_unused_list(self):
        ls = Method.un_used_list()
        expects = ['nanaco', 'Edy']
        self._assert_list(ls, expects)

    def test_chargeable_list(self):
        ls = Method.chargeable_list()
        expects = ['Kyash', 'PayPay']
        self._assert_list(ls, expects)
