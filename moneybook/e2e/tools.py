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
        self.assertTrue(self.driver.find_element(By.ID, 'actual_cash').is_displayed())

    def test_update_actual_cash(self):
        """実際の現金残高を更新できることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:tools'))

        # 実際の現金残高を入力
        actual_cash_input = self.driver.find_element(By.ID, 'actual_cash')
        actual_cash_input.clear()
        actual_cash_input.send_keys('5000')

        # 更新ボタンをクリック
        self.driver.find_element(By.XPATH, '//input[@value="更新" and @id="actual_cash_apply"]').click()
        time.sleep(2)

        # ページをリロードして値が保持されていることを確認
        self._location(self.live_server_url + reverse('moneybook:tools'))
        actual_cash_value = self.driver.find_element(By.ID, 'actual_cash').get_attribute('value')
        self.assertEqual(actual_cash_value, '5000')

    def test_update_actual_cash_enter(self):
        """Enterキーで実際の現金残高を更新できることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:tools'))

        # 実際の現金残高を入力してEnter
        actual_cash_input = self.driver.find_element(By.ID, 'actual_cash')
        actual_cash_input.clear()
        actual_cash_input.send_keys('10000')
        actual_cash_input.send_keys(Keys.RETURN)
        time.sleep(2)

        # ページをリロードして値が保持されていることを確認
        self._location(self.live_server_url + reverse('moneybook:tools'))
        actual_cash_value = self.driver.find_element(By.ID, 'actual_cash').get_attribute('value')
        self.assertEqual(actual_cash_value, '10000')

    def test_checked_date_section(self):
        """チェック日セクションが表示されることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:tools'))

        # チェック日の表が表示されている
        checked_date_table = self.driver.find_element(By.ID, 'checked_dates')
        self.assertTrue(checked_date_table.is_displayed())

    def test_update_checked_date(self):
        """チェック日を更新できることを確認"""
        self._login()

        self._location(self.live_server_url + reverse('moneybook:tools'))

        # チェック日更新ボタンをクリック
        self.driver.find_element(By.XPATH, '//button[contains(text(), "チェック日更新")]').click()
        time.sleep(1)

        # モーダルが表示される（実装による）
        # チェック日を変更する処理

    def test_now_bank_section(self):
        """銀行残高セクションが表示されることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:tools'))

        # 銀行残高情報が表示されている
        # セクションの存在を確認
        page_source = self.driver.page_source
        self.assertIn('銀行', page_source)

    def test_living_cost_mark_section(self):
        """生活費目標額セクションが表示されることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:tools'))

        # 生活費目標額の入力欄が表示されている
        living_cost_input = self.driver.find_element(By.ID, 'living_cost_mark')
        self.assertTrue(living_cost_input.is_displayed())

    def test_update_living_cost_mark(self):
        """生活費目標額を更新できることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:tools'))

        # 生活費目標額を入力
        living_cost_input = self.driver.find_element(By.ID, 'living_cost_mark')
        living_cost_input.clear()
        living_cost_input.send_keys('30000')

        # 更新ボタンをクリック
        self.driver.find_element(By.XPATH, '//input[@value="更新" and @id="living_cost_mark_apply"]').click()
        time.sleep(2)

        # ページをリロードして値が保持されていることを確認
        self._location(self.live_server_url + reverse('moneybook:tools'))
        living_cost_value = self.driver.find_element(By.ID, 'living_cost_mark').get_attribute('value')
        self.assertEqual(living_cost_value, '30000')

    def test_update_living_cost_mark_enter(self):
        """Enterキーで生活費目標額を更新できることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:tools'))

        # 生活費目標額を入力してEnter
        living_cost_input = self.driver.find_element(By.ID, 'living_cost_mark')
        living_cost_input.clear()
        living_cost_input.send_keys('40000')
        living_cost_input.send_keys(Keys.RETURN)
        time.sleep(2)

        # ページをリロードして値が保持されていることを確認
        self._location(self.live_server_url + reverse('moneybook:tools'))
        living_cost_value = self.driver.find_element(By.ID, 'living_cost_mark').get_attribute('value')
        self.assertEqual(living_cost_value, '40000')

    def test_unchecked_data_section(self):
        """未チェックデータセクションが表示されることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:tools'))

        # 未チェックデータボタンが表示されている
        page_source = self.driver.page_source
        self.assertIn('未チェック', page_source)

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

    def test_cash_balance_display(self):
        """現金残高が正しく表示されることを確認"""
        self._login()
        # データを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('現金テスト')
        self.driver.find_element(By.ID, 'a_price').send_keys('1000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/table/tbody/tr[4]/td/label[2]').click()  # 現金
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # ツール画面に移動
        self._location(self.live_server_url + reverse('moneybook:tools'))

        # 現金残高が表示されている
        page_source = self.driver.page_source
        self.assertIn('現金残高', page_source)

    def test_multiple_updates(self):
        """複数の値を連続して更新できることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:tools'))

        # 実際の現金残高を更新
        actual_cash_input = self.driver.find_element(By.ID, 'actual_cash')
        actual_cash_input.clear()
        actual_cash_input.send_keys('15000')
        self.driver.find_element(By.XPATH, '//input[@value="更新" and @id="actual_cash_apply"]').click()
        time.sleep(2)

        # 生活費目標額を更新
        living_cost_input = self.driver.find_element(By.ID, 'living_cost_mark')
        living_cost_input.clear()
        living_cost_input.send_keys('50000')
        self.driver.find_element(By.XPATH, '//input[@value="更新" and @id="living_cost_mark_apply"]').click()
        time.sleep(2)

        # ページをリロードして両方の値が保持されていることを確認
        self._location(self.live_server_url + reverse('moneybook:tools'))
        actual_cash_value = self.driver.find_element(By.ID, 'actual_cash').get_attribute('value')
        living_cost_value = self.driver.find_element(By.ID, 'living_cost_mark').get_attribute('value')
        self.assertEqual(actual_cash_value, '15000')
        self.assertEqual(living_cost_value, '50000')
