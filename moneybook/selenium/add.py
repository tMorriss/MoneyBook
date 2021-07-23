from datetime import datetime

from django.urls import reverse
from moneybook.selenium.base import SeleniumBase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.color import Color


class Add(SeleniumBase):
    # def test_get(self):
    #     now = datetime.now()
    #     self._login()
    #     self.driver.get(self.live_server_url + reverse('moneybook:add'))

    #     self._assert_common()

    #     self.assertEqual(self.driver.find_element_by_id('c_year').get_attribute('value'), str(now.year))
    #     self.assertEqual(self.driver.find_element_by_id('c_month').get_attribute('value'), str(now.month))
    #     self.assertEqual(self.driver.find_element_by_id('c_day').get_attribute('value'), '')
    #     self.assertEqual(self.driver.find_element_by_id('c_price').get_attribute('value'), '')
    #     expects = ['Kyash', 'PayPay']
    #     actuals = self.driver.find_elements_by_xpath('//section/form[1]/table/tbody/tr[3]/td/label')
    #     self._assert_texts(actuals, expects)

    #     self.assertEqual(self.driver.find_element_by_id('m_year').get_attribute('value'), str(now.year))
    #     self.assertEqual(self.driver.find_element_by_id('m_month').get_attribute('value'), str(now.month))
    #     self.assertEqual(self.driver.find_element_by_id('m_day').get_attribute('value'), '')
    #     self.assertEqual(self.driver.find_element_by_id('m_item').get_attribute('value'), '')
    #     self.assertEqual(self.driver.find_element_by_id('m_price').get_attribute('value'), '')
    #     expects = ['銀行', '現金', 'Kyash', 'PayPay']
    #     actuals = self.driver.find_elements_by_xpath('//section/form[2]/table/tbody/tr[4]/td/label')
    #     self._assert_texts(actuals, expects)
    #     actuals = self.driver.find_elements_by_xpath('//section/form[2]/table/tbody/tr[5]/td/label')
    #     self._assert_texts(actuals, expects)

    #     self.assertEqual(self.driver.find_element_by_id('s_year').get_attribute('value'), str(now.year))
    #     self.assertEqual(self.driver.find_element_by_id('s_month').get_attribute('value'), str(now.month))
    #     self.assertEqual(self.driver.find_element_by_id('s_day').get_attribute('value'), '')
    #     self.assertEqual(self.driver.find_element_by_id('s_price').get_attribute('value'), '')
    #     self.assertEqual(self.driver.find_element_by_xpath(
    #         '//section/form[3]/table/tbody/tr[3]/td/input[1]').get_attribute('value'), 'PayPayキャッシュバック&ボーナス')
    #     self.assertEqual(self.driver.find_element_by_xpath(
    #         '//section/form[3]/table/tbody/tr[3]/td/input[2]').get_attribute('value'), 'Suicaチャージ')

    #     self.assertEqual(self.driver.find_element_by_id('a_year').get_attribute('value'), str(now.year))
    #     self.assertEqual(self.driver.find_element_by_id('a_month').get_attribute('value'), str(now.month))
    #     self.assertEqual(self.driver.find_element_by_id('a_day').get_attribute('value'), '')
    #     self.assertEqual(self.driver.find_element_by_id('a_item').get_attribute('value'), '')
    #     self.assertEqual(self.driver.find_element_by_id('a_price').get_attribute('value'), '')
    #     expects = ['収入', '支出']
    #     actuals = self.driver.find_elements_by_xpath('//section/form[4]/table/tbody/tr[4]/td/label')
    #     self._assert_texts(actuals, expects)
    #     expects = ['銀行', '現金', 'Kyash', 'PayPay']
    #     actuals = self.driver.find_elements_by_xpath('//section/form[4]/table/tbody/tr[5]/td/label')
    #     self._assert_texts(actuals, expects)
    #     expects = ['食費', '必需品', 'その他', '内部移動', '貯金', '計算外']
    #     actuals = self.driver.find_elements_by_xpath('//section/form[4]/table/tbody/tr[6]/td/label')
    #     self._assert_texts(actuals, expects)
    #     expects = ['No', 'Yes']
    #     actuals = self.driver.find_elements_by_xpath('//section/form[4]/table/tbody/tr[7]/td/label')
    #     self._assert_texts(actuals, expects)

    # def _assert_bank_charge_kyash(self, method):
    #     now = datetime.now()
    #     self.driver.get(self.live_server_url + reverse('moneybook:index'))
    #     rows = self.driver.find_elements_by_xpath('//*[@id="transactions"]/table/tbody/tr')
    #     self.assertEqual(len(rows), 3)
    #     tds = rows[1].find_elements_by_tag_name('td')
    #     self.assertEqual(tds[0].text, str(now.year) + "/" + str.zfill(str(now.month), 2) + "/" + '01')
    #     self.assertEqual(tds[1].text, method + 'チャージ')
    #     self.assertEqual(tds[2].text, '100')
    #     self.assertEqual(tds[3].text, method)
    #     self.assertEqual(tds[4].text, '内部移動')
    #     self.assertEqual(Color.from_string(rows[1].value_of_css_property('background-color')), Color.from_string('rgba(0, 0, 0, 0)'))
    #     # direction確認
    #     tds[5].find_element_by_tag_name('a').click()
    #     self.assertEqual(self.driver.find_element_by_xpath('//form/table[1]/tbody/tr[4]/td[1]/input[1]').is_selected(), True)

    #     self.driver.get(self.live_server_url + reverse('moneybook:index'))
    #     rows = self.driver.find_elements_by_xpath('//*[@id="transactions"]/table/tbody/tr')
    #     tds = rows[2].find_elements_by_tag_name('td')
    #     self.assertEqual(tds[0].text, str(now.year) + "/" + str.zfill(str(now.month), 2) + "/" + '01')
    #     self.assertEqual(tds[1].text, method + 'チャージ')
    #     self.assertEqual(tds[2].text, '100')
    #     self.assertEqual(tds[3].text, '銀行')
    #     self.assertEqual(tds[4].text, '内部移動')
    #     self.assertEqual(Color.from_string(rows[2].value_of_css_property('background-color')), Color.from_string('rgba(0, 0, 0, 0)'))
    #     # direction確認
    #     tds[5].find_element_by_tag_name('a').click()
    #     self.assertEqual(self.driver.find_element_by_xpath('//form/table[1]/tbody/tr[4]/td[1]/input[2]').is_selected(), True)

    # def _assert_intra_move(self):
    #     now = datetime.now()
    #     self.driver.get(self.live_server_url + reverse('moneybook:index'))
    #     rows = self.driver.find_elements_by_xpath('//*[@id="transactions"]/table/tbody/tr')
    #     self.assertEqual(len(rows), 3)
    #     tds = rows[1].find_elements_by_tag_name('td')
    #     self.assertEqual(tds[0].text, str(now.year) + "/" + str.zfill(str(now.month), 2) + "/" + '02')
    #     self.assertEqual(tds[1].text, 'ないぶいどう')
    #     self.assertEqual(tds[2].text, '200')
    #     self.assertEqual(tds[3].text, 'Kyash')
    #     self.assertEqual(tds[4].text, '内部移動')
    #     self.assertEqual(Color.from_string(rows[1].value_of_css_property('background-color')), Color.from_string('rgba(0, 0, 0, 0)'))
    #     # direction確認
    #     tds[5].find_element_by_tag_name('a').click()
    #     self.assertEqual(self.driver.find_element_by_xpath('//form/table[1]/tbody/tr[4]/td[1]/input[1]').is_selected(), True)

    #     self.driver.get(self.live_server_url + reverse('moneybook:index'))
    #     rows = self.driver.find_elements_by_xpath('//*[@id="transactions"]/table/tbody/tr')
    #     tds = rows[2].find_elements_by_tag_name('td')
    #     self.assertEqual(tds[0].text, str(now.year) + "/" + str.zfill(str(now.month), 2) + "/" + '02')
    #     self.assertEqual(tds[1].text, 'ないぶいどう')
    #     self.assertEqual(tds[2].text, '200')
    #     self.assertEqual(tds[3].text, '現金')
    #     self.assertEqual(tds[4].text, '内部移動')
    #     self.assertEqual(Color.from_string(rows[2].value_of_css_property('background-color')), Color.from_string('rgba(0, 0, 0, 0)'))
    #     # direction確認
    #     tds[5].find_element_by_tag_name('a').click()
    #     self.assertEqual(self.driver.find_element_by_xpath('//form/table[1]/tbody/tr[4]/td[1]/input[2]').is_selected(), True)

    # def test_bank_charge_click(self):
    #     # 前処理
    #     self._login()
    #     self.driver.get(self.live_server_url + reverse('moneybook:add'))

    #     # テスト
    #     self.driver.find_element_by_id('c_day').send_keys('1')
    #     self.driver.find_element_by_id('c_price').send_keys('100')
    #     self.driver.find_element_by_xpath('//form[1]/input[@type="button"]').click()

    #     # 検証
    #     self._assert_bank_charge_kyash('Kyash')

    # def test_bank_charge_year_enter(self):
    #     # 前処理
    #     self._login()
    #     self.driver.get(self.live_server_url + reverse('moneybook:add'))

    #     # テスト
    #     self.driver.find_element_by_id('c_day').send_keys('1')
    #     self.driver.find_element_by_id('c_price').send_keys('100')
    #     self.driver.find_element_by_id('c_year').send_keys(Keys.RETURN)

    #     # 検証
    #     self._assert_bank_charge_kyash('Kyash')

    # def test_bank_charge_month_enter(self):
    #     # 前処理
    #     self._login()
    #     self.driver.get(self.live_server_url + reverse('moneybook:add'))

    #     # テスト
    #     self.driver.find_element_by_id('c_day').send_keys('1')
    #     self.driver.find_element_by_id('c_price').send_keys('100')
    #     self.driver.find_element_by_id('c_month').send_keys(Keys.RETURN)

    #     # 検証
    #     self._assert_bank_charge_kyash('Kyash')

    # def test_bank_charge_day_enter(self):
    #     # 前処理
    #     self._login()
    #     self.driver.get(self.live_server_url + reverse('moneybook:add'))

    #     # テスト
    #     self.driver.find_element_by_id('c_day').send_keys('1')
    #     self.driver.find_element_by_id('c_price').send_keys('100')
    #     self.driver.find_element_by_id('c_day').send_keys(Keys.RETURN)

    #     # 検証
    #     self._assert_bank_charge_kyash('Kyash')

    # def test_bank_charge_price_enter(self):
    #     # 前処理
    #     self._login()
    #     self.driver.get(self.live_server_url + reverse('moneybook:add'))

    #     # テスト
    #     self.driver.find_element_by_id('c_day').send_keys('1')
    #     self.driver.find_element_by_id('c_price').send_keys('100')
    #     self.driver.find_element_by_id('c_price').send_keys(Keys.RETURN)

    #     # 検証
    #     self._assert_bank_charge_kyash('Kyash')

    # def test_bank_charge_method_enter(self):
    #     # 前処理
    #     self._login()
    #     self.driver.get(self.live_server_url + reverse('moneybook:add'))

    #     # テスト
    #     self.driver.find_element_by_id('c_day').send_keys('1')
    #     self.driver.find_element_by_id('c_price').send_keys('100')
    #     self.driver.find_element_by_xpath('//form[1]/table/tbody/tr[3]/td/input[1]').send_keys(Keys.RETURN)

    #     # 検証
    #     self._assert_bank_charge_kyash('Kyash')

    # def test_bank_charge_select(self):
    #     # 前処理
    #     self._login()
    #     self.driver.get(self.live_server_url + reverse('moneybook:add'))

    #     # テスト
    #     self.driver.find_element_by_id('c_day').send_keys('1')
    #     self.driver.find_element_by_id('c_price').send_keys('100')
    #     self.driver.find_element_by_xpath('//form[1]/table/tbody/tr[3]/td/label[2]').click()
    #     self.driver.find_element_by_xpath('//form[1]/input[@type="button"]').click()

    #     # 検証
    #     self._assert_bank_charge_kyash('PayPay')

    # def test_intra_move_click(self):
    #     # 前処理
    #     self._login()
    #     self.driver.get(self.live_server_url + reverse('moneybook:add'))

    #     # テスト
    #     self.driver.find_element_by_id('m_day').send_keys('2')
    #     self.driver.find_element_by_id('m_item').send_keys('ないぶいどう')
    #     self.driver.find_element_by_id('m_price').send_keys('200')
    #     self.driver.find_element_by_xpath('//form[2]/table/tbody/tr[4]/td/label[2]').click()
    #     self.driver.find_element_by_xpath('//form[2]/table/tbody/tr[5]/td/label[3]').click()
    #     self.driver.find_element_by_xpath('//form[2]/input[@type="button"]').click()

    #     # 検証
    #     self._assert_intra_move()

    # def test_intra_move_year(self):
    #     # 前処理
    #     self._login()
    #     self.driver.get(self.live_server_url + reverse('moneybook:add'))

    #     # テスト
    #     self.driver.find_element_by_id('m_day').send_keys('2')
    #     self.driver.find_element_by_id('m_item').send_keys('ないぶいどう')
    #     self.driver.find_element_by_id('m_price').send_keys('200')
    #     self.driver.find_element_by_xpath('//form[2]/table/tbody/tr[4]/td/label[2]').click()
    #     self.driver.find_element_by_xpath('//form[2]/table/tbody/tr[5]/td/label[3]').click()
    #     self.driver.find_element_by_id('m_year').send_keys(Keys.RETURN)

    #     # 検証
    #     self._assert_intra_move()

    # def test_intra_move_month(self):
    #     # 前処理
    #     self._login()
    #     self.driver.get(self.live_server_url + reverse('moneybook:add'))

    #     # テスト
    #     self.driver.find_element_by_id('m_day').send_keys('2')
    #     self.driver.find_element_by_id('m_item').send_keys('ないぶいどう')
    #     self.driver.find_element_by_id('m_price').send_keys('200')
    #     self.driver.find_element_by_xpath('//form[2]/table/tbody/tr[4]/td/label[2]').click()
    #     self.driver.find_element_by_xpath('//form[2]/table/tbody/tr[5]/td/label[3]').click()
    #     self.driver.find_element_by_id('m_month').send_keys(Keys.RETURN)

    #     # 検証
    #     self._assert_intra_move()

    # def test_intra_move_day(self):
    #     # 前処理
    #     self._login()
    #     self.driver.get(self.live_server_url + reverse('moneybook:add'))

    #     # テスト
    #     self.driver.find_element_by_id('m_day').send_keys('2')
    #     self.driver.find_element_by_id('m_item').send_keys('ないぶいどう')
    #     self.driver.find_element_by_id('m_price').send_keys('200')
    #     self.driver.find_element_by_xpath('//form[2]/table/tbody/tr[4]/td/label[2]').click()
    #     self.driver.find_element_by_xpath('//form[2]/table/tbody/tr[5]/td/label[3]').click()
    #     self.driver.find_element_by_id('m_day').send_keys(Keys.RETURN)

    #     # 検証
    #     self._assert_intra_move()

    # def test_intra_move_item(self):
    #     # 前処理
    #     self._login()
    #     self.driver.get(self.live_server_url + reverse('moneybook:add'))

    #     # テスト
    #     self.driver.find_element_by_id('m_day').send_keys('2')
    #     self.driver.find_element_by_id('m_item').send_keys('ないぶいどう')
    #     self.driver.find_element_by_id('m_price').send_keys('200')
    #     self.driver.find_element_by_xpath('//form[2]/table/tbody/tr[4]/td/label[2]').click()
    #     self.driver.find_element_by_xpath('//form[2]/table/tbody/tr[5]/td/label[3]').click()
    #     self.driver.find_element_by_id('m_item').send_keys(Keys.RETURN)

    #     # 検証
    #     self._assert_intra_move()

    # def test_intra_move_price(self):
    #     # 前処理
    #     self._login()
    #     self.driver.get(self.live_server_url + reverse('moneybook:add'))

    #     # テスト
    #     self.driver.find_element_by_id('m_day').send_keys('2')
    #     self.driver.find_element_by_id('m_item').send_keys('ないぶいどう')
    #     self.driver.find_element_by_id('m_price').send_keys('200')
    #     self.driver.find_element_by_xpath('//form[2]/table/tbody/tr[4]/td/label[2]').click()
    #     self.driver.find_element_by_xpath('//form[2]/table/tbody/tr[5]/td/label[3]').click()
    #     self.driver.find_element_by_id('m_price').send_keys(Keys.RETURN)

    #     # 検証
    #     self._assert_intra_move()

    # def test_intra_move_before(self):
    #     # 前処理
    #     self._login()
    #     self.driver.get(self.live_server_url + reverse('moneybook:add'))

    #     # テスト
    #     self.driver.find_element_by_id('m_day').send_keys('2')
    #     self.driver.find_element_by_id('m_item').send_keys('ないぶいどう')
    #     self.driver.find_element_by_id('m_price').send_keys('200')
    #     self.driver.find_element_by_xpath('//form[2]/table/tbody/tr[4]/td/label[2]').click()
    #     self.driver.find_element_by_xpath('//form[2]/table/tbody/tr[5]/td/label[3]').click()
    #     self.driver.find_element_by_xpath('//form[2]/table/tbody/tr[4]/td/input[2]').send_keys(Keys.RETURN)

    #     # 検証
    #     self._assert_intra_move()

    # def test_intra_move_after(self):
    #     # 前処理
    #     self._login()
    #     self.driver.get(self.live_server_url + reverse('moneybook:add'))

    #     # テスト
    #     self.driver.find_element_by_id('m_day').send_keys('2')
    #     self.driver.find_element_by_id('m_item').send_keys('ないぶいどう')
    #     self.driver.find_element_by_id('m_price').send_keys('200')
    #     self.driver.find_element_by_xpath('//form[2]/table/tbody/tr[4]/td/label[2]').click()
    #     self.driver.find_element_by_xpath('//form[2]/table/tbody/tr[5]/td/label[3]').click()
    #     self.driver.find_element_by_xpath('//form[2]/table/tbody/tr[5]/td/input[3]').send_keys(Keys.RETURN)

    #     # 検証
    #     self._assert_intra_move()

    def test_paypay_cb(self):
        now = datetime.now()
        # 前処理
        self._login()
        self.driver.get(self.live_server_url + reverse('moneybook:add'))

        # テスト
        self.driver.find_element_by_id('s_day').send_keys('3')
        self.driver.find_element_by_id('s_price').send_keys('300')
        import time
        time.sleep(5)
        self.driver.find_element_by_xpath('//form[3]/table/tbody/tr[3]/td/input[@type="button"][1]').click()
        time.sleep(30)

        self.driver.get(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements_by_xpath('//*[@id="transactions"]/table/tbody/tr')
        self.assertEqual(len(rows), 3)
        tds = rows[1].find_elements_by_tag_name('td')
        self.assertEqual(tds[0].text, str(now.year) + "/" + str.zfill(str(now.month), 2) + "/" + '03')
        self.assertEqual(tds[1].text, 'ボーナス運用')
        self.assertEqual(tds[2].text, '300')
        self.assertEqual(tds[3].text, 'PayPay')
        self.assertEqual(tds[4].text, '貯金')
        self.assertEqual(Color.from_string(rows[1].value_of_css_property('background-color')), Color.from_string('rgba(0, 0, 0, 0)'))
        # direction確認
        tds[5].find_element_by_tag_name('a').click()
        self.assertEqual(self.driver.find_element_by_xpath('//form/table[1]/tbody/tr[4]/td[1]/input[1]').is_selected(), True)

        self.driver.get(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements_by_xpath('//*[@id="transactions"]/table/tbody/tr')
        tds = rows[2].find_elements_by_tag_name('td')
        self.assertEqual(tds[0].text, str(now.year) + "/" + str.zfill(str(now.month), 2) + "/" + '03')
        self.assertEqual(tds[1].text, 'PayPayキャッシュバック')
        self.assertEqual(tds[2].text, '300')
        self.assertEqual(tds[3].text, 'PayPay')
        self.assertEqual(tds[4].text, '収入')
        self.assertEqual(Color.from_string(rows[2].value_of_css_property('background-color')), Color.from_string('rgba(0, 0, 0, 0)'))
        # direction確認
        tds[5].find_element_by_tag_name('a').click()
        self.assertEqual(self.driver.find_element_by_xpath('//form/table[1]/tbody/tr[4]/td[1]/input[2]').is_selected(), True)
