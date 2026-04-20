from moneybook.tests.base import BaseTestCase
from moneybook.utils import is_valid_date


class UtilsTestCase(BaseTestCase):
    def test_is_valid_date_january(self):
        self.assertTrue(is_valid_date(2000, 1))

    def test_is_valid_date_december(self):
        self.assertTrue(is_valid_date(2000, 12))

    def test_is_valid_date_out_of_range_month(self):
        self.assertFalse(is_valid_date(2000, 13))

    def test_is_valid_date_zero_year(self):
        self.assertFalse(is_valid_date(0, 1))

    def test_is_valid_date_negative_year(self):
        self.assertFalse(is_valid_date(-1, 1))

    def test_is_valid_date_str_year(self):
        self.assertFalse(is_valid_date('a', 1))

    def test_is_valid_date_str_month(self):
        self.assertFalse(is_valid_date(2000, 'a'))
