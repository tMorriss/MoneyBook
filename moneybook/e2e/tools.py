import time

from django.urls import reverse
from moneybook.e2e.base import SeleniumBase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Tools(SeleniumBase):
    def test_get(self):
        """ツール画面が正しく表示されることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:tools'))

        self._assert_common()

    def test_actual_cash_section(self):
        """実際の現金残高セクションが表示されることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:tools'))

        # 実際の現金残高の入力欄が表示されている
        self.assertTrue(self.driver.find_element(By.ID, 'actual_balance').is_displayed())

    def test_update_actual_cash(self):
        """実際の現金残高を更新できることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:tools'))

        # 実際の現金残高を入力
        actual_cash_input = self.driver.find_element(By.ID, 'actual_balance')
        actual_cash_input.clear()
        actual_cash_input.send_keys('5000')

        # 計算ボタンをクリック
        self.driver.find_element(By.XPATH, '//input[@value="計算"]').click()
        time.sleep(2)

        # ページをリロードして値が保持されていることを確認
        self._location(self.live_server_url + reverse('moneybook:tools'))
        actual_cash_value = self.driver.find_element(By.ID, 'actual_balance').get_attribute('value')
        self.assertEqual(actual_cash_value, '5,000')

    def test_update_actual_cash_enter(self):
        """Enterキーで実際の現金残高を更新できることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:tools'))

        # 実際の現金残高を入力してEnter
        actual_cash_input = self.driver.find_element(By.ID, 'actual_balance')
        actual_cash_input.clear()
        actual_cash_input.send_keys('10000')
        actual_cash_input.send_keys(Keys.RETURN)
        time.sleep(2)

        # ページをリロードして値が保持されていることを確認
        self._location(self.live_server_url + reverse('moneybook:tools'))
        actual_cash_value = self.driver.find_element(By.ID, 'actual_balance').get_attribute('value')
        self.assertEqual(actual_cash_value, '10,000')

    def test_checked_date_section(self):
        """チェック日セクションが表示されることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:tools'))

        # チェック日の表が表示されている
        checked_date_table = self.driver.find_element(By.ID, 'checked-date')
        self.assertTrue(checked_date_table.is_displayed())

    def test_update_checked_date(self):
        """チェック日の入力フィールドが表示されることを確認"""
        self._login()

        self._location(self.live_server_url + reverse('moneybook:tools'))

        # チェック日の入力フィールドが表示されている
        self.assertTrue(self.driver.find_element(By.ID, 'check_year').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'check_month').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'check_day').is_displayed())

    def test_living_cost_mark_section(self):
        """生活費目標額セクションが表示されることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:tools'))

        # 生活費目標額の入力欄が表示されている
        living_cost_input = self.driver.find_element(By.ID, 'txt_living_cost')
        self.assertTrue(living_cost_input.is_displayed())

    def test_update_living_cost_mark(self):
        """生活費目標額を更新できることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:tools'))

        # 生活費目標額を入力
        living_cost_input = self.driver.find_element(By.ID, 'txt_living_cost')
        living_cost_input.clear()
        living_cost_input.send_keys('30000')

        # 更新ボタンをクリック
        update_buttons = self.driver.find_elements(By.XPATH, '//input[@value="更新"]')
        update_buttons[0].click()
        time.sleep(2)

        # ページをリロードして値が保持されていることを確認
        self._location(self.live_server_url + reverse('moneybook:tools'))
        living_cost_value = self.driver.find_element(By.ID, 'txt_living_cost').get_attribute('value')
        self.assertEqual(living_cost_value, '30,000')

    def test_update_living_cost_mark_enter(self):
        """Enterキーで生活費目標額を更新できることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:tools'))

        # 生活費目標額を入力してEnter
        living_cost_input = self.driver.find_element(By.ID, 'txt_living_cost')
        living_cost_input.clear()
        living_cost_input.send_keys('40000')
        living_cost_input.send_keys(Keys.RETURN)
        time.sleep(2)

        # ページをリロードして値が保持されていることを確認
        self._location(self.live_server_url + reverse('moneybook:tools'))
        living_cost_value = self.driver.find_element(By.ID, 'txt_living_cost').get_attribute('value')
        self.assertEqual(living_cost_value, '40,000')

    def test_link_from_taskbar(self):
        """タスクバーからツール画面に遷移できることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index'))

        # タスクバーのツールリンクをクリック
        taskbar_links = self.driver.find_elements(By.XPATH, '//nav[@class="task_bar"]/ul/li/a')
        tools_link = None
        for link in taskbar_links:
            if link.text == 'ツール':
                tools_link = link
                break

        self.assertIsNotNone(tools_link)
        tools_link.click()
        time.sleep(1)

        # ツール画面に遷移したことを確認
        self.assertEqual(self.driver.current_url, self.live_server_url + reverse('moneybook:tools'))

    def test_multiple_updates(self):
        """複数の値を連続して更新できることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:tools'))

        # 実際の現金残高を更新
        actual_cash_input = self.driver.find_element(By.ID, 'actual_balance')
        actual_cash_input.clear()
        actual_cash_input.send_keys('15000')
        self.driver.find_element(By.XPATH, '//input[@value="計算"]').click()
        time.sleep(2)

        # 生活費目標額を更新
        living_cost_input = self.driver.find_element(By.ID, 'txt_living_cost')
        living_cost_input.clear()
        living_cost_input.send_keys('50000')
        # 生活費の更新ボタンをクリック（現金差額計算の後の2番目の「更新」ボタン）
        update_buttons = self.driver.find_elements(By.XPATH, '//input[@value="更新"]')
        update_buttons[0].click()
        time.sleep(2)

        # ページをリロードして両方の値が保持されていることを確認
        self._location(self.live_server_url + reverse('moneybook:tools'))
        actual_cash_value = self.driver.find_element(By.ID, 'actual_balance').get_attribute('value')
        living_cost_value = self.driver.find_element(By.ID, 'txt_living_cost').get_attribute('value')
        self.assertEqual(actual_cash_value, '15,000')
        self.assertEqual(living_cost_value, '50,000')
