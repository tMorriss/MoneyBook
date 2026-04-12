import time
from datetime import datetime

from django.urls import reverse
from moneybook.e2e.base import SeleniumBase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Search(SeleniumBase):
    fixtures = ['test_case']

    def test_get(self):
        """検索画面が正しく表示されることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:search'))

        self._assert_common()

        # 検索フォームが表示されている
        self.assertTrue(self.driver.find_element(By.NAME, 'start_year').is_displayed())
        self.assertTrue(self.driver.find_element(By.NAME, 'start_month').is_displayed())
        self.assertTrue(self.driver.find_element(By.NAME, 'start_day').is_displayed())
        self.assertTrue(self.driver.find_element(By.NAME, 'end_year').is_displayed())
        self.assertTrue(self.driver.find_element(By.NAME, 'end_month').is_displayed())
        self.assertTrue(self.driver.find_element(By.NAME, 'end_day').is_displayed())
        self.assertTrue(self.driver.find_element(By.NAME, 'item').is_displayed())
        self.assertTrue(self.driver.find_element(By.NAME, 'lower_price').is_displayed())
        self.assertTrue(self.driver.find_element(By.NAME, 'upper_price').is_displayed())

    def test_search_by_item(self):
        """項目名で検索できることを確認"""
        self._login()
        # テストデータを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('UniqueItem1')
        self.driver.find_element(By.ID, 'a_price').send_keys('1000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        self.driver.find_element(By.ID, 'a_day').send_keys('11')
        self.driver.find_element(By.ID, 'a_item').send_keys('UniqueItem2')
        self.driver.find_element(By.ID, 'a_price').send_keys('2000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 検索画面に移動
        self._location(self.live_server_url + reverse('moneybook:search'))

        # 項目名で検索
        self.driver.find_element(By.NAME, 'item').send_keys('UniqueItem1')
        self.driver.find_element(By.XPATH, '//input[@value="検索"]').click()
        time.sleep(2)

        # 検索結果を確認
        rows = self.driver.find_elements(By.CSS_SELECTOR, '#search-result .data-row')
        self.assertEqual(len(rows), 1)
        tds = rows[0].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[1].text, 'UniqueItem1')

    def test_search_by_date_range(self):
        """日付範囲で検索できることを確認"""
        self._login()
        now = datetime.now()

        # テストデータを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('5')
        self.driver.find_element(By.ID, 'a_item').send_keys('UniqueDate5')
        self.driver.find_element(By.ID, 'a_price').send_keys('1000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        self.driver.find_element(By.ID, 'a_day').send_keys('15')
        self.driver.find_element(By.ID, 'a_item').send_keys('UniqueDate15')
        self.driver.find_element(By.ID, 'a_price').send_keys('2000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 検索画面に移動
        self._location(self.live_server_url + reverse('moneybook:search'))

        # 10日〜20日の範囲で検索
        self.driver.find_element(By.NAME, 'start_year').clear()
        self.driver.find_element(By.NAME, 'start_year').send_keys(str(now.year))
        self.driver.find_element(By.NAME, 'start_month').clear()
        self.driver.find_element(By.NAME, 'start_month').send_keys(str(now.month))
        self.driver.find_element(By.NAME, 'start_day').send_keys('10')
        self.driver.find_element(By.NAME, 'end_year').clear()
        self.driver.find_element(By.NAME, 'end_year').send_keys(str(now.year))
        self.driver.find_element(By.NAME, 'end_month').clear()
        self.driver.find_element(By.NAME, 'end_month').send_keys(str(now.month))
        self.driver.find_element(By.NAME, 'end_day').send_keys('20')
        self.driver.find_element(By.XPATH, '//input[@value="検索"]').click()
        time.sleep(2)

        # 検索結果を確認（15日のデータのみヒット）
        rows = self.driver.find_elements(By.CSS_SELECTOR, '#search-result .data-row')
        self.assertEqual(len(rows), 1)
        tds = rows[0].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[1].text, 'UniqueDate15')

    def test_search_by_price_range(self):
        """金額範囲で検索できることを確認"""
        self._login()
        # テストデータを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('UniquePrice500')
        self.driver.find_element(By.ID, 'a_price').send_keys('500')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        self.driver.find_element(By.ID, 'a_day').send_keys('11')
        self.driver.find_element(By.ID, 'a_item').send_keys('UniquePrice1500')
        self.driver.find_element(By.ID, 'a_price').send_keys('1500')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 検索画面に移動
        self._location(self.live_server_url + reverse('moneybook:search'))

        # 1000円〜3000円の範囲で検索
        self.driver.find_element(By.NAME, 'lower_price').send_keys('1000')
        self.driver.find_element(By.NAME, 'upper_price').send_keys('3000')
        self.driver.find_element(By.XPATH, '//input[@value="検索"]').click()
        time.sleep(2)

        # 検索結果を確認
        rows = self.driver.find_elements(By.CSS_SELECTOR, '#search-result .data-row')
        self.assertEqual(len(rows), 1)
        tds = rows[0].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[1].text, 'UniquePrice1500')

    def test_search_by_method(self):
        """支払い方法で検索できることを確認"""
        self._login()

        # テストデータを追加（銀行）
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('UniqueBankItem')
        self.driver.find_element(By.ID, 'a_price').send_keys('1000')
        self.driver.find_element(By.ID, 'lbl_a_method-2').click()  # 銀行
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 検索画面に移動
        self._location(self.live_server_url + reverse('moneybook:search'))

        # 品目と銀行で検索
        self.driver.find_element(By.NAME, 'item').send_keys('UniqueBankItem')
        self.driver.find_element(By.ID, 'lbl_method-2').click()  # 銀行をチェック
        self.driver.find_element(By.XPATH, '//input[@value="検索"]').click()
        time.sleep(2)

        # 検索結果を確認
        rows = self.driver.find_elements(By.CSS_SELECTOR, '#search-result .data-row')
        self.assertEqual(len(rows), 1)
        tds = rows[0].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[1].text, 'UniqueBankItem')

    def test_search_by_category(self):
        """カテゴリーで検索できることを確認"""
        self._login()

        # テストデータを追加（食費）
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('UniqueFoodItem')
        self.driver.find_element(By.ID, 'a_price').send_keys('1000')
        self.driver.find_element(By.ID, 'lbl_a_category-1').click()  # 食費
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 検索画面に移動
        self._location(self.live_server_url + reverse('moneybook:search'))

        # 品目と食費で検索
        self.driver.find_element(By.NAME, 'item').send_keys('UniqueFoodItem')
        self.driver.find_element(By.ID, 'lbl_category-1').click()  # 食費をチェック
        self.driver.find_element(By.XPATH, '//input[@value="検索"]').click()
        time.sleep(2)

        # 検索結果を確認
        rows = self.driver.find_elements(By.CSS_SELECTOR, '#search-result .data-row')
        self.assertEqual(len(rows), 1)
        tds = rows[0].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[1].text, 'UniqueFoodItem')

    def test_search_combined_conditions(self):
        """複数の条件を組み合わせて検索できることを確認"""
        self._login()

        # テストデータを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('UniqueCombinedItem')
        self.driver.find_element(By.ID, 'a_price').send_keys('1500')
        self.driver.find_element(By.ID, 'lbl_a_method-2').click()  # 銀行
        self.driver.find_element(By.ID, 'lbl_a_category-1').click()  # 食費
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 検索画面に移動
        self._location(self.live_server_url + reverse('moneybook:search'))

        # 品目、銀行、食費で検索
        self.driver.find_element(By.NAME, 'item').send_keys('UniqueCombined')
        self.driver.find_element(By.ID, 'lbl_method-2').click()  # 銀行
        self.driver.find_element(By.ID, 'lbl_category-1').click()  # 食費
        self.driver.find_element(By.XPATH, '//input[@value="検索"]').click()
        time.sleep(2)

        # 検索結果を確認
        rows = self.driver.find_elements(By.CSS_SELECTOR, '#search-result .data-row')
        self.assertEqual(len(rows), 1)
        tds = rows[0].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[1].text, 'UniqueCombinedItem')

    def test_search_button_enter(self):
        """Enterキーで検索できることを確認"""
        self._login()
        # テストデータを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('UniqueEnterItem')
        self.driver.find_element(By.ID, 'a_price').send_keys('1000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 検索画面に移動
        self._location(self.live_server_url + reverse('moneybook:search'))

        # 項目名で検索（Enterキーを使用）
        item_input = self.driver.find_element(By.NAME, 'item')
        item_input.send_keys('UniqueEnterItem')
        item_input.send_keys(Keys.RETURN)
        time.sleep(2)

        # 検索結果を確認
        rows = self.driver.find_elements(By.CSS_SELECTOR, '#search-result .data-row')
        self.assertEqual(len(rows), 1)
        tds = rows[0].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[1].text, 'UniqueEnterItem')

    def test_search_no_results(self):
        """検索結果が0件の場合の表示を確認"""
        self._login()
        # 検索画面に移動
        self._location(self.live_server_url + reverse('moneybook:search'))

        # 存在しない項目名で検索
        self.driver.find_element(By.NAME, 'item').send_keys('NonExistentItem')
        self.driver.find_element(By.XPATH, '//input[@value="検索"]').click()
        time.sleep(2)

        # 検索結果を確認（データ行なし）
        rows = self.driver.find_elements(By.CSS_SELECTOR, '#search-result .data-row')
        self.assertEqual(len(rows), 0)

    def test_search_result_link_to_edit(self):
        """検索結果から編集画面に遷移できることを確認"""
        self._login()
        # テストデータを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('UniqueEditItem')
        self.driver.find_element(By.ID, 'a_price').send_keys('1000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 検索画面に移動
        self._location(self.live_server_url + reverse('moneybook:search'))

        # 項目名で検索
        self.driver.find_element(By.NAME, 'item').send_keys('UniqueEditItem')
        self.driver.find_element(By.XPATH, '//input[@value="検索"]').click()
        time.sleep(2)

        # 編集リンクをクリック
        self.driver.find_element(By.CSS_SELECTOR, '#search-result .data-row .a-edit a').click()
        time.sleep(1)

        # 編集画面に遷移したことを確認
        self.assertIn('edit', self.driver.current_url)
        self.assertEqual(self.driver.find_element(By.ID, 'item').get_attribute('value'), 'UniqueEditItem')
