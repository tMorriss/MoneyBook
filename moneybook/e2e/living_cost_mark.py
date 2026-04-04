import time

from django.urls import reverse
from moneybook.e2e.base import SeleniumBase
from selenium.webdriver.common.by import By


class LivingCostMark(SeleniumBase):
    def test_get(self):
        """生活費目標一覧画面が正しく表示されることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:living_cost_mark'))

        self._assert_common()
        self.assertTrue(self.driver.find_element(By.XPATH, '//h1[text()="生活費目標一覧"]').is_displayed())

    def test_edit_navigation(self):
        """一覧画面から編集画面に遷移できることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:living_cost_mark'))

        # 編集ボタンをクリック
        self.driver.find_element(By.XPATH, '//input[@value="編集"]').click()
        time.sleep(1)

        # 編集画面に遷移したことを確認
        self.assertEqual(self.driver.current_url, self.live_server_url + reverse('moneybook:living_cost_mark_edit'))
        self.assertTrue(self.driver.find_element(By.XPATH, '//h1[text()="生活費目標編集"]').is_displayed())

    def test_add_row(self):
        """編集画面で行を追加できることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:living_cost_mark_edit'))

        # 初期状態の行数を取得
        initial_rows = len(self.driver.find_elements(By.XPATH, '//*[@id="mark_table_body"]/tr'))

        # 行を追加ボタンをクリック
        self.driver.find_element(By.ID, 'btn_add_row').click()
        time.sleep(1)

        # 行が増えていることを確認
        current_rows = len(self.driver.find_elements(By.XPATH, '//*[@id="mark_table_body"]/tr'))
        self.assertEqual(current_rows, initial_rows + 1)

    def test_update_living_cost_mark(self):
        """生活費目標を更新できることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:living_cost_mark_edit'))

        # 全ての行を削除（クリーンな状態からテスト）
        delete_buttons = self.driver.find_elements(By.CLASS_NAME, 'btn-delete-row')
        for btn in reversed(delete_buttons):
            btn.click()

        # 行を追加して入力
        self.driver.find_element(By.ID, 'btn_add_row').click()

        # 最初の行の入力フィールドを取得
        # start_date は type="date"
        # 実際には JavaScript で生成された名前になっているはず
        # セレクタを工夫
        rows = self.driver.find_elements(By.XPATH, '//*[@id="mark_table_body"]/tr')
        start_date_input = rows[0].find_element(By.XPATH, './/input[@type="date" and contains(@name, "start_date_")]')
        price_input = rows[0].find_element(By.XPATH, './/input[@type="text" and contains(@name, "price_")]')

        start_date_input.send_keys('20240101')  # YYYYMMDD形式
        price_input.send_keys('150000')

        # 更新ボタンをクリック
        self.driver.find_element(By.XPATH, '//button[text()="更新"]').click()
        time.sleep(2)

        # 一覧画面に戻り、値が反映されていることを確認
        self.assertEqual(self.driver.current_url, self.live_server_url + reverse('moneybook:living_cost_mark'))

        cells = self.driver.find_elements(By.XPATH, '//table[@class="tbl-data tbl-boarder"]/tbody/tr[1]/td')
        self.assertEqual(cells[0].text, '2024/01')
        self.assertEqual(cells[2].text, '150,000')
