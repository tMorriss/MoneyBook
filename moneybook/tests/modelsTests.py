from datetime import date

from django.test import TestCase
from moneybook.models import Category, Data, Direction, Method


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
        l = Direction.list()
        self.assertEqual(len(l), 2)
        self.assertEqual(str(l[0]), "収入")
        self.assertEqual(str(l[1]), "支出")


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
        l = Method.list()
        self.assertEqual(len(l), 2)
        self.assertEqual(str(l[0]), "1")
        self.assertEqual(str(l[1]), "2")

    def test_unUsedList(self):
        l = Method.unUsedList()
        self.assertEqual(len(l), 3)
        self.assertEqual(str(l[0]), "0")
        self.assertEqual(str(l[1]), "-1")
        self.assertEqual(str(l[2]), "-2")

    def test_chargeableList(self):
        l = Method.chargeableList()
        self.assertEqual(len(l), 1)
        self.assertEqual(str(l[0]), "1")


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
        l = Category.list()
        self.assertEqual(len(l), 5)
        self.assertEqual(str(l[0]), "-2")
        self.assertEqual(str(l[4]), "2")

    def test_first_list(self):
        l = Category.first_list()
        self.assertEqual(len(l), 2)
        self.assertEqual(str(l[0]), "1")
        self.assertEqual(str(l[1]), "2")

    def test_latter_list(self):
        l = Category.latter_list()
        self.assertEqual(len(l), 3)
        self.assertEqual(str(l[0]), "0")
        self.assertEqual(str(l[2]), "-2")
