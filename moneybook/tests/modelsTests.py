from django.test import TestCase
from moneybook.models import Category, Direction, Method


class DirectionTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Direction.objects.create(name="収入")
        Direction.objects.create(name="支出")

    def test_get(self):
        self.assertEqual(str(Direction.get(1)), "収入")
        self.assertEqual(str(Direction.get(2)), "支出")

    def test_list(self):
        ls = Direction.list()
        self.assertEqual(len(ls), 2)
        self.assertEqual(str(ls[0]), "収入")
        self.assertEqual(str(ls[1]), "支出")


class MethodTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Method.objects.create(show_order=1, name="1", chargeable=True)
        Method.objects.create(show_order=2, name="2", chargeable=False)
        Method.objects.create(show_order=0, name="0", chargeable=False)
        Method.objects.create(show_order=-2, name="-2", chargeable=False)
        Method.objects.create(show_order=-1, name="-1", chargeable=True)

    def test_get(self):
        self.assertEqual(str(Method.get(1)), "1")
        self.assertEqual(str(Method.get(4)), "-2")

    def test_list(self):
        ls = Method.list()
        self.assertEqual(len(ls), 2)
        self.assertEqual(str(ls[0]), "1")
        self.assertEqual(str(ls[1]), "2")

    def test_unUsedList(self):
        ls = Method.unUsedList()
        self.assertEqual(len(ls), 3)
        self.assertEqual(str(ls[0]), "0")
        self.assertEqual(str(ls[1]), "-1")
        self.assertEqual(str(ls[2]), "-2")

    def test_chargeableList(self):
        ls = Method.chargeableList()
        self.assertEqual(len(ls), 1)
        self.assertEqual(str(ls[0]), "1")


class CategoryTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Category.objects.create(show_order=1, name="1",
                                is_living_cost=True, is_variable_cost=False)
        Category.objects.create(show_order=2, name="2",
                                is_living_cost=False, is_variable_cost=True)
        Category.objects.create(show_order=0, name="0",
                                is_living_cost=False, is_variable_cost=False)
        Category.objects.create(show_order=-1, name="-1",
                                is_living_cost=False, is_variable_cost=False)
        Category.objects.create(show_order=-2, name="-2",
                                is_living_cost=False, is_variable_cost=False)

    def test_get(self):
        self.assertEqual(str(Category.get(1)), "1")
        self.assertEqual(str(Category.get(4)), "-1")

    def test_list(self):
        ls = Category.list()
        self.assertEqual(len(ls), 5)
        self.assertEqual(str(ls[0]), "-2")
        self.assertEqual(str(ls[4]), "2")

    def test_first_list(self):
        ls = Category.first_list()
        self.assertEqual(len(ls), 2)
        self.assertEqual(str(ls[0]), "1")
        self.assertEqual(str(ls[1]), "2")

    def test_latter_list(self):
        ls = Category.latter_list()
        self.assertEqual(len(ls), 3)
        self.assertEqual(str(ls[0]), "0")
        self.assertEqual(str(ls[2]), "-2")
