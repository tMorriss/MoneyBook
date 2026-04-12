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
