import time
from datetime import datetime

from django.urls import reverse
from moneybook.selenium.base import SeleniumBase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.color import Color


class Add(SeleniumBase):
    def _assert_bank_charge_kyash(self, method):
        now = datetime.now()
        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        self.assertEqual(len(rows), 3)
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, str(now.year) + "/" + str.zfill(str(now.month), 2) + "/" + '01')
        self.assertEqual(tds[1].text, method + 'チャージ')
        self.assertEqual(tds[2].text, '100')
        self.assertEqual(tds[3].text, method)
        self.assertEqual(tds[4].text, '内部移動')
        self.assertEqual(Color.from_string(rows[1].value_of_css_property('background-color')), Color.from_string('rgba(0, 0, 0, 0)'))
        # direction確認
        tds[5].find_element(By.TAG_NAME, 'a').click()
        self.assertEqual(self.driver.find_element(By.XPATH, '//form/table[1]/tbody/tr[4]/td[1]/input[1]').is_selected(), True)

        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        tds = rows[2].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, str(now.year) + "/" + str.zfill(str(now.month), 2) + "/" + '01')
        self.assertEqual(tds[1].text, method + 'チャージ')
        self.assertEqual(tds[2].text, '100')
        self.assertEqual(tds[3].text, '銀行')
        self.assertEqual(tds[4].text, '内部移動')
        self.assertEqual(Color.from_string(rows[2].value_of_css_property('background-color')), Color.from_string('rgba(0, 0, 0, 0)'))
        # direction確認
        tds[5].find_element(By.TAG_NAME, 'a').click()
        self.assertEqual(self.driver.find_element(By.XPATH, '//form/table[1]/tbody/tr[4]/td[1]/input[2]').is_selected(), True)

    def _assert_intra_move(self):
        now = datetime.now()
        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        self.assertEqual(len(rows), 3)
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, str(now.year) + "/" + str.zfill(str(now.month), 2) + "/" + '02')
        self.assertEqual(tds[1].text, 'ないぶいどう')
        self.assertEqual(tds[2].text, '200')
        self.assertEqual(tds[3].text, 'Kyash')
        self.assertEqual(tds[4].text, '内部移動')
        self.assertEqual(Color.from_string(rows[1].value_of_css_property('background-color')), Color.from_string('rgba(0, 0, 0, 0)'))
        # direction確認
        tds[5].find_element(By.TAG_NAME, 'a').click()
        self.assertEqual(self.driver.find_element(By.XPATH, '//form/table[1]/tbody/tr[4]/td[1]/input[1]').is_selected(), True)

        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        tds = rows[2].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, str(now.year) + "/" + str.zfill(str(now.month), 2) + "/" + '02')
        self.assertEqual(tds[1].text, 'ないぶいどう')
        self.assertEqual(tds[2].text, '200')
        self.assertEqual(tds[3].text, '現金')
        self.assertEqual(tds[4].text, '内部移動')
        self.assertEqual(Color.from_string(rows[2].value_of_css_property('background-color')), Color.from_string('rgba(0, 0, 0, 0)'))
        # direction確認
        tds[5].find_element(By.TAG_NAME, 'a').click()
        self.assertEqual(self.driver.find_element(By.XPATH, '//form/table[1]/tbody/tr[4]/td[1]/input[2]').is_selected(), True)

    def test_get(self):
        now = datetime.now()
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self._assert_common()

        self.assertEqual(self.driver.find_element(By.ID, 'c_year').get_attribute('value'), str(now.year))
        self.assertEqual(self.driver.find_element(By.ID, 'c_month').get_attribute('value'), str(now.month))
        self.assertEqual(self.driver.find_element(By.ID, 'c_day').get_attribute('value'), '')
        self.assertEqual(self.driver.find_element(By.ID, 'c_price').get_attribute('value'), '')
        expects = ['Kyash', 'PayPay']
        actuals = self.driver.find_elements(By.XPATH, '//section/form[1]/table/tbody/tr[3]/td/label')
        self._assert_texts(actuals, expects)

        self.assertEqual(self.driver.find_element(By.ID, 'm_year').get_attribute('value'), str(now.year))
        self.assertEqual(self.driver.find_element(By.ID, 'm_month').get_attribute('value'), str(now.month))
        self.assertEqual(self.driver.find_element(By.ID, 'm_day').get_attribute('value'), '')
        self.assertEqual(self.driver.find_element(By.ID, 'm_item').get_attribute('value'), '')
        self.assertEqual(self.driver.find_element(By.ID, 'm_price').get_attribute('value'), '')
        expects = ['銀行', '現金', 'Kyash', 'PayPay']
        actuals = self.driver.find_elements(By.XPATH, '//section/form[2]/table/tbody/tr[4]/td/label')
        self._assert_texts(actuals, expects)
        actuals = self.driver.find_elements(By.XPATH, '//section/form[2]/table/tbody/tr[5]/td/label')
        self._assert_texts(actuals, expects)

        self.assertEqual(self.driver.find_element(By.ID, 's_year').get_attribute('value'), str(now.year))
        self.assertEqual(self.driver.find_element(By.ID, 's_month').get_attribute('value'), str(now.month))
        self.assertEqual(self.driver.find_element(By.ID, 's_day').get_attribute('value'), '')
        self.assertEqual(self.driver.find_element(By.ID, 's_day').get_attribute('placeholder'), str(now.day))
        self.assertEqual(self.driver.find_element(By.ID, 's_price').get_attribute('value'), '')
        self.assertEqual(self.driver.find_element(By.ID, 's_price').get_attribute('placeholder'), '3000')
        self.assertEqual(self.driver.find_element(By.XPATH,
                                                  '//section/form[3]/table/tbody/tr[3]/td/input[1]').get_attribute('value'), 'Suicaチャージ')

        self.assertEqual(self.driver.find_element(By.ID, 'a_year').get_attribute('value'), str(now.year))
        self.assertEqual(self.driver.find_element(By.ID, 'a_month').get_attribute('value'), str(now.month))
        self.assertEqual(self.driver.find_element(By.ID, 'a_day').get_attribute('value'), '')
        self.assertEqual(self.driver.find_element(By.ID, 'a_item').get_attribute('value'), '')
        self.assertEqual(self.driver.find_element(By.ID, 'a_price').get_attribute('value'), '')
        expects = ['収入', '支出']
        actuals = self.driver.find_elements(By.XPATH, '//section/form[4]/table/tbody/tr[4]/td/label')
        self._assert_texts(actuals, expects)
        expects = ['銀行', '現金', 'Kyash', 'PayPay']
        actuals = self.driver.find_elements(By.XPATH, '//section/form[4]/table/tbody/tr[5]/td/label')
        self._assert_texts(actuals, expects)
        expects = ['食費', '必需品', '交通費', 'その他', '内部移動', '貯金', '計算外', '収入']
        actuals = self.driver.find_elements(By.XPATH, '//section/form[4]/table/tbody/tr[6]/td/label')
        self._assert_texts(actuals, expects)
        expects = ['No', 'Yes']
        actuals = self.driver.find_elements(By.XPATH, '//section/form[4]/table/tbody/tr[7]/td/label')
        self._assert_texts(actuals, expects)

    def test_bank_charge_click(self):
        # 前処理
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # テスト
        self.driver.find_element(By.ID, 'c_day').send_keys('1')
        self.driver.find_element(By.ID, 'c_price').send_keys('100')
        self.driver.find_element(By.XPATH, '//form[1]/input[@type="button"]').click()

        # 検証
        self._assert_bank_charge_kyash('Kyash')

    def test_bank_charge_year_enter(self):
        # 前処理
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # テスト
        self.driver.find_element(By.ID, 'c_day').send_keys('1')
        self.driver.find_element(By.ID, 'c_price').send_keys('100')
        self.driver.find_element(By.ID, 'c_year').send_keys(Keys.RETURN)

        # 検証
        self._assert_bank_charge_kyash('Kyash')

    def test_bank_charge_month_enter(self):
        # 前処理
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # テスト
        self.driver.find_element(By.ID, 'c_day').send_keys('1')
        self.driver.find_element(By.ID, 'c_price').send_keys('100')
        self.driver.find_element(By.ID, 'c_month').send_keys(Keys.RETURN)

        # 検証
        self._assert_bank_charge_kyash('Kyash')

    def test_bank_charge_day_enter(self):
        # 前処理
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # テスト
        self.driver.find_element(By.ID, 'c_day').send_keys('1')
        self.driver.find_element(By.ID, 'c_price').send_keys('100')
        self.driver.find_element(By.ID, 'c_day').send_keys(Keys.RETURN)

        # 検証
        self._assert_bank_charge_kyash('Kyash')

    def test_bank_charge_price_enter(self):
        # 前処理
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # テスト
        self.driver.find_element(By.ID, 'c_day').send_keys('1')
        self.driver.find_element(By.ID, 'c_price').send_keys('100')
        self.driver.find_element(By.ID, 'c_price').send_keys(Keys.RETURN)

        # 検証
        self._assert_bank_charge_kyash('Kyash')

    def test_bank_charge_method_enter(self):
        # 前処理
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # テスト
        self.driver.find_element(By.ID, 'c_day').send_keys('1')
        self.driver.find_element(By.ID, 'c_price').send_keys('100')
        self.driver.find_element(By.XPATH, '//form[1]/table/tbody/tr[3]/td/input[1]').send_keys(Keys.RETURN)

        # 検証
        self._assert_bank_charge_kyash('Kyash')

    def test_bank_charge_select(self):
        # 前処理
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # テスト
        self.driver.find_element(By.ID, 'c_day').send_keys('1')
        self.driver.find_element(By.ID, 'c_price').send_keys('100')
        self.driver.find_element(By.XPATH, '//form[1]/table/tbody/tr[3]/td/label[2]').click()
        self.driver.find_element(By.XPATH, '//form[1]/input[@type="button"]').click()

        # 検証
        self._assert_bank_charge_kyash('PayPay')

    def test_intra_move_click(self):
        # 前処理
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # テスト
        self.driver.find_element(By.ID, 'm_day').send_keys('2')
        self.driver.find_element(By.ID, 'm_item').send_keys('ないぶいどう')
        self.driver.find_element(By.ID, 'm_price').send_keys('200')
        self.driver.find_element(By.XPATH, '//form[2]/table/tbody/tr[4]/td/label[2]').click()
        self.driver.find_element(By.XPATH, '//form[2]/table/tbody/tr[5]/td/label[3]').click()
        self.driver.find_element(By.XPATH, '//form[2]/input[@type="button"]').click()

        # 検証
        self._assert_intra_move()

    def test_intra_move_year(self):
        # 前処理
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # テスト
        self.driver.find_element(By.ID, 'm_day').send_keys('2')
        self.driver.find_element(By.ID, 'm_item').send_keys('ないぶいどう')
        self.driver.find_element(By.ID, 'm_price').send_keys('200')
        self.driver.find_element(By.XPATH, '//form[2]/table/tbody/tr[4]/td/label[2]').click()
        self.driver.find_element(By.XPATH, '//form[2]/table/tbody/tr[5]/td/label[3]').click()
        self.driver.find_element(By.ID, 'm_year').send_keys(Keys.RETURN)

        # 検証
        self._assert_intra_move()

    def test_intra_move_month(self):
        # 前処理
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # テスト
        self.driver.find_element(By.ID, 'm_day').send_keys('2')
        self.driver.find_element(By.ID, 'm_item').send_keys('ないぶいどう')
        self.driver.find_element(By.ID, 'm_price').send_keys('200')
        self.driver.find_element(By.XPATH, '//form[2]/table/tbody/tr[4]/td/label[2]').click()
        self.driver.find_element(By.XPATH, '//form[2]/table/tbody/tr[5]/td/label[3]').click()
        self.driver.find_element(By.ID, 'm_month').send_keys(Keys.RETURN)

        # 検証
        self._assert_intra_move()

    def test_intra_move_day(self):
        # 前処理
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # テスト
        self.driver.find_element(By.ID, 'm_day').send_keys('2')
        self.driver.find_element(By.ID, 'm_item').send_keys('ないぶいどう')
        self.driver.find_element(By.ID, 'm_price').send_keys('200')
        self.driver.find_element(By.XPATH, '//form[2]/table/tbody/tr[4]/td/label[2]').click()
        self.driver.find_element(By.XPATH, '//form[2]/table/tbody/tr[5]/td/label[3]').click()
        self.driver.find_element(By.ID, 'm_day').send_keys(Keys.RETURN)

        # 検証
        self._assert_intra_move()

    def test_intra_move_item(self):
        # 前処理
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # テスト
        self.driver.find_element(By.ID, 'm_day').send_keys('2')
        self.driver.find_element(By.ID, 'm_item').send_keys('ないぶいどう')
        self.driver.find_element(By.ID, 'm_price').send_keys('200')
        self.driver.find_element(By.XPATH, '//form[2]/table/tbody/tr[4]/td/label[2]').click()
        self.driver.find_element(By.XPATH, '//form[2]/table/tbody/tr[5]/td/label[3]').click()
        self.driver.find_element(By.ID, 'm_item').send_keys(Keys.RETURN)

        # 検証
        self._assert_intra_move()

    def test_intra_move_price(self):
        # 前処理
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # テスト
        self.driver.find_element(By.ID, 'm_day').send_keys('2')
        self.driver.find_element(By.ID, 'm_item').send_keys('ないぶいどう')
        self.driver.find_element(By.ID, 'm_price').send_keys('200')
        self.driver.find_element(By.XPATH, '//form[2]/table/tbody/tr[4]/td/label[2]').click()
        self.driver.find_element(By.XPATH, '//form[2]/table/tbody/tr[5]/td/label[3]').click()
        self.driver.find_element(By.ID, 'm_price').send_keys(Keys.RETURN)

        # 検証
        self._assert_intra_move()

    def test_intra_move_before(self):
        # 前処理
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # テスト
        self.driver.find_element(By.ID, 'm_day').send_keys('2')
        self.driver.find_element(By.ID, 'm_item').send_keys('ないぶいどう')
        self.driver.find_element(By.ID, 'm_price').send_keys('200')
        self.driver.find_element(By.XPATH, '//form[2]/table/tbody/tr[4]/td/label[2]').click()
        self.driver.find_element(By.XPATH, '//form[2]/table/tbody/tr[5]/td/label[3]').click()
        self.driver.find_element(By.XPATH, '//form[2]/table/tbody/tr[4]/td/input[2]').send_keys(Keys.RETURN)

        # 検証
        self._assert_intra_move()

    def test_intra_move_after(self):
        # 前処理
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # テスト
        self.driver.find_element(By.ID, 'm_day').send_keys('2')
        self.driver.find_element(By.ID, 'm_item').send_keys('ないぶいどう')
        self.driver.find_element(By.ID, 'm_price').send_keys('200')
        self.driver.find_element(By.XPATH, '//form[2]/table/tbody/tr[4]/td/label[2]').click()
        self.driver.find_element(By.XPATH, '//form[2]/table/tbody/tr[5]/td/label[3]').click()
        self.driver.find_element(By.XPATH, '//form[2]/table/tbody/tr[5]/td/input[3]').send_keys(Keys.RETURN)

        # 検証
        self._assert_intra_move()

    def test_suica_charge(self):
        now = datetime.now()
        # 前処理
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # テスト
        self.driver.find_element(By.ID, 's_day').send_keys('4')
        self.driver.find_element(By.ID, 's_price').send_keys('400')
        self.driver.find_element(By.XPATH, '//form[3]/table/tbody/tr[3]/td/input[@type="button"][1]').click()

        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        self.assertEqual(len(rows), 2)
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, str(now.year) + "/" + str.zfill(str(now.month), 2) + "/" + '04')
        self.assertEqual(tds[1].text, 'Suicaチャージ')
        self.assertEqual(tds[2].text, '400')
        self.assertEqual(tds[3].text, '銀行')
        self.assertEqual(tds[4].text, '交通費')
        self.assertEqual(Color.from_string(rows[1].value_of_css_property('background-color')), Color.from_string('rgba(0, 0, 0, 0)'))
        # direction確認
        tds[5].find_element(By.TAG_NAME, 'a').click()
        self.assertEqual(self.driver.find_element(By.XPATH, '//form/table[1]/tbody/tr[4]/td[1]/input[2]').is_selected(), True)

    def test_suica_charge_default_day(self):
        now = datetime.now()
        # 前処理
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # テスト - 日付を空にして送信
        self.driver.find_element(By.ID, 's_price').send_keys('400')
        self.driver.find_element(By.XPATH, '//form[3]/table/tbody/tr[3]/td/input[@type="button"][1]').click()

        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        self.assertEqual(len(rows), 2)
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        # 今日の日付が使われていることを確認
        self.assertEqual(tds[0].text, str(now.year) + "/" + str.zfill(str(now.month), 2) + "/" + str.zfill(str(now.day), 2))
        self.assertEqual(tds[1].text, 'Suicaチャージ')
        self.assertEqual(tds[2].text, '400')
        self.assertEqual(tds[3].text, '銀行')
        self.assertEqual(tds[4].text, '交通費')

    def test_suica_charge_default_price(self):
        now = datetime.now()
        # 前処理
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # テスト - 金額を空にして送信
        self.driver.find_element(By.ID, 's_day').send_keys('5')
        self.driver.find_element(By.XPATH, '//form[3]/table/tbody/tr[3]/td/input[@type="button"][1]').click()

        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        self.assertEqual(len(rows), 2)
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, str(now.year) + "/" + str.zfill(str(now.month), 2) + "/" + '05')
        self.assertEqual(tds[1].text, 'Suicaチャージ')
        # デフォルトの3000円が使われていることを確認
        self.assertEqual(tds[2].text, '3,000')
        self.assertEqual(tds[3].text, '銀行')
        self.assertEqual(tds[4].text, '交通費')

    def test_suica_charge_all_defaults(self):
        now = datetime.now()
        # 前処理
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # テスト - 日付も金額も空で送信
        self.driver.find_element(By.XPATH, '//form[3]/table/tbody/tr[3]/td/input[@type="button"][1]').click()

        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        self.assertEqual(len(rows), 2)
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        # 今日の日付とデフォルトの3000円が使われていることを確認
        self.assertEqual(tds[0].text, str(now.year) + "/" + str.zfill(str(now.month), 2) + "/" + str.zfill(str(now.day), 2))
        self.assertEqual(tds[1].text, 'Suicaチャージ')
        self.assertEqual(tds[2].text, '3,000')
        self.assertEqual(tds[3].text, '銀行')
        self.assertEqual(tds[4].text, '交通費')

    def test_manual_add_click(self):
        now = datetime.now()
        # 前処理
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # テスト
        self.driver.find_element(By.ID, 'a_day').send_keys('5')
        self.driver.find_element(By.ID, 'a_item').send_keys('マニュアルテスト')
        self.driver.find_element(By.ID, 'a_price').send_keys('500')
        self.driver.find_element(By.XPATH, '//form[4]/table/tbody/tr[4]/td/label[2]').click()
        self.driver.find_element(By.XPATH, '//form[4]/table/tbody/tr[5]/td/label[2]').click()
        self.driver.find_element(By.XPATH, '//form[4]/table/tbody/tr[6]/td/label[2]').click()
        self.driver.find_element(By.XPATH, '//form[4]/input[@type="button"]').click()

        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        self.assertEqual(len(rows), 2)
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, str(now.year) + "/" + str.zfill(str(now.month), 2) + "/" + '05')
        self.assertEqual(tds[1].text, 'マニュアルテスト')
        self.assertEqual(tds[2].text, '500')
        self.assertEqual(tds[3].text, '現金')
        self.assertEqual(tds[4].text, '必需品')
        self.assertEqual(Color.from_string(rows[1].value_of_css_property('background-color')), Color.from_string('rgba(0, 0, 0, 0)'))
        # direction確認
        tds[5].find_element(By.TAG_NAME, 'a').click()
        self.assertEqual(self.driver.find_element(By.XPATH, '//form/table[1]/tbody/tr[4]/td[1]/input[2]').is_selected(), True)

    def test_manual_add_year(self):
        now = datetime.now()
        # 前処理
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # テスト
        self.driver.find_element(By.ID, 'a_day').send_keys('5')
        self.driver.find_element(By.ID, 'a_item').send_keys('マニュアルテスト')
        self.driver.find_element(By.ID, 'a_price').send_keys('500')
        self.driver.find_element(By.ID, 'a_year').send_keys(Keys.RETURN)

        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        self.assertEqual(len(rows), 2)
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, str(now.year) + "/" + str.zfill(str(now.month), 2) + "/" + '05')
        self.assertEqual(tds[1].text, 'マニュアルテスト')
        self.assertEqual(tds[2].text, '500')
        self.assertEqual(tds[3].text, '銀行')
        self.assertEqual(tds[4].text, '食費')
        self.assertEqual(Color.from_string(rows[1].value_of_css_property('background-color')), Color.from_string('rgba(0, 0, 0, 0)'))
        # direction確認
        tds[5].find_element(By.TAG_NAME, 'a').click()
        self.assertEqual(self.driver.find_element(By.XPATH, '//form/table[1]/tbody/tr[4]/td[1]/input[2]').is_selected(), False)

    def test_manual_add_month(self):
        now = datetime.now()
        # 前処理
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # テスト
        self.driver.find_element(By.ID, 'a_day').send_keys('5')
        self.driver.find_element(By.ID, 'a_item').send_keys('マニュアルテスト')
        self.driver.find_element(By.ID, 'a_price').send_keys('500')
        self.driver.find_element(By.ID, 'a_month').send_keys(Keys.RETURN)

        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        self.assertEqual(len(rows), 2)
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, str(now.year) + "/" + str.zfill(str(now.month), 2) + "/" + '05')
        self.assertEqual(tds[1].text, 'マニュアルテスト')
        self.assertEqual(tds[2].text, '500')
        self.assertEqual(tds[3].text, '銀行')
        self.assertEqual(tds[4].text, '食費')
        self.assertEqual(Color.from_string(rows[1].value_of_css_property('background-color')), Color.from_string('rgba(0, 0, 0, 0)'))
        # direction確認
        tds[5].find_element(By.TAG_NAME, 'a').click()
        self.assertEqual(self.driver.find_element(By.XPATH, '//form/table[1]/tbody/tr[4]/td[1]/input[2]').is_selected(), False)

    def test_manual_add_day(self):
        now = datetime.now()
        # 前処理
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # テスト
        self.driver.find_element(By.ID, 'a_day').send_keys('5')
        self.driver.find_element(By.ID, 'a_item').send_keys('マニュアルテスト')
        self.driver.find_element(By.ID, 'a_price').send_keys('500')
        self.driver.find_element(By.ID, 'a_day').send_keys(Keys.RETURN)

        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        self.assertEqual(len(rows), 2)
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, str(now.year) + "/" + str.zfill(str(now.month), 2) + "/" + '05')
        self.assertEqual(tds[1].text, 'マニュアルテスト')
        self.assertEqual(tds[2].text, '500')
        self.assertEqual(tds[3].text, '銀行')
        self.assertEqual(tds[4].text, '食費')
        self.assertEqual(Color.from_string(rows[1].value_of_css_property('background-color')), Color.from_string('rgba(0, 0, 0, 0)'))
        # direction確認
        tds[5].find_element(By.TAG_NAME, 'a').click()
        self.assertEqual(self.driver.find_element(By.XPATH, '//form/table[1]/tbody/tr[4]/td[1]/input[2]').is_selected(), False)

    def test_manual_add_item(self):
        now = datetime.now()
        # 前処理
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # テスト
        self.driver.find_element(By.ID, 'a_day').send_keys('5')
        self.driver.find_element(By.ID, 'a_item').send_keys('マニュアルテスト')
        self.driver.find_element(By.ID, 'a_price').send_keys('500')
        self.driver.find_element(By.ID, 'a_item').send_keys(Keys.RETURN)

        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        self.assertEqual(len(rows), 2)
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, str(now.year) + "/" + str.zfill(str(now.month), 2) + "/" + '05')
        self.assertEqual(tds[1].text, 'マニュアルテスト')
        self.assertEqual(tds[2].text, '500')
        self.assertEqual(tds[3].text, '銀行')
        self.assertEqual(tds[4].text, '食費')
        self.assertEqual(Color.from_string(rows[1].value_of_css_property('background-color')), Color.from_string('rgba(0, 0, 0, 0)'))
        # direction確認
        tds[5].find_element(By.TAG_NAME, 'a').click()
        self.assertEqual(self.driver.find_element(By.XPATH, '//form/table[1]/tbody/tr[4]/td[1]/input[2]').is_selected(), False)

    def test_manual_add_price(self):
        now = datetime.now()
        # 前処理
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # テスト
        self.driver.find_element(By.ID, 'a_day').send_keys('5')
        self.driver.find_element(By.ID, 'a_item').send_keys('マニュアルテスト')
        self.driver.find_element(By.ID, 'a_price').send_keys('500')
        self.driver.find_element(By.ID, 'a_price').send_keys(Keys.RETURN)

        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        self.assertEqual(len(rows), 2)
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, str(now.year) + "/" + str.zfill(str(now.month), 2) + "/" + '05')
        self.assertEqual(tds[1].text, 'マニュアルテスト')
        self.assertEqual(tds[2].text, '500')
        self.assertEqual(tds[3].text, '銀行')
        self.assertEqual(tds[4].text, '食費')
        self.assertEqual(Color.from_string(rows[1].value_of_css_property('background-color')), Color.from_string('rgba(0, 0, 0, 0)'))
        # direction確認
        tds[5].find_element(By.TAG_NAME, 'a').click()
        self.assertEqual(self.driver.find_element(By.XPATH, '//form/table[1]/tbody/tr[4]/td[1]/input[2]').is_selected(), False)

    def test_manual_add_tmp(self):
        now = datetime.now()
        # 前処理
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # テスト
        self.driver.find_element(By.ID, 'a_day').send_keys('5')
        self.driver.find_element(By.ID, 'a_item').send_keys('マニュアルテスト')
        self.driver.find_element(By.ID, 'a_price').send_keys('500')
        self.driver.find_element(By.XPATH, '//form[4]/table/tbody/tr[7]/td/label[2]').click()
        self.driver.find_element(By.XPATH, '//form[4]/input[@type="button"]').click()

        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        self.assertEqual(len(rows), 2)
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, str(now.year) + "/" + str.zfill(str(now.month), 2) + "/" + '05')
        self.assertEqual(tds[1].text, 'マニュアルテスト')
        self.assertEqual(tds[2].text, '500')
        self.assertEqual(tds[3].text, '銀行')
        self.assertEqual(tds[4].text, '立替')
        self.assertEqual(Color.from_string(rows[1].value_of_css_property('background-color')), Color.from_string('rgba(0, 0, 0, 0)'))
        # direction確認
        tds[5].find_element(By.TAG_NAME, 'a').click()
        self.assertEqual(self.driver.find_element(By.XPATH, '//form/table[1]/tbody/tr[4]/td[1]/input[2]').is_selected(), False)

    def test_add_formula_normal_form(self):
        '''通常追加フォームで数式を入力できることを確認（addページ）'''
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # 初期確認
        self._location(self.live_server_url + reverse('moneybook:index'))
        initial_count = len(self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr'))

        # 通常追加フォームで数式 =50*3 → 150
        self._location(self.live_server_url + reverse('moneybook:add'))
        self.driver.find_element(By.ID, 'a_day').send_keys('15')
        self.driver.find_element(By.ID, 'a_item').send_keys('add数式')
        self.driver.find_element(By.ID, 'a_price').send_keys('=50*3')
        self.driver.find_element(By.XPATH, '//section/form[4]/input[@value="追加"]').click()
        time.sleep(2)

        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        self.assertEqual(len(rows), initial_count + 1)
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[1].text, 'add数式')
        self.assertEqual(tds[2].text, '150')

    def test_add_formula_internal_transfer(self):
        '''内部移動フォームで数式を入力できることを確認（addページ）'''
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # 初期確認
        self._location(self.live_server_url + reverse('moneybook:index'))
        initial_count = len(self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr'))

        # 内部移動で数式 =100+200 → 300
        self._location(self.live_server_url + reverse('moneybook:add'))
        self.driver.find_element(By.ID, 'm_day').send_keys('16')
        self.driver.find_element(By.ID, 'm_item').send_keys('add数式')
        self.driver.find_element(By.ID, 'm_price').send_keys('=100+200')
        self.driver.find_element(By.XPATH, '//section/form[2]/input[@value="追加"]').click()
        time.sleep(2)

        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        # 内部移動は2件追加される
        self.assertEqual(len(rows), initial_count + 2)
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[1].text, 'add数式')
        self.assertEqual(tds[2].text, '300')

    def test_add_formula_charge(self):
        '''チャージフォームで数式を入力できることを確認（addページ）'''
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        # 初期確認
        self._location(self.live_server_url + reverse('moneybook:index'))
        initial_count = len(self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr'))

        # チャージで数式 =1000/4 → 250
        self._location(self.live_server_url + reverse('moneybook:add'))
        self.driver.find_element(By.ID, 'c_day').send_keys('17')
        self.driver.find_element(By.ID, 'c_price').send_keys('=1000/4')
        self.driver.find_element(By.XPATH, '//section/form[1]/input[@value="追加"]').click()
        time.sleep(2)

        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        # チャージも2件追加される
        self.assertEqual(len(rows), initial_count + 2)
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[2].text, '250')
