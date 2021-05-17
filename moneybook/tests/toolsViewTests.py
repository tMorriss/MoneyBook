import json
from datetime import date, datetime

from django.contrib.auth.models import User
from django.urls import reverse
from moneybook.models import BankBalance, CheckedDate, CreditCheckedDate, Data, SeveralCosts
from moneybook.tests.base import BaseTestCase


class ToolsViewTests(BaseTestCase):
    def test_get(self):
        now = datetime.now()

        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:tools'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['app_name'], 'test-MoneyBook')
        self.assertEqual(response.context['username'].username, self.username)
        self.assertEqual(response.context['cash_balance'], -3930)
        self.assertEqual(response.context['year'], now.year)
        self.assertEqual(response.context['month'], now.month)
        self.assertEqual(response.context['day'], now.day)
        self.assertEqual(response.context['actual_cash_balance'], 2000)
        self._assert_list(response.context['credit_checked_date'], ['AmexGold', 'センチュリオン'])
        self.assertEqual(response.context['living_cost_mark'], 1000)
        self._assert_templates(response.templates, ['tools.html', '_base.html', '_result_message.html'])

    def test_get_guest(self):
        response = self.client.get(reverse('moneybook:tools'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('moneybook:login'))


class ActualCashViewTests(BaseTestCase):
    def test_post(self):
        self.client.force_login(User.objects.create_user(self.username))
        self.assertEqual(SeveralCosts.get_actual_cash_balance(), 2000)
        response = self.client.post(reverse('moneybook:actual_cash'), {'price': 1200})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SeveralCosts.get_actual_cash_balance(), 1200)

    def test_post_str(self):
        self.client.force_login(User.objects.create_user(self.username))
        self.assertEqual(SeveralCosts.get_actual_cash_balance(), 2000)
        response = self.client.post(reverse('moneybook:actual_cash'), {'price': 'a'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(SeveralCosts.get_actual_cash_balance(), 2000)

    def test_post_missing(self):
        self.client.force_login(User.objects.create_user(self.username))
        self.assertEqual(SeveralCosts.get_actual_cash_balance(), 2000)
        response = self.client.post(reverse('moneybook:actual_cash'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(SeveralCosts.get_actual_cash_balance(), 2000)

    def test_post_guest(self):
        self.assertEqual(SeveralCosts.get_actual_cash_balance(), 2000)
        response = self.client.post(reverse('moneybook:actual_cash'), {'price': 1200})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(SeveralCosts.get_actual_cash_balance(), 2000)


class CheckedDateViewTests(BaseTestCase):
    def test_get(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:checked_date'))
        self.assertEqual(response.status_code, 200)
        content_json = json.loads(response.content.decode())
        expects = [
            {
                'name': '銀行',
                'balance': 54054,
                'year': 2000,
                'month': 1,
                'day': 5
            },
            {
                'name': '現金',
                'balance': -3930,
                'year': 2000,
                'month': 1,
                'day': 2
            },
            {
                'name': 'PayPay',
                'balance': -1800,
                'year': 2000,
                'month': 2,
                'day': 2
            },
        ]
        self.assertEqual(len(content_json), len(expects))
        for i in range(len(expects)):
            with self.subTest(i=i):
                self.assertEqual(content_json[i]['name'], expects[i]['name'])
                self.assertEqual(content_json[i]['balance'], expects[i]['balance'])
                self.assertEqual(content_json[i]['year'], expects[i]['year'])
                self.assertEqual(content_json[i]['month'], expects[i]['month'])
                self.assertEqual(content_json[i]['day'], expects[i]['day'])

    def test_post(self):
        self.client.force_login(User.objects.create_user(self.username))
        self.assertEqual(CheckedDate.get(2).date, date(2000, 1, 5))
        unchecked_data = Data.get_unchecked_data(Data.get_all_data())
        expects = ['必需品1', 'スーパー', '計算外', '貯金', 'PayPayチャージ', '立替分1', '内部移動1', '内部移動2']
        self._assert_list(unchecked_data, expects)
        response = self.client.post(
            reverse('moneybook:checked_date'),
            {'year': 2001, 'month': 2, 'day': 20, 'method': 2}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CheckedDate.get(2).date, date(2001, 2, 20))
        unchecked_data = Data.get_unchecked_data(Data.get_all_data())
        self._assert_list(unchecked_data, expects)

    def test_post_check(self):
        self.client.force_login(User.objects.create_user(self.username))
        self.assertEqual(CheckedDate.get(2).date, date(2000, 1, 5))
        unchecked_data = Data.get_unchecked_data(Data.get_all_data())
        expects = ['必需品1', 'スーパー', '計算外', '貯金', 'PayPayチャージ', '立替分1', '内部移動1', '内部移動2']
        self._assert_list(unchecked_data, expects)

        response = self.client.post(
            reverse('moneybook:checked_date'),
            {'year': 2000, 'month': 1, 'day': 20, 'method': 2, 'check_all': 1}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CheckedDate.get(2).date, date(2000, 1, 20))
        unchecked_data = Data.get_unchecked_data(Data.get_all_data())
        expects = ['スーパー', 'PayPayチャージ', '立替分1', '内部移動1', '内部移動2']
        self._assert_list(unchecked_data, expects)

    def test_post_check_2(self):
        self.client.force_login(User.objects.create_user(self.username))
        self.assertEqual(CheckedDate.get(2).date, date(2000, 1, 5))
        unchecked_data = Data.get_unchecked_data(Data.get_all_data())
        expects = ['必需品1', 'スーパー', '計算外', '貯金', 'PayPayチャージ', '立替分1', '内部移動1', '内部移動2']
        self._assert_list(unchecked_data, expects)

        response = self.client.post(
            reverse('moneybook:checked_date'),
            {'year': 2000, 'month': 1, 'day': 20, 'method': 2, 'check_all': 2}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CheckedDate.get(2).date, date(2000, 1, 20))
        unchecked_data = Data.get_unchecked_data(Data.get_all_data())
        self._assert_list(unchecked_data, expects)

    def test_post_out_of_date_range(self):
        self.client.force_login(User.objects.create_user(self.username))
        self.assertEqual(CheckedDate.get(2).date, date(2000, 1, 5))
        unchecked_data = Data.get_unchecked_data(Data.get_all_data())
        expects = ['必需品1', 'スーパー', '計算外', '貯金', 'PayPayチャージ', '立替分1', '内部移動1', '内部移動2']
        self._assert_list(unchecked_data, expects)

        response = self.client.post(
            reverse('moneybook:checked_date'),
            {'year': 2000, 'month': 1, 'day': 40, 'method': 2}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(CheckedDate.get(2).date, date(2000, 1, 5))
        unchecked_data = Data.get_unchecked_data(Data.get_all_data())
        self._assert_list(unchecked_data, expects)

    def test_post_missing_year(self):
        self.client.force_login(User.objects.create_user(self.username))
        self.assertEqual(CheckedDate.get(2).date, date(2000, 1, 5))
        unchecked_data = Data.get_unchecked_data(Data.get_all_data())
        expects = ['必需品1', 'スーパー', '計算外', '貯金', 'PayPayチャージ', '立替分1', '内部移動1', '内部移動2']
        self._assert_list(unchecked_data, expects)

        response = self.client.post(
            reverse('moneybook:checked_date'),
            {'month': 1, 'day': 40, 'method': 2}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(CheckedDate.get(2).date, date(2000, 1, 5))
        unchecked_data = Data.get_unchecked_data(Data.get_all_data())
        self._assert_list(unchecked_data, expects)

    def test_post_missing_day(self):
        self.client.force_login(User.objects.create_user(self.username))
        self.assertEqual(CheckedDate.get(2).date, date(2000, 1, 5))
        unchecked_data = Data.get_unchecked_data(Data.get_all_data())
        expects = ['必需品1', 'スーパー', '計算外', '貯金', 'PayPayチャージ', '立替分1', '内部移動1', '内部移動2']
        self._assert_list(unchecked_data, expects)

        response = self.client.post(
            reverse('moneybook:checked_date'),
            {'year': 2000, 'month': 1, 'method': 2}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(CheckedDate.get(2).date, date(2000, 1, 5))
        unchecked_data = Data.get_unchecked_data(Data.get_all_data())
        self._assert_list(unchecked_data, expects)

    def test_post_missing_method(self):
        self.client.force_login(User.objects.create_user(self.username))
        self.assertEqual(CheckedDate.get(2).date, date(2000, 1, 5))
        unchecked_data = Data.get_unchecked_data(Data.get_all_data())
        expects = ['必需品1', 'スーパー', '計算外', '貯金', 'PayPayチャージ', '立替分1', '内部移動1', '内部移動2']
        self._assert_list(unchecked_data, expects)

        response = self.client.post(
            reverse('moneybook:checked_date'),
            {'year': 2000, 'month': 1, 'day': 20}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(CheckedDate.get(2).date, date(2000, 1, 5))
        unchecked_data = Data.get_unchecked_data(Data.get_all_data())
        self._assert_list(unchecked_data, expects)

    def test_post_str_year(self):
        self.client.force_login(User.objects.create_user(self.username))
        self.assertEqual(CheckedDate.get(2).date, date(2000, 1, 5))
        unchecked_data = Data.get_unchecked_data(Data.get_all_data())
        expects = ['必需品1', 'スーパー', '計算外', '貯金', 'PayPayチャージ', '立替分1', '内部移動1', '内部移動2']
        self._assert_list(unchecked_data, expects)

        response = self.client.post(
            reverse('moneybook:checked_date'),
            {'year': 'a', 'month': 1, 'day': 40, 'method': 2}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(CheckedDate.get(2).date, date(2000, 1, 5))
        unchecked_data = Data.get_unchecked_data(Data.get_all_data())
        self._assert_list(unchecked_data, expects)

    def test_post_str_month(self):
        self.client.force_login(User.objects.create_user(self.username))
        self.assertEqual(CheckedDate.get(2).date, date(2000, 1, 5))
        unchecked_data = Data.get_unchecked_data(Data.get_all_data())
        expects = ['必需品1', 'スーパー', '計算外', '貯金', 'PayPayチャージ', '立替分1', '内部移動1', '内部移動2']
        self._assert_list(unchecked_data, expects)

        response = self.client.post(
            reverse('moneybook:checked_date'),
            {'year': 2000, 'month': 'a', 'day': 40, 'method': 2}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(CheckedDate.get(2).date, date(2000, 1, 5))
        unchecked_data = Data.get_unchecked_data(Data.get_all_data())
        self._assert_list(unchecked_data, expects)

    def test_post_str_day(self):
        self.client.force_login(User.objects.create_user(self.username))
        self.assertEqual(CheckedDate.get(2).date, date(2000, 1, 5))
        unchecked_data = Data.get_unchecked_data(Data.get_all_data())
        expects = ['必需品1', 'スーパー', '計算外', '貯金', 'PayPayチャージ', '立替分1', '内部移動1', '内部移動2']
        self._assert_list(unchecked_data, expects)

        response = self.client.post(
            reverse('moneybook:checked_date'),
            {'year': 2000, 'month': 1, 'day': 'a', 'method': 2}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(CheckedDate.get(2).date, date(2000, 1, 5))
        unchecked_data = Data.get_unchecked_data(Data.get_all_data())
        self._assert_list(unchecked_data, expects)

    def test_post_not_exist(self):
        self.client.force_login(User.objects.create_user(self.username))
        self.assertEqual(CheckedDate.get(2).date, date(2000, 1, 5))
        unchecked_data = Data.get_unchecked_data(Data.get_all_data())
        expects = ['必需品1', 'スーパー', '計算外', '貯金', 'PayPayチャージ', '立替分1', '内部移動1', '内部移動2']
        self._assert_list(unchecked_data, expects)

        response = self.client.post(
            reverse('moneybook:checked_date'),
            {'year': 2000, 'month': 1, 'day': 20, 'method': 1000000}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(CheckedDate.get(2).date, date(2000, 1, 5))
        unchecked_data = Data.get_unchecked_data(Data.get_all_data())
        self._assert_list(unchecked_data, expects)

    def test_post_guest(self):
        self.assertEqual(CheckedDate.get(2).date, date(2000, 1, 5))
        unchecked_data = Data.get_unchecked_data(Data.get_all_data())
        expects = ['必需品1', 'スーパー', '計算外', '貯金', 'PayPayチャージ', '立替分1', '内部移動1', '内部移動2']
        self._assert_list(unchecked_data, expects)
        response = self.client.post(
            reverse('moneybook:checked_date'),
            {'year': 2001, 'month': 2, 'day': 20, 'method': 2}
        )
        self.assertEqual(response.status_code, 403)

        self.assertEqual(CheckedDate.get(2).date, date(2000, 1, 5))
        unchecked_data = Data.get_unchecked_data(Data.get_all_data())
        self._assert_list(unchecked_data, expects)


class SeveralCheckedDateViewTests(BaseTestCase):
    def test_get(self):
        now = datetime.now()
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:several_checked_date'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['year'], now.year)

        banks = response.context['banks']
        self.assertEqual(banks.count(), 2)
        self.assertEqual(banks[0].name, '三井住友')
        self.assertEqual(banks[0].price, 20000)
        self.assertEqual(banks[1].name, 'みずほ')
        self.assertEqual(banks[1].price, 40000)

        credit_checked_date = response.context['credit_checked_date']
        self.assertEqual(credit_checked_date.count(), 2)
        amex_gold = credit_checked_date[0]
        self.assertEqual(amex_gold.name, 'AmexGold')
        self.assertEqual(amex_gold.date, date(2000, 2, 4))
        self.assertEqual(amex_gold.price, 0)
        centurion = credit_checked_date[1]
        self.assertEqual(centurion.name, 'センチュリオン')
        self.assertEqual(centurion.date, date(3000, 1, 1))
        self.assertEqual(centurion.price, 30000)

        self.assertEqual(response.context['bank_written'], 54054)

        self._assert_templates(
            response.templates,
            ['_several_checked_date.html']
        )

    def test_get_guest(self):
        response = self.client.post(reverse('moneybook:several_checked_date'))
        self.assertEqual(response.status_code, 403)


class CreditCheckedDateViewTests(BaseTestCase):
    def test_post(self):
        self.client.force_login(User.objects.create_user(self.username))
        d = CreditCheckedDate.objects.get(pk=2)
        self.assertEqual(d.name, 'AmexGold')
        self.assertEqual(d.date, date(2000, 2, 4))
        self.assertEqual(d.price, 2000)

        response = self.client.post(
            reverse('moneybook:credit_checked_date'),
            {'year': 2001, 'month': 3, 'day': 10, 'pk': 2}
        )
        self.assertEqual(response.status_code, 200)
        d = CreditCheckedDate.objects.get(pk=2)
        self.assertEqual(d.name, 'AmexGold')
        self.assertEqual(d.date, date(2001, 3, 10))
        self.assertEqual(d.price, 2000)

    def test_post_missing_year(self):
        self.client.force_login(User.objects.create_user(self.username))
        d = CreditCheckedDate.objects.get(pk=2)
        self.assertEqual(d.name, 'AmexGold')
        self.assertEqual(d.date, date(2000, 2, 4))
        self.assertEqual(d.price, 2000)

        response = self.client.post(
            reverse('moneybook:credit_checked_date'),
            {'month': 3, 'day': 10, 'pk': 2}
        )
        self.assertEqual(response.status_code, 400)
        d = CreditCheckedDate.objects.get(pk=2)
        self.assertEqual(d.name, 'AmexGold')
        self.assertEqual(d.date, date(2000, 2, 4))
        self.assertEqual(d.price, 2000)

    def test_post_missing_month(self):
        self.client.force_login(User.objects.create_user(self.username))
        d = CreditCheckedDate.objects.get(pk=2)
        self.assertEqual(d.name, 'AmexGold')
        self.assertEqual(d.date, date(2000, 2, 4))
        self.assertEqual(d.price, 2000)

        response = self.client.post(
            reverse('moneybook:credit_checked_date'),
            {'year': 2001, 'day': 10, 'pk': 2}
        )
        self.assertEqual(response.status_code, 400)
        d = CreditCheckedDate.objects.get(pk=2)
        self.assertEqual(d.name, 'AmexGold')
        self.assertEqual(d.date, date(2000, 2, 4))
        self.assertEqual(d.price, 2000)

    def test_post_missing_day(self):
        self.client.force_login(User.objects.create_user(self.username))
        d = CreditCheckedDate.objects.get(pk=2)
        self.assertEqual(d.name, 'AmexGold')
        self.assertEqual(d.date, date(2000, 2, 4))
        self.assertEqual(d.price, 2000)

        response = self.client.post(
            reverse('moneybook:credit_checked_date'),
            {'year': 2001, 'month': 3, 'pk': 2}
        )
        self.assertEqual(response.status_code, 400)
        d = CreditCheckedDate.objects.get(pk=2)
        self.assertEqual(d.name, 'AmexGold')
        self.assertEqual(d.date, date(2000, 2, 4))
        self.assertEqual(d.price, 2000)

    def test_post_missing_pk(self):
        self.client.force_login(User.objects.create_user(self.username))
        d = CreditCheckedDate.objects.get(pk=2)
        self.assertEqual(d.name, 'AmexGold')
        self.assertEqual(d.date, date(2000, 2, 4))
        self.assertEqual(d.price, 2000)

        response = self.client.post(
            reverse('moneybook:credit_checked_date'),
            {'year': 2001, 'month': 3, 'day': 10}
        )
        self.assertEqual(response.status_code, 400)
        d = CreditCheckedDate.objects.get(pk=2)
        self.assertEqual(d.name, 'AmexGold')
        self.assertEqual(d.date, date(2000, 2, 4))
        self.assertEqual(d.price, 2000)

    def test_post_str_year(self):
        self.client.force_login(User.objects.create_user(self.username))
        d = CreditCheckedDate.objects.get(pk=2)
        self.assertEqual(d.name, 'AmexGold')
        self.assertEqual(d.date, date(2000, 2, 4))
        self.assertEqual(d.price, 2000)

        response = self.client.post(
            reverse('moneybook:credit_checked_date'),
            {'year': 'a', 'month': 3, 'day': 10, 'pk': 2}
        )
        self.assertEqual(response.status_code, 400)
        d = CreditCheckedDate.objects.get(pk=2)
        self.assertEqual(d.name, 'AmexGold')
        self.assertEqual(d.date, date(2000, 2, 4))
        self.assertEqual(d.price, 2000)

    def test_post_invalid_pk(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.post(
            reverse('moneybook:credit_checked_date'),
            {'year': 2001, 'month': 3, 'day': 10, 'pk': 1000000}
        )
        self.assertEqual(response.status_code, 400)

    def test_post_guest(self):
        d = CreditCheckedDate.objects.get(pk=2)
        self.assertEqual(d.name, 'AmexGold')
        self.assertEqual(d.date, date(2000, 2, 4))
        self.assertEqual(d.price, 2000)
        response = self.client.post(
            reverse('moneybook:credit_checked_date'),
            {'year': 2001, 'month': 3, 'day': 10, 'pk': 2}
        )
        self.assertEqual(response.status_code, 403)
        d = CreditCheckedDate.objects.get(pk=2)
        self.assertEqual(d.name, 'AmexGold')
        self.assertEqual(d.date, date(2000, 2, 4))
        self.assertEqual(d.price, 2000)


class LivingCostMarkViewTests(BaseTestCase):
    def test_post(self):
        self.client.force_login(User.objects.create_user(self.username))
        self.assertEqual(SeveralCosts.get_living_cost_mark(), 1000)
        response = self.client.post(
            reverse('moneybook:living_cost_mark'),
            {'price': 2000}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SeveralCosts.get_living_cost_mark(), 2000)

    def test_post_missing_price(self):
        self.client.force_login(User.objects.create_user(self.username))
        self.assertEqual(SeveralCosts.get_living_cost_mark(), 1000)
        response = self.client.post(reverse('moneybook:living_cost_mark'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(SeveralCosts.get_living_cost_mark(), 1000)

    def test_post_str_price(self):
        self.client.force_login(User.objects.create_user(self.username))
        self.assertEqual(SeveralCosts.get_living_cost_mark(), 1000)
        response = self.client.post(
            reverse('moneybook:living_cost_mark'),
            {'price': 'a'}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(SeveralCosts.get_living_cost_mark(), 1000)

    def test_post_guest(self):
        self.assertEqual(SeveralCosts.get_living_cost_mark(), 1000)
        response = self.client.post(
            reverse('moneybook:living_cost_mark'),
            {'price': 2000}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(SeveralCosts.get_living_cost_mark(), 1000)


class UncheckedDataViewTests(BaseTestCase):
    def test_get(self):
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.get(reverse('moneybook:unchecked_data'))
        self.assertEqual(response.status_code, 200)
        expects = ['必需品1', 'スーパー', '計算外', '貯金', 'PayPayチャージ', '立替分1', '内部移動1', '内部移動2']
        self._assert_list(response.context['unchecked_data'], expects)
        self._assert_templates(
            response.templates,
            ['_unchecked_data.html']
        )

    def test_get_guest(self):
        response = self.client.get(reverse('moneybook:unchecked_data'))
        self.assertEqual(response.status_code, 403)


class NowBankViewTests(BaseTestCase):
    def test_post(self):
        self.assertEqual(BankBalance.get_price(1), 40000)
        self.assertEqual(BankBalance.get_price(2), 20000)
        self.assertEqual(CreditCheckedDate.get_price(1), 30000)
        self.assertEqual(CreditCheckedDate.get_price(2), 2000)
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.post(
            reverse('moneybook:now_bank'),
            {'bank-1': 50000, 'bank-2': 10000, 'credit-1': 20000, 'credit-2': 3000}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(BankBalance.get_price(1), 50000)
        self.assertEqual(BankBalance.get_price(2), 10000)
        self.assertEqual(CreditCheckedDate.get_price(1), 20000)
        self.assertEqual(CreditCheckedDate.get_price(2), 3000)
        response_json = json.loads(response.content.decode())
        self.assertEqual(response_json['balance'], 54054 - (50000 + 10000 - 20000 - 3000))

    def test_post_part(self):
        self.assertEqual(BankBalance.get_price(1), 40000)
        self.assertEqual(BankBalance.get_price(2), 20000)
        self.assertEqual(CreditCheckedDate.get_price(1), 30000)
        self.assertEqual(CreditCheckedDate.get_price(2), 2000)
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.post(
            reverse('moneybook:now_bank'),
            {'bank-1': 50000, 'credit-2': 3000}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(BankBalance.get_price(1), 50000)
        self.assertEqual(BankBalance.get_price(2), 20000)
        self.assertEqual(CreditCheckedDate.get_price(1), 30000)
        self.assertEqual(CreditCheckedDate.get_price(2), 3000)
        response_json = json.loads(response.content.decode())
        self.assertEqual(response_json['balance'], 54054 - (50000 + 20000 - 30000 - 3000))

    def test_post_empty(self):
        self.assertEqual(BankBalance.get_price(1), 40000)
        self.assertEqual(BankBalance.get_price(2), 20000)
        self.assertEqual(CreditCheckedDate.get_price(1), 30000)
        self.assertEqual(CreditCheckedDate.get_price(2), 2000)
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.post(reverse('moneybook:now_bank'))
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content.decode())
        self.assertEqual(response_json['balance'], 54054 - (40000 + 20000 - 30000 - 2000))
        self.assertEqual(BankBalance.get_price(1), 40000)
        self.assertEqual(BankBalance.get_price(2), 20000)
        self.assertEqual(CreditCheckedDate.get_price(1), 30000)
        self.assertEqual(CreditCheckedDate.get_price(2), 2000)

    def test_post_str_bank(self):
        self.assertEqual(BankBalance.get_price(1), 40000)
        self.assertEqual(BankBalance.get_price(2), 20000)
        self.assertEqual(CreditCheckedDate.get_price(1), 30000)
        self.assertEqual(CreditCheckedDate.get_price(2), 2000)
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.post(
            reverse('moneybook:now_bank'),
            {'bank-1': 'a', 'bank-2': 10000, 'credit-1': 20000, 'credit-2': 3000}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(BankBalance.get_price(1), 40000)
        self.assertEqual(BankBalance.get_price(2), 20000)
        self.assertEqual(CreditCheckedDate.get_price(1), 30000)
        self.assertEqual(CreditCheckedDate.get_price(2), 2000)

    def test_post_str_credit(self):
        self.assertEqual(BankBalance.get_price(1), 40000)
        self.assertEqual(BankBalance.get_price(2), 20000)
        self.assertEqual(CreditCheckedDate.get_price(1), 30000)
        self.assertEqual(CreditCheckedDate.get_price(2), 2000)
        self.client.force_login(User.objects.create_user(self.username))
        response = self.client.post(
            reverse('moneybook:now_bank'),
            {'bank-1': 50000, 'bank-2': 10000, 'credit-1': 'a', 'credit-2': 3000}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(BankBalance.get_price(1), 40000)
        self.assertEqual(BankBalance.get_price(2), 20000)
        self.assertEqual(CreditCheckedDate.get_price(1), 30000)
        self.assertEqual(CreditCheckedDate.get_price(2), 2000)

    def test_post_guest(self):
        self.assertEqual(BankBalance.get_price(1), 40000)
        self.assertEqual(BankBalance.get_price(2), 20000)
        self.assertEqual(CreditCheckedDate.get_price(1), 30000)
        self.assertEqual(CreditCheckedDate.get_price(2), 2000)
        response = self.client.post(
            reverse('moneybook:now_bank'),
            {'bank-1': 50000, 'bank-2': 10000, 'credit-1': 20000, 'credit-2': 3000}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(BankBalance.get_price(1), 40000)
        self.assertEqual(BankBalance.get_price(2), 20000)
        self.assertEqual(CreditCheckedDate.get_price(1), 30000)
        self.assertEqual(CreditCheckedDate.get_price(2), 2000)
