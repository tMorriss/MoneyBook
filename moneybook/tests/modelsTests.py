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
        ls = Direction.list()
        self.assertEqual(ls.count(), 2)
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
        self.assertEqual(ls.count(), 2)
        self.assertEqual(str(ls[0]), "1")
        self.assertEqual(str(ls[1]), "2")

    def test_unUsedList(self):
        ls = Method.unUsedList()
        self.assertEqual(ls.count(), 3)
        self.assertEqual(str(ls[0]), "0")
        self.assertEqual(str(ls[1]), "-1")
        self.assertEqual(str(ls[2]), "-2")

    def test_chargeableList(self):
        ls = Method.chargeableList()
        self.assertEqual(ls.count(), 1)
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
        self.assertEqual(ls.count(), 5)
        self.assertEqual(str(ls[0]), "-2")
        self.assertEqual(str(ls[4]), "2")

    def test_first_list(self):
        ls = Category.first_list()
        self.assertEqual(ls.count(), 2)
        self.assertEqual(str(ls[0]), "1")
        self.assertEqual(str(ls[1]), "2")

    def test_latter_list(self):
        ls = Category.latter_list()
        self.assertEqual(ls.count(), 3)
        self.assertEqual(str(ls[0]), "0")
        self.assertEqual(str(ls[2]), "-2")


class DataTestCase(TestCase):
    fixtures = ['data_test_case']

    def test_getAllData(self):
        self.assertEqual(Data.getAllData().count(), 31)

    def test_getRangeData(self):
        start = date(2000, 2, 1)
        end = date(2000, 2, 10)
        data = Data.getRangeData(start, end)
        self.assertEqual(data.count(), 2)
        self.assertEqual(str(data[0]), "必需品1")
        self.assertEqual(str(data[1]), "収入")

    def test_getMonthData(self):
        data = Data.getMonthData(2000, 2)
        self.assertEqual(data.count(), 3)
        self.assertEqual(str(data[0]), "必需品1")
        self.assertEqual(str(data[1]), "収入")
        self.assertEqual(str(data[2]), "スーパー")

    def test_getSum(self):
        data = Data.getMonthData(2000, 2)
        self.assertEqual(Data.getSum(data, 1), 3000)
        self.assertEqual(Data.getSum(data, 2), 2000)

        self.assertEqual(Data.getSum(Data.getMonthData(1999, 1), 1), 0)

    def test_getIncomeSum(self):
        data = Data.getMonthData(2000, 2)
        self.assertEqual(Data.getIncomeSum(data), 3000)

    def test_getOutgoSum(self):
        data = Data.getMonthData(2000, 2)
        self.assertEqual(Data.getOutgoSum(data), 2000)

    def test_getMethodData(self):
        month_data = Data.getMonthData(2000, 2)
        method_data = Data.getMethodData(month_data, 3)
        self.assertEqual(method_data.count(), 1)
        self.assertEqual(str(method_data[0]), "スーパー")

    def test_getCategoryData(self):
        start = date(2000, 1, 1)
        end = date(2000, 2, 11)
        data = Data.getRangeData(start, end)
        category_data = Data.getCategoryData(data, 1)
        self.assertEqual(category_data.count(), 2)
        self.assertEqual(str(category_data[0]), "コンビニ")
        self.assertEqual(str(category_data[1]), "スーパー")

    def test_getTempSum(self):
        data = Data.getMonthData(2000, 3)
        self.assertEqual(Data.getTempSum(data), 500)

        data = Data.getMonthData(2000, 2)
        self.assertEqual(Data.getTempSum(data), 0)

    def test_getTempAndDepositSum(self):
        data = Data.getMonthData(2000, 3)
        self.assertEqual(Data.getTempAndDepositSum(data), 1200)

        data = Data.getMonthData(2000, 2)
        self.assertEqual(Data.getTempAndDepositSum(data), 0)

    def test_getDataWithoutInmove(self):
        base_data = Data.getMonthData(2000, 4)
        data = Data.getDataWithoutInmove(base_data)
        self.assertEqual(data.count(), 3)
        self.assertEqual(str(data[0]), "必需品1")
        self.assertEqual(str(data[1]), "収入")
        self.assertEqual(str(data[2]), "計算外1")

    def test_getNormalData(self):
        base_data = Data.getMonthData(2000, 4)
        data = Data.getNormalData(base_data)
        self.assertEqual(data.count(), 2)
        self.assertEqual(str(data[0]), "必需品1")
        self.assertEqual(str(data[1]), "収入")

    def test_getLivingData(self):
        base_data = Data.getMonthData(2000, 5)
        data = Data.getLivingData(base_data)
        self.assertEqual(data.count(), 2)
        self.assertEqual(str(data[0]), "コンビニ")
        self.assertEqual(str(data[1]), "スーパー")

    def test_getVariableData(self):
        base_data = Data.getMonthData(2000, 5)
        data = Data.getVariableData(base_data)
        self.assertEqual(data.count(), 2)
        self.assertEqual(str(data[0]), "必需品1")
        self.assertEqual(str(data[1]), "収入")

    def test_getFoodCosts(self):
        data = Data.getMonthData(2000, 6)
        self.assertEqual(Data.getFoodCosts(data), 600)

    def test_sortDateAscending(self):
        data = Data.getMonthData(2000, 7)
        sorted_data = Data.sortDateAscending(data)
        self.assertEqual(sorted_data.count(), 5)
        self.assertEqual(str(sorted_data[0]), "必需品1")
        self.assertEqual(str(sorted_data[1]), "立替分")
        self.assertEqual(str(sorted_data[2]), "コンビニ")
        self.assertEqual(str(sorted_data[3]), "スーパー")
        self.assertEqual(str(sorted_data[4]), "収入")

        data = Data.getMonthData(1999, 1)
        sorted_data = Data.sortDateAscending(data)
        self.assertEqual(sorted_data.count(), 0)

    def test_sortDateDescending(self):
        data = Data.getMonthData(2000, 7)
        sorted_data = Data.sortDateDescending(data)
        self.assertEqual(sorted_data.count(), 5)
        self.assertEqual(str(sorted_data[0]), "収入")
        self.assertEqual(str(sorted_data[1]), "スーパー")
        self.assertEqual(str(sorted_data[2]), "コンビニ")
        self.assertEqual(str(sorted_data[3]), "立替分")
        self.assertEqual(str(sorted_data[4]), "必需品1")

        data = Data.getMonthData(1999, 1)
        sorted_data = Data.sortDateDescending(data)
        self.assertEqual(sorted_data.count(), 0)

    def test_getKeywordData(self):
        base_data = Data.getMonthData(2000, 7)
        data = Data.getKeywordData(base_data, "品")
        self.assertEqual(data.count(), 1)
        self.assertEqual(str(data[0]), "必需品1")

        base_data = Data.getMonthData(1999, 1)
        data = Data.getKeywordData(base_data, "品")
        self.assertEqual(data.count(), 0)
