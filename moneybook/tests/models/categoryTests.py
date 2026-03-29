from moneybook.models import Category
from moneybook.tests.base import BaseTestCase


class CategoryTestCase(BaseTestCase):
    def test_get(self):
        self.assertEqual(str(Category.get(1)), '食費')
        self.assertEqual(str(Category.get(4)), '内部移動')

    def test_list(self):
        ls = Category.list()
        expects = ['収入', '計算外', '貯金', '内部移動', 'その他', '食費', '必需品', '交通費']
        self._assert_list(ls, expects)

    def test_first_list(self):
        ls = Category.first_list()
        expects = ['食費', '必需品', '交通費']
        self._assert_list(ls, expects)

    def test_latter_list(self):
        ls = Category.latter_list()
        expects = ['その他', '内部移動', '貯金', '計算外', '収入']
        self._assert_list(ls, expects)
