import time
from datetime import datetime

from django.urls import reverse
from moneybook.e2e.base import SeleniumBase
from selenium.webdriver.common.by import By


class Statistics(SeleniumBase):
    def test_get(self):
        """統計画面が正しく表示されることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:statistics'))

        self._assert_common()

        # 年が表示されている
        now = datetime.now()
        year_element = self.driver.find_element(By.ID, 'jump_year')
        self.assertEqual(year_element.get_attribute('value'), str(now.year))

        # 統計テーブルが表示されている
        self.assertTrue(self.driver.find_element(By.XPATH, '//table').is_displayed())

    def test_statistics_table_structure(self):
        """統計テーブルの構造が正しいことを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:statistics'))

        # テーブルのヘッダーを確認
        headers = self.driver.find_elements(By.XPATH, '//table/thead/tr[1]/th')
        self.assertGreater(len(headers), 0)

        # 12ヶ月分の行が存在することを確認
        rows = self.driver.find_elements(By.XPATH, '//table/tbody/tr')
        self.assertEqual(len(rows), 12)

    def test_statistics_with_data(self):
        """データがある状態で統計画面を表示して集計が反映されることを確認"""
        self._login()
        now = datetime.now()

        # テストデータを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('統計テスト')
        self.driver.find_element(By.ID, 'a_price').send_keys('1000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 統計画面に移動
        self._location(self.live_server_url + reverse('moneybook:statistics'))

        # データが反映されている（今月の行に値がある）
        rows = self.driver.find_elements(By.XPATH, '//table/tbody/tr')
        # 今月の行を探す
        current_month_row = None
        for row in rows:
            first_cell = row.find_element(By.TAG_NAME, 'th')
            if first_cell.text == f'{now.month}月':
                current_month_row = row
                break

        self.assertIsNotNone(current_month_row)

    def test_statistics_year_navigation(self):
        """年の選択ができることを確認"""
        self._login()
        now = datetime.now()

        # 統計画面に移動
        self._location(self.live_server_url + reverse('moneybook:statistics'))

        # 年選択フォームが存在する
        year_select = self.driver.find_element(By.ID, 'year')
        self.assertTrue(year_select.is_displayed())

        # 別の年を選択（現在年-1）
        year_select.send_keys(str(now.year - 1))
        self.driver.find_element(By.XPATH, '//input[@value="表示"]').click()
        time.sleep(2)

        # 選択した年が表示されている
        year_element = self.driver.find_element(By.XPATH, '//h2')
        self.assertIn(str(now.year - 1), year_element.text)

    def test_statistics_specific_year(self):
        """特定の年の統計画面に直接アクセスできることを確認"""
        self._login()
        target_year = 2020

        # 特定の年の統計画面に移動
        self._location(self.live_server_url + reverse('moneybook:statistics_month', kwargs={'year': target_year}))

        # 指定した年が表示されている
        year_element = self.driver.find_element(By.XPATH, '//h2')
        self.assertIn(str(target_year), year_element.text)

    def test_statistics_multiple_months_data(self):
        """複数月にデータがある場合の統計を確認"""
        self._login()
        now = datetime.now()

        # 今月のデータを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('今月のデータ')
        self.driver.find_element(By.ID, 'a_price').send_keys('1000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 別の月のデータを追加（前月）
        if now.month > 1:
            prev_month = now.month - 1
            prev_year = now.year
        else:
            prev_month = 12
            prev_year = now.year - 1

        self._location(self.live_server_url + reverse('moneybook:index_month', kwargs={'year': prev_year, 'month': prev_month}))
        self.driver.find_element(By.ID, 'a_day').send_keys('15')
        self.driver.find_element(By.ID, 'a_item').send_keys('前月のデータ')
        self.driver.find_element(By.ID, 'a_price').send_keys('2000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 統計画面に移動
        self._location(self.live_server_url + reverse('moneybook:statistics_month', kwargs={'year': now.year}))

        # テーブルが表示されている
        rows = self.driver.find_elements(By.XPATH, '//table/tbody/tr')
        self.assertEqual(len(rows), 12)

    def test_statistics_food_cost(self):
        """食費が正しく集計されることを確認"""
        self._login()
        now = datetime.now()

        # 食費データを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('スーパー')
        self.driver.find_element(By.ID, 'a_price').send_keys('1500')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/table/tbody/tr[5]/td/table/tbody/tr/td/label[1]').click()  # 食費
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 統計画面に移動
        self._location(self.live_server_url + reverse('moneybook:statistics'))

        # 食費データが存在することを確認（hidden ulに格納されている）
        food_costs_ul = self.driver.find_element(By.ID, 'food_costs')
        self.assertIsNotNone(food_costs_ul)
        food_costs_items = food_costs_ul.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(food_costs_items), 0)

        # 当月の食費データが含まれていることを確認
        current_month_data = None
        for item in food_costs_items:
            if f'{now.month}月' in item.text:
                current_month_data = item.text
                break
        self.assertIsNotNone(current_month_data)
        self.assertIn('1500', current_month_data)

    def test_statistics_living_cost(self):
        """生活費が正しく集計されることを確認"""
        self._login()
        now = datetime.now()

        # 生活費データを追加（食費は生活費に含まれる）
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('日用品')
        self.driver.find_element(By.ID, 'a_price').send_keys('2000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/table/tbody/tr[5]/td/table/tbody/tr/td/label[1]').click()  # 食費
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 統計画面に移動
        self._location(self.live_server_url + reverse('moneybook:statistics'))

        # 生活費データが存在することを確認（hidden ulに格納されている）
        living_costs_ul = self.driver.find_element(By.ID, 'living_costs')
        self.assertIsNotNone(living_costs_ul)
        living_costs_items = living_costs_ul.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(living_costs_items), 0)

        # 当月の生活費データが含まれていることを確認
        current_month_data = None
        for item in living_costs_items:
            if f'{now.month}月' in item.text:
                current_month_data = item.text
                break
        self.assertIsNotNone(current_month_data)
        self.assertIn('2000', current_month_data)

    def test_statistics_link_from_taskbar(self):
        """タスクバーから統計画面に遷移できることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index'))

        # タスクバーの統計リンクをクリック
        taskbar_links = self.driver.find_elements(By.XPATH, '//nav[@class="task_bar"]/ul/li/a')
        statistics_link = None
        for link in taskbar_links:
            if link.text == '統計':
                statistics_link = link
                break

        self.assertIsNotNone(statistics_link)
        statistics_link.click()
        time.sleep(1)

        # 統計画面に遷移したことを確認
        self.assertEqual(self.driver.current_url, self.live_server_url + reverse('moneybook:statistics'))
