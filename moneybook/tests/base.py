from django.test import TestCase


class BaseTestCase(TestCase):
    fixtures = ['data_test_case']
    username = 'tester'

    def _assert_list(self, data, expects):
        self.assertEqual(data.count(), len(expects))
        for i in range(len(expects)):
            with self.subTest(i=i):
                self.assertEqual(str(data[i]), expects[i])

    def _assert_templates(self, templates, expects):
        self.assertEqual(len(templates), len(expects))
        for i in range(len(expects)):
            with self.subTest(i=i):
                self.assertEqual(templates[i].name, expects[i])

    def _assert_all_directions(self, response):
        data = response.context['directions']
        expects = ['収入', '支出']
        self._assert_list(data, expects)

    def _assert_all_methods(self, response):
        data = response.context['methods']
        expects = ['銀行', '現金', 'Kyash', 'PayPay']
        self._assert_list(data, expects)

    def _assert_all_unused_methods(self, response):
        data = response.context['unused_methods']
        expects = ['nanaco', 'Edy']
        self._assert_list(data, expects)

    def _assert_all_chargeable_methods(self, response):
        data = response.context['chargeable_methods']
        expects = ['Kyash', 'PayPay']
        self._assert_list(data, expects)

    def _assert_all_first_categories(self, response):
        data = response.context['first_categories']
        expects = ['食費', '必需品', '交通費']
        self._assert_list(data, expects)

    def _assert_all_latter_categories(self, response):
        data = response.context['latter_categories']
        expects = ['その他', '内部移動', '貯金', '計算外', '収入']
        self._assert_list(data, expects)

    def _assert_all_temps(self, response):
        data = response.context['temps']
        self.assertEqual(data, {0: "No", 1: "Yes"})

    def _assert_all_checkeds(self, response):
        data = response.context['checkeds']
        self.assertEqual(data, {0: "No", 1: "Yes"})
