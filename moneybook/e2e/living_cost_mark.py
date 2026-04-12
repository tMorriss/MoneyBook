import time

from django.urls import reverse
from moneybook.e2e.base import SeleniumBase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


class LivingCostMark(SeleniumBase):
    def test_get(self):
        """生活費目標一覧画面が正しく表示されることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:living_cost_mark'))

        self._assert_common()
        self.assertTrue(self.driver.find_element(By.XPATH, '//h1[text()="生活費目標一覧"]').is_displayed())

        # データの表示確認 (fixtureから)
        cells = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//table[@class="tbl-data tbl-boarder"]/tbody/tr[1]/td'))
        )
        self.assertEqual(cells[0].text, '2000/01')
        self.assertEqual(cells[2].text, '1,000')

    def test_edit_navigation(self):
        """一覧画面から編集画面に遷移できることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:living_cost_mark'))

        # 編集ボタンをクリック
        edit_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@value="編集"]'))
        )
        self.driver.execute_script('arguments[0].click();', edit_btn)

        # 編集画面に遷移したことを確認
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h1[text()="生活費目標編集"]'))
        )
        self.assertEqual(self.driver.current_url, self.live_server_url + reverse('moneybook:living_cost_mark_edit'))

    def test_add_row(self):
        """編集画面で行を追加できることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:living_cost_mark_edit'))

        # 初期状態の行数を取得
        initial_rows = len(self.driver.find_elements(By.CSS_SELECTOR, '#mark_table_body tr'))

        # 行を追加ボタンをクリック
        add_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'btn_add_row'))
        )
        self.driver.execute_script('arguments[0].click();', add_btn)

        # 行が増えていることを確認
        WebDriverWait(self.driver, 10).until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, '#mark_table_body tr')) == initial_rows + 1
        )

    def test_update_living_cost_mark(self):
        """生活費目標を更新できることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:living_cost_mark_edit'))

        # 全ての行を削除（クリーンな状態からテスト）
        self.driver.execute_script("document.querySelectorAll('#mark_table_body .btn-delete-row').forEach(el => el.click())")

        # 行が消えるのを待つ
        WebDriverWait(self.driver, 10).until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, '#mark_table_body tr')) == 0
        )

        # 行を追加
        add_btn = self.driver.find_element(By.ID, 'btn_add_row')
        self.driver.execute_script('arguments[0].click();', add_btn)

        # 行が表示されるまで待機
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mark_table_body tr'))
        )

        rows = self.driver.find_elements(By.CSS_SELECTOR, '#mark_table_body tr')
        start_date_input = rows[0].find_element(By.CSS_SELECTOR, 'input[type="date"][name^="start_date_"]')
        price_input = rows[0].find_element(By.CSS_SELECTOR, 'input[type="text"][name^="price_"]')

        # 日付と価格を入力
        self.driver.execute_script("arguments[0].value = '2024-01-01';", start_date_input)
        self.driver.execute_script("arguments[0].value = '150000';", price_input)

        # ブラウザ側バリデーションを避ける
        self.driver.execute_script("document.querySelectorAll('input').forEach(el => el.required = false)")

        # 更新ボタンをクリック
        submit_btn = self.driver.find_element(By.CSS_SELECTOR, 'form button[type="submit"]')
        self.driver.execute_script('arguments[0].click();', submit_btn)

        # 一覧画面に戻り、値が反映されていることを確認
        try:
            WebDriverWait(self.driver, 20).until(
                EC.url_to_be(self.live_server_url + reverse('moneybook:living_cost_mark'))
            )
        except TimeoutException:
            # 失敗した場合はエラーメッセージを確認して表示する
            error_msg = ""
            errors = self.driver.find_elements(By.CSS_SELECTOR, 'p[style="color: red;"]')
            if errors:
                error_msg = f" Validation Error on page: {errors[0].text}"
            raise TimeoutException(f"Timed out waiting for redirect to list page. Current URL: {self.driver.current_url}.{error_msg}")

        # 反映された値を確認
        cells = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//table[@class="tbl-data tbl-boarder"]/tbody/tr[1]/td'))
        )
        self.assertEqual(cells[0].text, '2024/01')
        self.assertEqual(cells[2].text, '150,000')
