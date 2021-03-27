from django.test import TestCase


class CommonTestCase(TestCase):
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
