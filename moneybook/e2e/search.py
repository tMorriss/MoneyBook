import re
from datetime import datetime

from django.urls import reverse
from moneybook.e2e.base import expect, PlaywrightBase


class Search(PlaywrightBase):
    fixtures = ['test_case']

    def test_get(self):
        """検索画面が正しく表示されることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:search'))

        self._assert_common()

        # 検索フォームが表示されている
        expect(self.page.locator('input[name="start_year"]')).to_be_visible()
        expect(self.page.locator('input[name="start_month"]')).to_be_visible()
        expect(self.page.locator('input[name="start_day"]')).to_be_visible()
        expect(self.page.locator('input[name="end_year"]')).to_be_visible()
        expect(self.page.locator('input[name="end_month"]')).to_be_visible()
        expect(self.page.locator('input[name="end_day"]')).to_be_visible()
        expect(self.page.locator('input[name="item"]')).to_be_visible()
        expect(self.page.locator('input[name="lower_price"]')).to_be_visible()
        expect(self.page.locator('input[name="upper_price"]')).to_be_visible()

    def test_search_by_item(self):
        """項目名で検索できることを確認"""
        self._login()
        # テストデータを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.page.fill('#a_day', '10')
        self.page.fill('#a_item', '検索テスト1')
        self.page.fill('#a_price', '1000')
        self.page.click('#filter-fixed form input[value="追加"]')
        self._wait_for_ajax()

        self.page.fill('#a_day', '11')
        self.page.fill('#a_item', '別のデータ')
        self.page.fill('#a_price', '2000')
        self.page.click('#filter-fixed form input[value="追加"]')
        self._wait_for_ajax()

        # 検索画面に移動
        self._location(self.live_server_url + reverse('moneybook:search'))

        # 項目名で検索
        self.page.fill('input[name="item"]', '検索テスト1')
        self.page.click('input[value="検索"]')
        # 検索結果が表示されるのを待つ
        self.page.wait_for_selector('#search-result')

        # 検索結果を確認
        expect(self.page.locator('#search-result .data-row')).to_have_count(1)
        expect(self.page.locator('#search-result .data_item')).to_have_text(['検索テスト1'])

    def test_search_by_date_range(self):
        """日付範囲で検索できることを確認"""
        self._login()
        now = datetime.now()

        # テストデータを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.page.fill('#a_day', '5')
        self.page.fill('#a_item', '5日のデータ')
        self.page.fill('#a_price', '1000')
        self.page.click('#filter-fixed form input[value="追加"]')
        self._wait_for_ajax()

        self.page.fill('#a_day', '15')
        self.page.fill('#a_item', '15日のデータ')
        self.page.fill('#a_price', '2000')
        self.page.click('#filter-fixed form input[value="追加"]')
        self._wait_for_ajax()

        self.page.fill('#a_day', '25')
        self.page.fill('#a_item', '25日のデータ')
        self.page.fill('#a_price', '3000')
        self.page.click('#filter-fixed form input[value="追加"]')
        self._wait_for_ajax()

        # 検索画面に移動
        self._location(self.live_server_url + reverse('moneybook:search'))

        # 10日〜20日の範囲で検索
        self.page.fill('input[name="start_year"]', str(now.year))
        self.page.fill('input[name="start_month"]', str(now.month))
        self.page.fill('input[name="start_day"]', '10')
        self.page.fill('input[name="end_year"]', str(now.year))
        self.page.fill('input[name="end_month"]', str(now.month))
        self.page.fill('input[name="end_day"]', '20')
        self.page.click('input[value="検索"]')
        self.page.wait_for_selector('#search-result')

        # 検索結果を確認（15日のデータのみヒット）
        expect(self.page.locator('#search-result .data-row')).to_have_count(1)
        expect(self.page.locator('#search-result .data_item')).to_have_text(['15日のデータ'])

    def test_search_by_price_range(self):
        """金額範囲で検索できることを確認"""
        self._login()
        # テストデータを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.page.fill('#a_day', '10')
        self.page.fill('#a_item', '安いデータ')
        self.page.fill('#a_price', '500')
        self.page.click('#filter-fixed form input[value="追加"]')
        self._wait_for_ajax()

        self.page.fill('#a_day', '11')
        self.page.fill('#a_item', '中間のデータ')
        self.page.fill('#a_price', '1500')
        self.page.click('#filter-fixed form input[value="追加"]')
        self._wait_for_ajax()

        self.page.fill('#a_day', '12')
        self.page.fill('#a_item', '高いデータ')
        self.page.fill('#a_price', '5000')
        self.page.click('#filter-fixed form input[value="追加"]')
        self._wait_for_ajax()

        # 検索画面に移動
        self._location(self.live_server_url + reverse('moneybook:search'))

        # 1000円〜3000円の範囲で検索
        self.page.fill('input[name="lower_price"]', '1000')
        self.page.fill('input[name="upper_price"]', '3000')
        self.page.click('input[value="検索"]')
        self.page.wait_for_selector('#search-result')

        # 検索結果を確認（中間のデータのみヒット）
        expect(self.page.locator('#search-result .data-row')).to_have_count(1)
        expect(self.page.locator('#search-result .data_item')).to_have_text(['中間のデータ'])

    def test_search_by_method(self):
        """支払い方法で検索できることを確認"""
        self._login()
        # テストデータを追加（銀行）
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.page.fill('#a_day', '10')
        self.page.fill('#a_item', '銀行データ')
        self.page.fill('#a_price', '1000')
        # 銀行ラベルをクリック
        self.page.locator('#filter-fixed form label').filter(has_text='銀行').first.click()
        self.page.click('#filter-fixed form input[value="追加"]')
        self._wait_for_ajax()

        # テストデータを追加（現金）
        self.page.fill('#a_day', '11')
        self.page.fill('#a_item', '現金データ')
        self.page.fill('#a_price', '2000')
        # 現金ラベルをクリック
        self.page.locator('#filter-fixed form label').filter(has_text='現金').first.click()
        self.page.click('#filter-fixed form input[value="追加"]')
        self._wait_for_ajax()

        # 検索画面に移動
        self._location(self.live_server_url + reverse('moneybook:search'))

        # 銀行のみで検索
        # 検索フォーム内の「銀行」ラベルを探す
        self.page.locator('form table label').filter(has_text='銀行').first.click()
        self.page.click('input[value="検索"]')
        self.page.wait_for_selector('#search-result')

        # 検索結果を確認（銀行データのみヒット）
        expect(self.page.locator('#search-result .data-row')).to_have_count(1)
        expect(self.page.locator('#search-result .data_item')).to_have_text(['銀行データ'])

    def test_search_by_category(self):
        """カテゴリーで検索できることを確認"""
        self._login()
        # テストデータを追加（食費）
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.page.fill('#a_day', '10')
        self.page.fill('#a_item', '食費データ')
        self.page.fill('#a_price', '1000')
        # 食費ラベルをクリック
        self.page.locator('#filter-fixed form label').filter(has_text='食費').first.click()
        self.page.click('#filter-fixed form input[value="追加"]')
        self._wait_for_ajax()

        # テストデータを追加（必需品）
        self.page.fill('#a_day', '11')
        self.page.fill('#a_item', '必需品データ')
        self.page.fill('#a_price', '2000')
        # 必需品ラベルをクリック
        self.page.locator('#filter-fixed form label').filter(has_text='必需品').first.click()
        self.page.click('#filter-fixed form input[value="追加"]')
        self._wait_for_ajax()

        # 検索画面に移動
        self._location(self.live_server_url + reverse('moneybook:search'))

        # 食費のみで検索
        self.page.locator('form table label').filter(has_text='食費').first.click()
        self.page.click('input[value="検索"]')
        self.page.wait_for_selector('#search-result')

        # 検索結果を確認（食費データのみヒット）
        expect(self.page.locator('#search-result .data-row')).to_have_count(1)
        expect(self.page.locator('#search-result .data_item')).to_have_text(['食費データ'])

    def test_search_combined_conditions(self):
        """複数の条件を組み合わせて検索できることを確認"""
        self._login()

        # テストデータを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.page.fill('#a_day', '10')
        self.page.fill('#a_item', 'スーパー買い物')
        self.page.fill('#a_price', '1500')
        self.page.locator('#filter-fixed form label').filter(has_text='銀行').first.click()
        self.page.locator('#filter-fixed form label').filter(has_text='食費').first.click()
        self.page.click('#filter-fixed form input[value="追加"]')
        self._wait_for_ajax()

        self.page.fill('#a_day', '20')
        self.page.fill('#a_item', 'コンビニ買い物')
        self.page.fill('#a_price', '500')
        self.page.locator('#filter-fixed form label').filter(has_text='現金').first.click()
        self.page.locator('#filter-fixed form label').filter(has_text='食費').first.click()
        self.page.click('#filter-fixed form input[value="追加"]')
        self._wait_for_ajax()

        # 検索画面に移動
        self._location(self.live_server_url + reverse('moneybook:search'))

        # 項目名に「スーパー」を含み、銀行、食費で検索
        self.page.fill('input[name="item"]', 'スーパー')
        self.page.locator('form table label').filter(has_text='銀行').first.click()
        self.page.locator('form table label').filter(has_text='食費').first.click()
        self.page.click('input[value="検索"]')
        self.page.wait_for_selector('#search-result')

        # 検索結果を確認（スーパー買い物のみヒット）
        expect(self.page.locator('#search-result .data-row')).to_have_count(1)
        expect(self.page.locator('#search-result .data_item')).to_have_text(['スーパー買い物'])

    def test_search_button_enter(self):
        """Enterキーで検索できることを確認"""
        self._login()
        # テストデータを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.page.fill('#a_day', '10')
        self.page.fill('#a_item', 'Enterテスト')
        self.page.fill('#a_price', '1000')
        self.page.click('#filter-fixed form input[value="追加"]')
        self._wait_for_ajax()

        # 検索画面に移動
        self._location(self.live_server_url + reverse('moneybook:search'))

        # 項目名で検索（Enterキーを使用）
        item_input = self.page.locator('input[name="item"]')
        item_input.fill('Enterテスト')
        item_input.press('Enter')
        self.page.wait_for_selector('#search-result')

        # 検索結果を確認
        expect(self.page.locator('#search-result .data-row')).to_have_count(1)
        expect(self.page.locator('#search-result .data_item')).to_have_text(['Enterテスト'])

    def test_search_no_results(self):
        """検索結果が0件の場合の表示を確認"""
        self._login()
        # 検索画面に移動
        self._location(self.live_server_url + reverse('moneybook:search'))

        # 存在しない項目名で検索
        self.page.fill('input[name="item"]', '存在しないデータ')
        self.page.click('input[value="検索"]')
        self.page.wait_for_selector('#search-result')

        # 検索結果を確認
        expect(self.page.locator('#search-result .data-row')).to_have_count(0)

    def test_search_result_link_to_edit(self):
        """検索結果から編集画面に遷移できることを確認"""
        self._login()
        # テストデータを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.page.fill('#a_day', '10')
        self.page.fill('#a_item', '編集遷移テスト')
        self.page.fill('#a_price', '1000')
        self.page.click('#filter-fixed form input[value="追加"]')
        self._wait_for_ajax()

        # 検索画面に移動
        self._location(self.live_server_url + reverse('moneybook:search'))

        # 項目名で検索
        self.page.fill('input[name="item"]', '編集遷移テスト')
        self.page.click('input[value="検索"]')
        self.page.wait_for_selector('#search-result')

        # 編集リンクをクリック
        self.page.locator('#search-result .data-row').filter(has_text='編集遷移テスト').locator('.a-edit a').click()

        # 編集画面に遷移したことを確認
        expect(self.page).to_have_url(re.compile(r'/edit/'))
        expect(self.page.locator('#item')).to_have_value('編集遷移テスト')
