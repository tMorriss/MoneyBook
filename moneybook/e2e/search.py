import time
from datetime import datetime

from django.urls import reverse
from moneybook.e2e.base import SeleniumBase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Search(SeleniumBase):
    def test_get(self):
        '''検索画面が正しく表示されることを確認'''
        self._login()
        self._location(self.live_server_url + reverse('moneybook:search'))

        self._assert_common()

        # 検索フォームが表示されている
        self.assertTrue(self.driver.find_element(By.ID, 'start_year').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'start_month').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'start_day').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'end_year').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'end_month').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'end_day').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'item').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'lower_price').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'upper_price').is_displayed())

    def test_search_by_item(self):
        '''項目名で検索できることを確認'''
        self._login()
        # テストデータを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('検索テスト1')
        self.driver.find_element(By.ID, 'a_price').send_keys('1000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        self.driver.find_element(By.ID, 'a_day').send_keys('11')
        self.driver.find_element(By.ID, 'a_item').send_keys('別のデータ')
        self.driver.find_element(By.ID, 'a_price').send_keys('2000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 検索画面に移動
        self._location(self.live_server_url + reverse('moneybook:search'))

        # 項目名で検索
        self.driver.find_element(By.ID, 'item').send_keys('検索テスト1')
        self.driver.find_element(By.XPATH, '//input[@value="検索"]').click()
        time.sleep(2)

        # 検索結果を確認
        rows = self.driver.find_elements(By.XPATH, '//table[@id="search-result"]/tbody/tr')
        self.assertEqual(len(rows), 2)  # ヘッダー + 1件
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[1].text, '検索テスト1')

    def test_search_by_date_range(self):
        '''日付範囲で検索できることを確認'''
        self._login()
        now = datetime.now()

        # テストデータを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('5')
        self.driver.find_element(By.ID, 'a_item').send_keys('5日のデータ')
        self.driver.find_element(By.ID, 'a_price').send_keys('1000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        self.driver.find_element(By.ID, 'a_day').send_keys('15')
        self.driver.find_element(By.ID, 'a_item').send_keys('15日のデータ')
        self.driver.find_element(By.ID, 'a_price').send_keys('2000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        self.driver.find_element(By.ID, 'a_day').send_keys('25')
        self.driver.find_element(By.ID, 'a_item').send_keys('25日のデータ')
        self.driver.find_element(By.ID, 'a_price').send_keys('3000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 検索画面に移動
        self._location(self.live_server_url + reverse('moneybook:search'))

        # 10日〜20日の範囲で検索
        self.driver.find_element(By.ID, 'start_year').clear()
        self.driver.find_element(By.ID, 'start_year').send_keys(str(now.year))
        self.driver.find_element(By.ID, 'start_month').clear()
        self.driver.find_element(By.ID, 'start_month').send_keys(str(now.month))
        self.driver.find_element(By.ID, 'start_day').send_keys('10')
        self.driver.find_element(By.ID, 'end_year').clear()
        self.driver.find_element(By.ID, 'end_year').send_keys(str(now.year))
        self.driver.find_element(By.ID, 'end_month').clear()
        self.driver.find_element(By.ID, 'end_month').send_keys(str(now.month))
        self.driver.find_element(By.ID, 'end_day').send_keys('20')
        self.driver.find_element(By.XPATH, '//input[@value="検索"]').click()
        time.sleep(2)

        # 検索結果を確認（15日のデータのみヒット）
        rows = self.driver.find_elements(By.XPATH, '//table[@id="search-result"]/tbody/tr')
        self.assertEqual(len(rows), 2)  # ヘッダー + 1件
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[1].text, '15日のデータ')

    def test_search_by_price_range(self):
        '''金額範囲で検索できることを確認'''
        self._login()
        # テストデータを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('安いデータ')
        self.driver.find_element(By.ID, 'a_price').send_keys('500')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        self.driver.find_element(By.ID, 'a_day').send_keys('11')
        self.driver.find_element(By.ID, 'a_item').send_keys('中間のデータ')
        self.driver.find_element(By.ID, 'a_price').send_keys('1500')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        self.driver.find_element(By.ID, 'a_day').send_keys('12')
        self.driver.find_element(By.ID, 'a_item').send_keys('高いデータ')
        self.driver.find_element(By.ID, 'a_price').send_keys('5000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 検索画面に移動
        self._location(self.live_server_url + reverse('moneybook:search'))

        # 1000円〜3000円の範囲で検索
        self.driver.find_element(By.ID, 'lower_price').send_keys('1000')
        self.driver.find_element(By.ID, 'upper_price').send_keys('3000')
        self.driver.find_element(By.XPATH, '//input[@value="検索"]').click()
        time.sleep(2)

        # 検索結果を確認（中間のデータのみヒット）
        rows = self.driver.find_elements(By.XPATH, '//table[@id="search-result"]/tbody/tr')
        self.assertEqual(len(rows), 2)  # ヘッダー + 1件
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[1].text, '中間のデータ')

    def test_search_by_method(self):
        '''支払い方法で検索できることを確認'''
        self._login()
        # テストデータを追加（銀行）
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('銀行データ')
        self.driver.find_element(By.ID, 'a_price').send_keys('1000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/table/tbody/tr[4]/td/label[1]').click()  # 銀行
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # テストデータを追加（現金）
        self.driver.find_element(By.ID, 'a_day').send_keys('11')
        self.driver.find_element(By.ID, 'a_item').send_keys('現金データ')
        self.driver.find_element(By.ID, 'a_price').send_keys('2000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/table/tbody/tr[4]/td/label[2]').click()  # 現金
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 検索画面に移動
        self._location(self.live_server_url + reverse('moneybook:search'))

        # 銀行のみで検索
        self.driver.find_element(By.XPATH, '//form/table/tbody/tr[6]/td/label[1]').click()  # 銀行をチェック
        self.driver.find_element(By.XPATH, '//input[@value="検索"]').click()
        time.sleep(2)

        # 検索結果を確認（銀行データのみヒット）
        rows = self.driver.find_elements(By.XPATH, '//table[@id="search-result"]/tbody/tr')
        self.assertEqual(len(rows), 2)  # ヘッダー + 1件
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[1].text, '銀行データ')

    def test_search_by_category(self):
        '''カテゴリーで検索できることを確認'''
        self._login()
        # テストデータを追加（食費）
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('食費データ')
        self.driver.find_element(By.ID, 'a_price').send_keys('1000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/table/tbody/tr[5]/td/table/tbody/tr/td/label[1]').click()  # 食費
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # テストデータを追加（必需品）
        self.driver.find_element(By.ID, 'a_day').send_keys('11')
        self.driver.find_element(By.ID, 'a_item').send_keys('必需品データ')
        self.driver.find_element(By.ID, 'a_price').send_keys('2000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/table/tbody/tr[5]/td/table/tbody/tr/td/label[2]').click()  # 必需品
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 検索画面に移動
        self._location(self.live_server_url + reverse('moneybook:search'))

        # 食費のみで検索
        self.driver.find_element(By.XPATH, '//form/table/tbody/tr[7]/td/label[1]').click()  # 食費をチェック
        self.driver.find_element(By.XPATH, '//input[@value="検索"]').click()
        time.sleep(2)

        # 検索結果を確認（食費データのみヒット）
        rows = self.driver.find_elements(By.XPATH, '//table[@id="search-result"]/tbody/tr')
        self.assertEqual(len(rows), 2)  # ヘッダー + 1件
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[1].text, '食費データ')

    def test_search_combined_conditions(self):
        '''複数の条件を組み合わせて検索できることを確認'''
        self._login()

        # テストデータを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('スーパー買い物')
        self.driver.find_element(By.ID, 'a_price').send_keys('1500')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/table/tbody/tr[4]/td/label[1]').click()  # 銀行
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/table/tbody/tr[5]/td/table/tbody/tr/td/label[1]').click()  # 食費
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        self.driver.find_element(By.ID, 'a_day').send_keys('20')
        self.driver.find_element(By.ID, 'a_item').send_keys('コンビニ買い物')
        self.driver.find_element(By.ID, 'a_price').send_keys('500')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/table/tbody/tr[4]/td/label[2]').click()  # 現金
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/table/tbody/tr[5]/td/table/tbody/tr/td/label[1]').click()  # 食費
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 検索画面に移動
        self._location(self.live_server_url + reverse('moneybook:search'))

        # 項目名に「スーパー」を含み、銀行、食費で検索
        self.driver.find_element(By.ID, 'item').send_keys('スーパー')
        self.driver.find_element(By.XPATH, '//form/table/tbody/tr[6]/td/label[1]').click()  # 銀行
        self.driver.find_element(By.XPATH, '//form/table/tbody/tr[7]/td/label[1]').click()  # 食費
        self.driver.find_element(By.XPATH, '//input[@value="検索"]').click()
        time.sleep(2)

        # 検索結果を確認（スーパー買い物のみヒット）
        rows = self.driver.find_elements(By.XPATH, '//table[@id="search-result"]/tbody/tr')
        self.assertEqual(len(rows), 2)  # ヘッダー + 1件
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[1].text, 'スーパー買い物')

    def test_search_button_enter(self):
        '''Enterキーで検索できることを確認'''
        self._login()
        # テストデータを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('Enterテスト')
        self.driver.find_element(By.ID, 'a_price').send_keys('1000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 検索画面に移動
        self._location(self.live_server_url + reverse('moneybook:search'))

        # 項目名で検索（Enterキーを使用）
        item_input = self.driver.find_element(By.ID, 'item')
        item_input.send_keys('Enterテスト')
        item_input.send_keys(Keys.RETURN)
        time.sleep(2)

        # 検索結果を確認
        rows = self.driver.find_elements(By.XPATH, '//table[@id="search-result"]/tbody/tr')
        self.assertEqual(len(rows), 2)  # ヘッダー + 1件
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[1].text, 'Enterテスト')

    def test_search_no_results(self):
        '''検索結果が0件の場合の表示を確認'''
        self._login()
        # 検索画面に移動
        self._location(self.live_server_url + reverse('moneybook:search'))

        # 存在しない項目名で検索
        self.driver.find_element(By.ID, 'item').send_keys('存在しないデータ')
        self.driver.find_element(By.XPATH, '//input[@value="検索"]').click()
        time.sleep(2)

        # 検索結果を確認（ヘッダーのみ）
        rows = self.driver.find_elements(By.XPATH, '//table[@id="search-result"]/tbody/tr')
        self.assertEqual(len(rows), 1)  # ヘッダーのみ

    def test_search_result_link_to_edit(self):
        '''検索結果から編集画面に遷移できることを確認'''
        self._login()
        # テストデータを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('編集遷移テスト')
        self.driver.find_element(By.ID, 'a_price').send_keys('1000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 検索画面に移動
        self._location(self.live_server_url + reverse('moneybook:search'))

        # 項目名で検索
        self.driver.find_element(By.ID, 'item').send_keys('編集遷移テスト')
        self.driver.find_element(By.XPATH, '//input[@value="検索"]').click()
        time.sleep(2)

        # 編集リンクをクリック
        self.driver.find_element(By.XPATH, '//table[@id="search-result"]/tbody/tr[2]/td[6]/a').click()
        time.sleep(1)

        # 編集画面に遷移したことを確認
        self.assertIn('edit', self.driver.current_url)
        self.assertEqual(self.driver.find_element(By.ID, 'id_item').get_attribute('value'), '編集遷移テスト')
