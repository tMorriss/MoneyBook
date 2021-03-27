from datetime import datetime
from unittest.mock import patch

from django.contrib.auth.models import User
from django.urls import reverse
from moneybook.tests.commonTests import CommonTestCase
from moneybook.views import indexView


class IndexViewTestCase(CommonTestCase):
    fixtures = ['data_test_case']
    username = 'tester'

    @patch.object(indexView, 'index_month', return_value=True)
    def test_index(self, index_month):
        now = datetime.now()
        self.client.get(reverse('moneybook:index'))
        request, year, month = indexView.index_month.call_args.args
        self.assertEqual(year, now.year)
        self.assertEqual(month, now.month)

    def test_index_guest(self):
        response = self.client.get(reverse('moneybook:index'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:login'))

    def test_index_month(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:index_month', kwargs={'year': 2000, 'month': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['app_name'], 'test-MoneyBook')
        self.assertEqual(
            response.context['username'].username, self.username)
        self.assertEqual(response.context['year'], 2000)
        self.assertEqual(response.context['month'], 1)
        self.assertEqual(response.context['next_year'], 2000)
        self.assertEqual(response.context['next_month'], 2)
        self.assertEqual(response.context['last_year'], 1999)
        self.assertEqual(response.context['last_month'], 12)
        data = response.context['directions']
        expects = ['収入', '支出']
        self.__assert_list(data, expects)
        data = response.context['methods']
        expects = ['銀行', "現金", "PayPay"]
        self.__assert_list(data, expects)
        data = response.context['unused_methods']
        expects = ['nanaco']
        self.__assert_list(data, expects)
        data = response.context['first_categories']
        expects = ['食費', '必需品']
        self.__assert_list(data, expects)
        data = response.context['latter_categories']
        expects = ['その他', '内部移動', '貯金', '計算外']
        self.__assert_list(data, expects)

        expects = [
            'index.html',
            '_base.html',
            '_add_mini.html',
            '_filter_mini.html',
            '_result_message.html'
        ]
        self.__assert_templates(response.templates, expects)

    def test_index_month_out_of_range(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:index_month', kwargs={'year': 2000, 'month': 13}))
        self.assertEqual(response.status_code, 400)

    def test_index_month_guest(self):
        response = self.client.get(
            reverse('moneybook:index_month', kwargs={'year': 2000, 'month': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:login'))

    def test_index_balance_statistic_mini(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:balance_statistic_mini'),
            {'year': 2000, 'month': 1}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_balance'], -360)
        self.assertEqual(response.context['monthly_income'], 7870)
        self.assertEqual(response.context['monthly_outgo'], 6430)
        self.assertEqual(response.context['monthly_inout'], 1440)
        self.assertEqual(response.context['variable_cost'], 3900)
        self.assertEqual(response.context['living_cost'], 2500)
        self.assertEqual(
            response.context['variable_remain'], 7870 - 2500 - 3900)
        self.assertEqual(response.context['all_income'], 9000)
        self.assertEqual(response.context['all_outgo'], 8060)

        expects = [
            {
                'label': '銀行',
                'balance': 4970
            },
            {
                'label': '現金',
                'balance': -3930
            },
            {
                'label': 'PayPay',
                'balance': -1400
            }
        ]
        iobs = response.context['methods_iob']
        for i in range(len(iobs)):
            with self.subTest(i=i):
                self.assertEqual(iobs[i].label, expects[i]['label'])
                self.assertEqual(iobs[i].balance, expects[i]['balance'])

        expects = [
            {
                'label': '銀行',
                'income': 6600,
                'outgo': 1630
            },
            {
                'label': '現金',
                'income': 3000,
                'outgo': 6430
            },
            {
                'label': 'PayPay',
                'income': 400,
                'outgo': 1000
            }
        ]
        iobs = response.context['methods_monthly_iob']
        for i in range(len(iobs)):
            with self.subTest(i=i):
                self.assertEqual(iobs[i].label, expects[i]['label'])
                self.assertEqual(iobs[i].income, expects[i]['income'])
                self.assertEqual(iobs[i].outgo, expects[i]['outgo'])

        expects = ['_balance_statistic_mini.html']
        self.__assert_templates(response.templates, expects)

    def test_index_balance_statistic_mini_without_year(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:balance_statistic_mini'),
            {'month': 1}
        )
        self.assertEqual(response.status_code, 400)

    def test_index_balance_statistic_mini_without_month(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:balance_statistic_mini'),
            {'year': 2000}
        )
        self.assertEqual(response.status_code, 400)

    def test_index_balance_statistic_mini_out_of_range(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:balance_statistic_mini'),
            {'year': 2000, 'month': 13}
        )
        self.assertEqual(response.status_code, 400)

    def test_index_balance_statistic_mini_without_parameters(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:balance_statistic_mini'))
        self.assertEqual(response.status_code, 400)

    def test_index_balance_statistic_mini_guest(self):
        response = self.client.get(
            reverse('moneybook:balance_statistic_mini'),
            {'year': 2000, 'month': 1}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:login'))

    def test_index_chart_data(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:chart_container_data'),
            {'year': 2000, 'month': 1}
        )
        self.assertEqual(response.status_code, 200)
        positive_categories_outgo = response.context['categories_outgo']
        actials = [
            {'name': 'その他', 'value': 30},
            {'name': '食費', 'value': 2500},
            {'name': '必需品', 'value': 3900}
        ]
        keys = list(positive_categories_outgo.keys())
        for i in range(len(keys)):
            self.assertEqual(keys[i], actials[i]['name'])
            self.assertEqual(
                positive_categories_outgo[keys[i]], actials[i]['value'])

    def test_index_chart_data_wituout_year(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:chart_container_data'),
            {'month': 1}
        )
        self.assertEqual(response.status_code, 400)

    def test_index_chart_data_wituout_month(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:chart_container_data'),
            {'year': 2000}
        )
        self.assertEqual(response.status_code, 400)

    def test_index_chart_data_without_parameters(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:chart_container_data'))
        self.assertEqual(response.status_code, 400)

    def test_index_chart_data_out_of_range(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:chart_container_data'),
            {'year': 2000, 'month': 13}
        )
        self.assertEqual(response.status_code, 400)

    def test_data_table(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:data_table'),
            {'year': 2000, 'month': 1}
        )
        self.assertEqual(response.status_code, 200)
        expects = [
            "立替分2",
            "立替分1",
            "PayPayチャージ",
            "PayPayチャージ",
            "貯金",
            "計算外",
            "スーパー",
            "銀行収入",
            "現金収入",
            "必需品2",
            "必需品1",
            "その他1",
            "コンビニ"
        ]
        data = response.context['show_data']
        self.assertEqual(data.count(), len(expects))
        for i in range(len(expects)):
            with self.subTest(i=i):
                self.assertEqual(str(data[i]), expects[i])

    def test_data_table_without_year(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:data_table'),
            {'month': 1}
        )
        self.assertEqual(response.status_code, 400)

    def test_data_table_without_month(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:data_table'),
            {'year': 2000}
        )
        self.assertEqual(response.status_code, 400)

    def test_data_table_without_parameters(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:data_table'))
        self.assertEqual(response.status_code, 400)

    def test_data_table_out_of_range(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(
            reverse('moneybook:data_table'),
            {'year': 2000, 'month': 13}
        )
        self.assertEqual(response.status_code, 400)
