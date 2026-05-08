from moneybook.models import Direction
from moneybook.tests.base import BaseTestCase


class DirectionTestCase(BaseTestCase):
    def test_get(self):
        self.assertEqual(str(Direction.get(1)), '収入')
        self.assertEqual(str(Direction.get(2)), '支出')

    def test_list(self):
        ls = Direction.list()
        self.assertEqual(ls.count(), 2)
        self.assertEqual(str(ls[0]), '収入')
        self.assertEqual(str(ls[1]), '支出')
