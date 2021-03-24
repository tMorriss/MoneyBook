from django.test import TestCase


class CommonTestCase(TestCase):
    def _assert_list(self, data, actuals):
        self.assertEqual(data.count(), len(actuals))
        for i in range(len(actuals)):
            with self.subTest(i=i):
                self.assertEqual(str(data[i]), actuals[i])

    def _assert_templates(self, templates, actuals):
        self.assertEqual(len(templates), len(actuals))
        for i in range(len(actuals)):
            with self.subTest(i=i):
                self.assertEqual(templates[i].name, actuals[i])
