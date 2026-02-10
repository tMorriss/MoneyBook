import time
from datetime import datetime

from django.urls import reverse
from moneybook.selenium.base import SeleniumBase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Edit(SeleniumBase):
    def test_get(self):
        '''編集画面が正しく表示されることを確認'''
        self._login()
        # まずデータを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('編集テスト')
        self.driver.find_element(By.ID, 'a_price').send_keys('1000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 編集画面に移動
        self.driver.find_element(By.XPATH, '//*[@id="transactions"]/table/tbody/tr[2]/td[6]/a').click()
        time.sleep(1)

        self._assert_common()

        # フォームの値を確認
        now = datetime.now()
        year_value = self.driver.find_element(By.ID, 'year').get_attribute('value')
        month_value = self.driver.find_element(By.ID, 'month').get_attribute('value')
        day_value = self.driver.find_element(By.ID, 'day').get_attribute('value')
        self.assertEqual(year_value, str(now.year))
        self.assertEqual(month_value, str(now.month).zfill(2))
        self.assertEqual(day_value, '10')
        self.assertEqual(self.driver.find_element(By.ID, 'item').get_attribute('value'), '編集テスト')
        self.assertEqual(self.driver.find_element(By.ID, 'price').get_attribute('value'), '1000')

    def test_edit_item(self):
        '''項目名を編集できることを確認'''
        self._login()
        # データを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('編集前')
        self.driver.find_element(By.ID, 'a_price').send_keys('2000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 編集画面に移動
        self.driver.find_element(By.XPATH, '//*[@id="transactions"]/table/tbody/tr[2]/td[6]/a').click()
        time.sleep(1)

        # 項目名を変更
        item_input = self.driver.find_element(By.ID, 'item')
        item_input.clear()
        item_input.send_keys('編集後')
        self.driver.find_element(By.XPATH, '//input[@value="更新"]').click()
        time.sleep(2)

        # トップに戻って確認
        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[1].text, '編集後')

    def test_edit_price(self):
        '''金額を編集できることを確認'''
        self._login()
        # データを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('金額変更テスト')
        self.driver.find_element(By.ID, 'a_price').send_keys('1000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 編集画面に移動
        self.driver.find_element(By.XPATH, '//*[@id="transactions"]/table/tbody/tr[2]/td[6]/a').click()
        time.sleep(1)

        # 金額を変更
        price_input = self.driver.find_element(By.ID, 'price')
        price_input.clear()
        price_input.send_keys('5000')
        self.driver.find_element(By.XPATH, '//input[@value="更新"]').click()
        time.sleep(2)

        # トップに戻って確認
        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[2].text, '5,000')

    def test_edit_date(self):
        '''日付を編集できることを確認'''
        self._login()
        # データを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('日付変更テスト')
        self.driver.find_element(By.ID, 'a_price').send_keys('3000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 編集画面に移動
        self.driver.find_element(By.XPATH, '//*[@id="transactions"]/table/tbody/tr[2]/td[6]/a').click()
        time.sleep(1)

        # 日付を変更
        now = datetime.now()
        day_input = self.driver.find_element(By.ID, 'day')
        day_input.clear()
        day_input.send_keys('15')
        self.driver.find_element(By.XPATH, '//input[@value="更新"]').click()
        time.sleep(2)

        # トップに戻って確認
        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, f"{now.year}/{str(now.month).zfill(2)}/15")

    def test_edit_method(self):
        '''支払い方法を編集できることを確認'''
        self._login()
        # データを追加（銀行で登録）
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('方法変更テスト')
        self.driver.find_element(By.ID, 'a_price').send_keys('4000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/table/tbody/tr[4]/td/label[1]').click()  # 銀行
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 編集画面に移動
        self.driver.find_element(By.XPATH, '//*[@id="transactions"]/table/tbody/tr[2]/td[6]/a').click()
        time.sleep(1)

        # 支払い方法を現金に変更
        self.driver.find_element(By.XPATH, '//form/table[1]/tbody/tr[5]/td[1]/label[2]').click()
        self.driver.find_element(By.XPATH, '//input[@value="更新"]').click()
        time.sleep(2)

        # トップに戻って確認
        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[3].text, '現金')

    def test_edit_category(self):
        '''カテゴリーを編集できることを確認'''
        self._login()
        # データを追加（食費で登録）
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('カテゴリー変更テスト')
        self.driver.find_element(By.ID, 'a_price').send_keys('6000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/table/tbody/tr[5]/td/table/tbody/tr/td/label[1]').click()  # 食費
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 編集画面に移動
        self.driver.find_element(By.XPATH, '//*[@id="transactions"]/table/tbody/tr[2]/td[6]/a').click()
        time.sleep(1)

        # カテゴリーを必需品に変更
        self.driver.find_element(By.XPATH, '//form/table[1]/tbody/tr[6]/td[1]/label[2]').click()
        self.driver.find_element(By.XPATH, '//input[@value="更新"]').click()
        time.sleep(2)

        # トップに戻って確認
        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[4].text, '必需品')

    def test_edit_formula_price(self):
        '''編集画面で金額入力欄に数式を入力できることを確認'''
        self._login()
        # データを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('数式編集テスト')
        self.driver.find_element(By.ID, 'a_price').send_keys('1000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 編集画面に移動
        self.driver.find_element(By.XPATH, '//*[@id="transactions"]/table/tbody/tr[2]/td[6]/a').click()
        time.sleep(1)

        # 金額を数式で変更 =200*5 → 1000
        price_input = self.driver.find_element(By.ID, 'price')
        price_input.clear()
        price_input.send_keys('=200*5')
        self.driver.find_element(By.XPATH, '//input[@value="更新"]').click()
        time.sleep(2)

        # トップに戻って確認
        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[2].text, '1,000')

    def test_edit_enter_date(self):
        '''日付入力欄でEnterキーを押すと更新されることを確認'''
        self._login()
        # データを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('Enter日付')
        self.driver.find_element(By.ID, 'a_price').send_keys('2000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 編集画面に移動
        self.driver.find_element(By.XPATH, '//*[@id="transactions"]/table/tbody/tr[2]/td[6]/a').click()
        time.sleep(1)

        # 日付を変更してEnter
        now = datetime.now()
        day_input = self.driver.find_element(By.ID, 'day')
        day_input.clear()
        day_input.send_keys('20')
        day_input.send_keys(Keys.RETURN)
        time.sleep(2)

        # トップに戻って確認
        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, f"{now.year}/{str(now.month).zfill(2)}/20")

    def test_edit_enter_item(self):
        '''項目入力欄でEnterキーを押すと更新されることを確認'''
        self._login()
        # データを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('Enter項目前')
        self.driver.find_element(By.ID, 'a_price').send_keys('3000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 編集画面に移動
        self.driver.find_element(By.XPATH, '//*[@id="transactions"]/table/tbody/tr[2]/td[6]/a').click()
        time.sleep(1)

        # 項目を変更してEnter
        item_input = self.driver.find_element(By.ID, 'item')
        item_input.clear()
        item_input.send_keys('Enter項目後')
        item_input.send_keys(Keys.RETURN)
        time.sleep(2)

        # トップに戻って確認
        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[1].text, 'Enter項目後')

    def test_edit_enter_price(self):
        '''金額入力欄でEnterキーを押すと更新されることを確認'''
        self._login()
        # データを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('Enter金額')
        self.driver.find_element(By.ID, 'a_price').send_keys('4000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 編集画面に移動
        self.driver.find_element(By.XPATH, '//*[@id="transactions"]/table/tbody/tr[2]/td[6]/a').click()
        time.sleep(1)

        # 金額を変更してEnter
        price_input = self.driver.find_element(By.ID, 'price')
        price_input.clear()
        price_input.send_keys('8000')
        price_input.send_keys(Keys.RETURN)
        time.sleep(2)

        # トップに戻って確認
        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[2].text, '8,000')

    def test_edit_invalid_pk(self):
        '''存在しないIDで編集画面にアクセスするとトップにリダイレクトされることを確認'''
        self._login()
        self._location(self.live_server_url + reverse('moneybook:edit', kwargs={'pk': 999999}))
        time.sleep(1)

        # トップにリダイレクトされる
        self.assertEqual(self.driver.current_url, self.live_server_url + reverse('moneybook:index'))
