import time
from datetime import datetime

from django.urls import reverse
from moneybook.selenium.base import SeleniumBase
from selenium.webdriver.common.keys import Keys


class Index(SeleniumBase):
    def _test_initialzed_add_mini(self, year, month):
        '''入力欄が初期値であることを確認'''
        self.assertEqual(self.driver.find_element_by_id('a_year').get_attribute('value'), str(year))
        self.assertEqual(self.driver.find_element_by_id('a_month').get_attribute('value'), str(month))
        self.assertEqual(self.driver.find_element_by_id('a_day').get_attribute('value'), '')
        self.assertEqual(self.driver.find_element_by_id('a_item').get_attribute('value'), '')
        self.assertEqual(self.driver.find_element_by_id('a_price').get_attribute('value'), '')
        self.assertTrue(self.driver.find_element_by_xpath('//*[@id="filter-fixed"]/form/table/tbody/tr[4]/td/input[1]').is_selected())
        self.assertTrue(self.driver.find_element_by_xpath(
            '//*[@id="filter-fixed"]/form/table/tbody/tr[5]/td/table/tbody/tr[1]/td/input[1]').is_selected())
        self.assertFalse(self.driver.find_element_by_id('lbl_is-charge').is_selected())

    def _test_add(self, item, method, category):
        now = datetime.now()
        self._login()
        self.driver.get(self.live_server_url + reverse('moneybook:index'))

        self.assertEqual(len(self.driver.find_elements_by_xpath('//*[@id="transactions"]/table/tbody/tr')), 1)

        # 1件追加
        self.driver.find_element_by_id('a_day').send_keys('3')
        self.driver.find_element_by_id('a_item').send_keys(item)
        self.driver.find_element_by_id('a_price').send_keys('1000')
        labels = self.driver.find_elements_by_xpath('//*[@id="filter-fixed"]/form/table/tbody/tr[4]/td/label')
        for label in labels:
            if label.text == method:
                label.click()
                break
        labels = self.driver.find_elements_by_xpath('//*[@id="filter-fixed"]/form/table/tbody/tr[5]/td/table/tbody/tr/td/label')
        for label in labels:
            if label.text == category:
                label.click()
                break
        self.driver.find_element_by_xpath('//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        rows = self.driver.find_elements_by_xpath('//*[@id="transactions"]/table/tbody/tr')
        self.assertEqual(len(rows), 2)
        tds = rows[1].find_elements_by_tag_name('td')
        self.assertEqual(tds[0].text, str(now.year) + "/" + str.zfill(str(now.month), 2) + "/" + '03')
        self.assertEqual(tds[1].text, item)
        self.assertEqual(tds[2].text, '1,000')
        self.assertEqual(tds[3].text, method)
        self.assertEqual(tds[4].text, category)

        # 入力欄が戻っていることを確認
        self._test_initialzed_add_mini(now.year, now.month)

    def _test_invalid_add(self, year, month, day, item, price):
        self._login()
        self.driver.get(self.live_server_url + reverse('moneybook:index'))

        self.assertEqual(len(self.driver.find_elements_by_xpath('//*[@id="transactions"]/table/tbody/tr')), 1)

        # 1件追加
        self.driver.find_element_by_id('a_year').clear()
        self.driver.find_element_by_id('a_year').send_keys(year)
        self.driver.find_element_by_id('a_month').clear()
        self.driver.find_element_by_id('a_month').send_keys(month)
        self.driver.find_element_by_id('a_day').send_keys(day)
        self.driver.find_element_by_id('a_item').send_keys(item)
        self.driver.find_element_by_id('a_price').send_keys(price)
        self.driver.find_element_by_xpath('//*[@id="filter-fixed"]/form/table/tbody/tr[4]/td/label[2]').click()
        self.driver.find_element_by_xpath('//*[@id="filter-fixed"]/form/table/tbody/tr[5]/td/table/tbody/tr/td/label[2]').click()
        self.driver.find_element_by_xpath('//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 入力欄がそのままであることを確認
        self.assertEqual(self.driver.find_element_by_id('a_year').get_attribute('value'), str(year))
        self.assertEqual(self.driver.find_element_by_id('a_month').get_attribute('value'), str(month))
        self.assertEqual(self.driver.find_element_by_id('a_day').get_attribute('value'), str(day))
        self.assertEqual(self.driver.find_element_by_id('a_item').get_attribute('value'), str(item))
        self.assertEqual(self.driver.find_element_by_id('a_price').get_attribute('value'), str(price))

        # 追加されていないことを確認
        self.assertEqual(len(self.driver.find_elements_by_xpath('//*[@id="transactions"]/table/tbody/tr')), 1)

    def _test_index_date(self, year, month):
        self._assert_common()

        self.assertEqual(self.driver.find_element_by_id('a_year').get_attribute('value'), str(year))
        self.assertEqual(self.driver.find_element_by_id('a_month').get_attribute('value'), str(month))
        self.assertEqual(self.driver.find_element_by_id('a_day').get_attribute('value'), '')

        self.assertEqual(self.driver.find_element_by_id('jump_year').get_attribute('value'), str(year))
        self.assertEqual(self.driver.find_element_by_id('jump_month').get_attribute('value'), str(month))

    def test_index(self):
        self._login()
        self.driver.get(self.live_server_url + reverse('moneybook:index'))

        # 日付だけ確認
        now = datetime.now()
        self._test_index_date(now.year, now.month)

    def test_index_month(self):
        self._login()
        self.driver.get(self.live_server_url + reverse('moneybook:index_month', kwargs={'year': 2000, 'month': 1}))
        self._assert_common()

        # 追加部分
        self._test_initialzed_add_mini(2000, 1)

        expects = ['銀行', '現金', 'PayPay']
        actuals = self.driver.find_elements_by_xpath('//*[@id="filter-fixed"]/form/table/tbody/tr[4]/td/label')
        self._assert_texts(actuals, expects)

        expects = ['食費', '必需品']
        actuals = self.driver.find_elements_by_xpath('//*[@id="filter-fixed"]/form/table/tbody/tr[5]/td/table/tbody/tr[1]/td/label')
        self._assert_texts(actuals, expects)
        expects = ['その他', '内部移動', '貯金', '計算外']
        actuals = self.driver.find_elements_by_xpath('//*[@id="filter-fixed"]/form/table/tbody/tr[5]/td/table/tbody/tr[2]/td/label')
        self._assert_texts(actuals, expects)

        # フィルタ
        self.assertEqual(
            self.driver.find_element_by_xpath(
                '//*[@id="filter-fixed"]/table[1]/tbody/tr[1]/td[1]/table/tbody/tr[1]/td[1]/a'
            ).get_attribute('href'),
            self.live_server_url + reverse('moneybook:index_month', kwargs={'year': 1999, 'month': 12})
        )
        self.assertEqual(
            self.driver.find_element_by_xpath(
                '//*[@id="filter-fixed"]/table[1]/tbody/tr[1]/td[1]/table/tbody/tr[1]/td[3]/a'
            ).get_attribute('href'),
            self.live_server_url + reverse('moneybook:index_month', kwargs={'year': 2000, 'month': 2})
        )
        self.assertEqual(self.driver.find_element_by_id('jump_year').get_attribute('value'), '2000')
        self.assertEqual(self.driver.find_element_by_id('jump_month').get_attribute('value'), '1')
        self.assertEqual(self.driver.find_element_by_id('filter-item').get_attribute('value'), '')
        expects = ['収入', '支出']
        actuals = self.driver.find_elements_by_xpath('//*[@id="filter-fixed"]/table[1]/tbody/tr[2]/td[1]/table/tbody/tr[2]/td/label')
        self._assert_texts(actuals, expects)
        inputs = self.driver.find_elements_by_xpath('//*[@id="filter-fixed"]/table[1]/tbody/tr[2]/td[1]/table/tbody/tr[2]/td/input')
        for i in inputs:
            self.assertTrue(i.is_selected())
        expects = ['銀行', '現金', 'PayPay', 'nanaco', 'Edy']
        actuals = self.driver.find_elements_by_xpath('//*[@id="filter-fixed"]/table[1]/tbody/tr[2]/td[1]/table/tbody/tr[3]/td/label')
        self._assert_texts(actuals, expects)
        actuals = self.driver.find_elements_by_xpath('//*[@id="filter-fixed"]/table[1]/tbody/tr[2]/td[1]/table/tbody/tr[3]/td/input')
        for i in inputs:
            self.assertTrue(i.is_selected())
        expects = ['食費', '必需品', 'その他', '内部移動', '貯金', '計算外']
        actuals = self.driver.find_elements_by_xpath('//*[@id="filter-fixed"]/table[1]/tbody/tr[2]/td[1]/table/tbody/tr[4]/td/label')
        self._assert_texts(actuals, expects)
        actuals = self.driver.find_elements_by_xpath('//*[@id="filter-fixed"]/table[1]/tbody/tr[2]/td[1]/table/tbody/tr[4]/td/input')
        for i in inputs:
            self.assertTrue(i.is_selected())

        # 一覧表示
        expects = ["立替分2", "立替分1", "水道代", "ガス代", "電気代", "PayPayチャージ", "PayPayチャージ",
                   "貯金", "計算外", "スーパー", "銀行収入", "現金収入", "必需品2", "必需品1", "その他1", "コンビニ", "給与"]
        actuals = self.driver.find_elements_by_class_name('data_item')
        self._assert_texts(actuals, expects)

        # 残高
        self.assertEqual(self.driver.find_element_by_xpath('//*[@id="statistic-fixed"]/table[1]/tbody/tr/td[2]').text, '46,694円')
        expects = ['銀行', '現金', 'PayPay']
        actuals = self.driver.find_elements_by_xpath('//*[@id="statistic-fixed"]/table[2]/tbody/tr[1]/th')
        self._assert_texts(actuals, expects)
        expects = ['52,424円', '-3,930円', '-1,800円']
        actuals = self.driver.find_elements_by_xpath('//*[@id="statistic-fixed"]/table[2]/tbody/tr[2]/td')
        self._assert_texts(actuals, expects)

        # 統計
        actuals = self.driver.find_elements_by_xpath('//*[@id="chart_container_data"]/ul[@id="chart_data"]/li')
        expects = [
            {'name': 'その他', 'price': '30'},
            {'name': '食費', 'price': '2500'},
            {'name': '必需品', 'price': '5390'}
        ]
        self.assertEqual(len(actuals), len(expects))
        for i in range(len(actuals)):
            with self.subTest(i=i):
                parts = actuals[i].get_attribute('innerHTML').split(',')
                self.assertEqual(parts[0], expects[i]['name'])
                self.assertEqual(parts[1], expects[i]['price'])

        actuals = self.driver.find_elements_by_xpath('//*[@id="statistic-fixed"]/table[3]/tbody/tr')
        expects = [
            {'title': '収入合計', 'value': '32,993'},
            {'title': '支出合計', 'value': '7,920'},
            {'title': '収支', 'value': '+25,073'},
            {'title': '生活費', 'value': '2,500'},
            {'title': '変動費', 'value': '5,390'},
            {'title': '生活費残額', 'value': '-1,500'},
            {'title': '変動残額', 'value': '25,103'},
            {'title': '全収入', 'value': '34,123'},
            {'title': '全支出', 'value': '9,550'}
        ]
        for i in range(len(actuals)):
            with self.subTest(i=i):
                self.assertEqual(actuals[i].find_element_by_tag_name('th').text, expects[i]['title'])
                self.assertEqual(actuals[i].find_element_by_tag_name('td').text, expects[i]['value'])

        actuals = self.driver.find_elements_by_xpath('//*[@id="statistic-fixed"]/table[4]/tbody/tr[1]/th')
        expects = ['', '銀行', '現金', 'PayPay']
        self._assert_texts(actuals, expects)
        actuals = self.driver.find_elements_by_xpath('//*[@id="statistic-fixed"]/table[4]/tbody/tr[2]/td')
        expects = ['31,723', '3,000', '400']
        self._assert_texts(actuals, expects)
        actuals = self.driver.find_elements_by_xpath('//*[@id="statistic-fixed"]/table[4]/tbody/tr[3]/td')
        expects = ['3,120', '6,430', '1,000']
        self._assert_texts(actuals, expects)

    def test_add_bank_food(self):
        self._test_add('テスト1', '銀行', '食費')

    def test_add_cash_necessary(self):
        self._test_add('テスト', '現金', '必需品')

    def test_add_paypay_other(self):
        self._test_add('テスト1', 'PayPay', 'その他')

    def test_add_bank_intra(self):
        self._test_add('テスト1', '銀行', '内部移動')

    def test_add_cash_deposit(self):
        self._test_add('テスト1', '現金', '貯金')

    def test_add_paypay_out(self):
        self._test_add('テスト1', 'PayPay', '計算外')

    def test_add_escape(self):
        self._test_add('テ&ス<>ト', '銀行', '食費')

    def test_all_charge(self):
        now = datetime.now()
        self._login()
        self.driver.get(self.live_server_url + reverse('moneybook:index'))

        self.assertEqual(len(self.driver.find_elements_by_xpath('//*[@id="transactions"]/table/tbody/tr')), 1)

        # 1件追加
        self.driver.find_element_by_id('a_day').send_keys('3')
        self.driver.find_element_by_id('a_item').send_keys('テスト1')
        self.driver.find_element_by_id('a_price').send_keys('2000')
        self.driver.find_element_by_xpath('//*[@id="filter-fixed"]/form/table/tbody/tr[4]/td/label[3]').click()
        self.driver.find_element_by_xpath('//*[@id="filter-fixed"]/form/table/tbody/tr[5]/td/table/tbody/tr/td/label[1]').click()
        self.driver.find_element_by_id('lbl_is-charge').click()
        self.driver.find_element_by_xpath('//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        rows = self.driver.find_elements_by_xpath('//*[@id="transactions"]/table/tbody/tr')
        self.assertEqual(len(rows), 4)
        tds = rows[1].find_elements_by_tag_name('td')
        self.assertEqual(tds[0].text, str(now.year) + "/" + str.zfill(str(now.month), 2) + "/" + '03')
        self.assertEqual(tds[1].text, 'PayPayチャージ')
        self.assertEqual(tds[2].text, '2,000')
        self.assertEqual(tds[3].text, 'PayPay')
        self.assertEqual(tds[4].text, '内部移動')
        tds = rows[2].find_elements_by_tag_name('td')
        self.assertEqual(tds[0].text, str(now.year) + "/" + str.zfill(str(now.month), 2) + "/" + '03')
        self.assertEqual(tds[1].text, 'PayPayチャージ')
        self.assertEqual(tds[2].text, '2,000')
        self.assertEqual(tds[3].text, '銀行')
        self.assertEqual(tds[4].text, '内部移動')
        tds = rows[3].find_elements_by_tag_name('td')
        self.assertEqual(tds[0].text, str(now.year) + "/" + str.zfill(str(now.month), 2) + "/" + '03')
        self.assertEqual(tds[1].text, 'テスト1')
        self.assertEqual(tds[2].text, '2,000')
        self.assertEqual(tds[3].text, 'PayPay')
        self.assertEqual(tds[4].text, '食費')

    def test_invalid_add_str_year(self):
        now = datetime.now()
        self._test_invalid_add('a', now.month, now.day, 'テスト1', 100)

    def test_invalid_add_empty_year(self):
        now = datetime.now()
        self._test_invalid_add('', now.month, now.day, 'テスト1', 100)

    def test_invalid_add_str_month(self):
        now = datetime.now()
        self._test_invalid_add(now.year, 'a', now.day, 'テスト1', 100)

    def test_invalid_add_empty_month(self):
        now = datetime.now()
        self._test_invalid_add(now.year, '', now.day, 'テスト1', 100)

    def test_invalid_add_str_day(self):
        now = datetime.now()
        self._test_invalid_add(now.year, now.month, 'a', 'テスト1', 100)

    def test_invalid_add_empty_day(self):
        now = datetime.now()
        self._test_invalid_add(now.year, now.month, '', 'テスト1', 100)

    def test_invalid_add_str_price(self):
        now = datetime.now()
        self._test_invalid_add(now.year, now.month, now.day, 'テスト1', 'a')

    def test_invalid_add_empty_item(self):
        now = datetime.now()
        self._test_invalid_add(now.year, now.month, now.day, '', 100)

    def test_invalid_add_empty_price(self):
        now = datetime.now()
        self._test_invalid_add(now.year, now.month, now.day, 'テスト1', '')

    def test_filter_button(self):
        self._login()
        self.driver.get(self.live_server_url + reverse('moneybook:index'))

        self.driver.find_element_by_id('jump_year').clear()
        self.driver.find_element_by_id('jump_year').send_keys('2000')
        self.driver.find_element_by_id('jump_month').clear()
        self.driver.find_element_by_id('jump_month').send_keys('1')
        self.driver.find_element_by_xpath(
            '//*[@id="filter-fixed"]/table[1]/tbody/tr[1]/td[1]/table/tbody/tr[2]/td[1]/input[@type="button"]'
        ).click()
        self._test_index_date(2000, 1)

    def test_filter_year_enter(self):
        self._login()
        self.driver.get(self.live_server_url + reverse('moneybook:index'))

        self.driver.find_element_by_id('jump_year').clear()
        self.driver.find_element_by_id('jump_year').send_keys('2000')
        self.driver.find_element_by_id('jump_month').clear()
        self.driver.find_element_by_id('jump_month').send_keys('1')
        self.driver.find_element_by_id('jump_year').send_keys(Keys.RETURN)
        self._test_index_date(2000, 1)

    def test_filter_month_enter(self):
        self._login()
        self.driver.get(self.live_server_url + reverse('moneybook:index'))

        self.driver.find_element_by_id('jump_year').clear()
        self.driver.find_element_by_id('jump_year').send_keys('2000')
        self.driver.find_element_by_id('jump_month').clear()
        self.driver.find_element_by_id('jump_month').send_keys('1')
        self.driver.find_element_by_id('jump_month').send_keys(Keys.RETURN)
        self._test_index_date(2000, 1)

    def test_filter_jump_last(self):
        self._login()
        self.driver.get(self.live_server_url + reverse('moneybook:index_month', kwargs={'year': 2000, 'month': 1}))
        self.driver.find_element_by_xpath(
            '//*[@id="filter-fixed"]/table[1]/tbody/tr[1]/td[1]/table/tbody/tr[1]/td[1]/a'
        ).click()
        self._test_index_date(1999, 12)

    def test_filter_jump_next(self):
        self._login()
        self.driver.get(self.live_server_url + reverse('moneybook:index_month', kwargs={'year': 2000, 'month': 12}))
        self.driver.find_element_by_xpath(
            '//*[@id="filter-fixed"]/table[1]/tbody/tr[1]/td[1]/table/tbody/tr[1]/td[3]/a'
        ).click()
        self._test_index_date(2001, 1)
