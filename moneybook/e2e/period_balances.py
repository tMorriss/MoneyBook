import time
from datetime import datetime

from django.urls import reverse
from moneybook.e2e.base import SeleniumBase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class PeriodBalances(SeleniumBase):
    def test_get(self):
        """期間残高画面が正しく表示されることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:period_balances'))

        self._assert_common()

        # フォームが表示されている
        self.assertTrue(self.driver.find_element(By.ID, 'start_year').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'start_month').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'end_year').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'end_month').is_displayed())

    def test_default_period(self):
        """デフォルトの期間が表示されることを確認"""
        self._login()
        now = datetime.now()

        # 期間残高画面に移動
        self._location(self.live_server_url + reverse('moneybook:period_balances'))

        # デフォルト値が設定されている（去年1月〜今月）
        start_year = self.driver.find_element(By.ID, 'start_year').get_attribute('value')
        start_month = self.driver.find_element(By.ID, 'start_month').get_attribute('value')
        end_year = self.driver.find_element(By.ID, 'end_year').get_attribute('value')
        end_month = self.driver.find_element(By.ID, 'end_month').get_attribute('value')

        self.assertEqual(start_year, str(now.year - 1))
        self.assertEqual(start_month, '1')
        self.assertEqual(end_year, str(now.year))
        self.assertEqual(end_month, str(now.month))

    def test_display_button(self):
        """更新ボタンをクリックしてグラフが表示されることを確認"""
        self._login()

        # 期間残高画面に移動
        self._location(self.live_server_url + reverse('moneybook:period_balances'))

        # 更新ボタンをクリック
        self.driver.find_element(By.XPATH, '//input[@value="更新"]').click()
        time.sleep(2)

        # グラフコンテナが表示されている
        graph_container = self.driver.find_element(By.ID, 'lineplot_monthly_balance')
        self.assertTrue(graph_container.is_displayed())

    def test_change_period(self):
        """期間を変更して表示できることを確認"""
        self._login()
        now = datetime.now()

        # 期間残高画面に移動
        self._location(self.live_server_url + reverse('moneybook:period_balances'))

        # 期間を変更（今年1月〜今月）
        start_year_input = self.driver.find_element(By.ID, 'start_year')
        start_year_input.clear()
        start_year_input.send_keys(str(now.year))

        start_month_input = self.driver.find_element(By.ID, 'start_month')
        start_month_input.clear()
        start_month_input.send_keys('1')

        # 更新ボタンをクリック
        self.driver.find_element(By.XPATH, '//input[@value="更新"]').click()
        time.sleep(2)

        # グラフが表示されている
        graph_container = self.driver.find_element(By.ID, 'lineplot_monthly_balance')
        self.assertTrue(graph_container.is_displayed())

        # 入力値が保持されている
        self.assertEqual(self.driver.find_element(By.ID, 'start_year').get_attribute('value'), str(now.year))
        self.assertEqual(self.driver.find_element(By.ID, 'start_month').get_attribute('value'), '1')

    def test_enter_year(self):
        """年入力欄でEnterキーを押すと表示されることを確認"""
        self._login()
        now = datetime.now()

        # 期間残高画面に移動
        self._location(self.live_server_url + reverse('moneybook:period_balances'))

        # 年を入力してEnter
        start_year_input = self.driver.find_element(By.ID, 'start_year')
        start_year_input.clear()
        start_year_input.send_keys(str(now.year))
        start_year_input.send_keys(Keys.RETURN)
        time.sleep(2)

        # グラフが表示されている
        graph_container = self.driver.find_element(By.ID, 'lineplot_monthly_balance')
        self.assertTrue(graph_container.is_displayed())

    def test_enter_month(self):
        """月入力欄でEnterキーを押すと表示されることを確認"""
        self._login()

        # 期間残高画面に移動
        self._location(self.live_server_url + reverse('moneybook:period_balances'))

        # 月を入力してEnter
        start_month_input = self.driver.find_element(By.ID, 'start_month')
        start_month_input.clear()
        start_month_input.send_keys('3')
        start_month_input.send_keys(Keys.RETURN)
        time.sleep(2)

        # グラフが表示されている
        graph_container = self.driver.find_element(By.ID, 'lineplot_monthly_balance')
        self.assertTrue(graph_container.is_displayed())

    def test_with_data(self):
        """データがある状態で期間残高を表示できることを確認"""
        self._login()

        # テストデータを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('期間残高テスト')
        self.driver.find_element(By.ID, 'a_price').send_keys('5000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 期間残高画面に移動
        self._location(self.live_server_url + reverse('moneybook:period_balances'))

        # 更新ボタンをクリック
        self.driver.find_element(By.XPATH, '//input[@value="更新"]').click()
        time.sleep(2)

        # グラフが表示されている
        graph_container = self.driver.find_element(By.ID, 'lineplot_monthly_balance')
        self.assertTrue(graph_container.is_displayed())

    def test_single_month_period(self):
        """1ヶ月だけの期間を指定して表示できることを確認"""
        self._login()
        now = datetime.now()

        # 期間残高画面に移動
        self._location(self.live_server_url + reverse('moneybook:period_balances'))

        # 開始と終了を同じ月に設定
        start_year_input = self.driver.find_element(By.ID, 'start_year')
        start_year_input.clear()
        start_year_input.send_keys(str(now.year))

        start_month_input = self.driver.find_element(By.ID, 'start_month')
        start_month_input.clear()
        start_month_input.send_keys(str(now.month))

        end_year_input = self.driver.find_element(By.ID, 'end_year')
        end_year_input.clear()
        end_year_input.send_keys(str(now.year))

        end_month_input = self.driver.find_element(By.ID, 'end_month')
        end_month_input.clear()
        end_month_input.send_keys(str(now.month))

        # 更新ボタンをクリック
        self.driver.find_element(By.XPATH, '//input[@value="更新"]').click()
        time.sleep(2)

        # グラフが表示されている
        graph_container = self.driver.find_element(By.ID, 'lineplot_monthly_balance')
        self.assertTrue(graph_container.is_displayed())

    def test_multiple_year_period(self):
        """複数年にまたがる期間を指定して表示できることを確認"""
        self._login()
        now = datetime.now()

        # 期間残高画面に移動
        self._location(self.live_server_url + reverse('moneybook:period_balances'))

        # 3年前から今月までの期間を設定
        start_year_input = self.driver.find_element(By.ID, 'start_year')
        start_year_input.clear()
        start_year_input.send_keys(str(now.year - 3))

        start_month_input = self.driver.find_element(By.ID, 'start_month')
        start_month_input.clear()
        start_month_input.send_keys('1')

        # 更新ボタンをクリック
        self.driver.find_element(By.XPATH, '//input[@value="更新"]').click()
        time.sleep(2)

        # グラフが表示されている
        graph_container = self.driver.find_element(By.ID, 'lineplot_monthly_balance')
        self.assertTrue(graph_container.is_displayed())

    def test_period_with_params(self):
        """URLパラメータで期間を指定して表示できることを確認"""
        self._login()
        now = datetime.now()

        # パラメータ付きで期間残高画面に移動
        base_url = f'{self.live_server_url}{reverse("moneybook:period_balances")}'
        url = f'{base_url}?start_year={now.year}&start_month=1&end_year={now.year}&end_month={now.month}'
        self._location(url)

        # 更新ボタンをクリック
        self.driver.find_element(By.XPATH, '//input[@value="更新"]').click()
        time.sleep(2)

        # グラフが表示されている
        graph_container = self.driver.find_element(By.ID, 'lineplot_monthly_balance')
        self.assertTrue(graph_container.is_displayed())

        # パラメータの値が入力欄に反映されている
        self.assertEqual(self.driver.find_element(By.ID, 'start_year').get_attribute('value'), str(now.year))
        self.assertEqual(self.driver.find_element(By.ID, 'start_month').get_attribute('value'), '1')
        self.assertEqual(self.driver.find_element(By.ID, 'end_year').get_attribute('value'), str(now.year))
        self.assertEqual(self.driver.find_element(By.ID, 'end_month').get_attribute('value'), str(now.month))
