import time
from datetime import datetime

from django.urls import reverse
from moneybook.playwright.base import PlaywrightBase


class EditTest(PlaywrightBase):
    def _add_row_and_goto_edit(self, day='10', item='編集テスト', price='1000', method_id=None, category_id=None):
        # 確実にインデックスにいる状態にする
        self.page.goto(self.live_server_url + reverse('moneybook:index'))

        # ページが完全に初期化されるのを待つ (fetchData)
        self.page.wait_for_selector('#a_day')
        # 少し待機してJSの初期化を確実にする
        time.sleep(0.5)

        self.page.fill('#a_day', day)
        self.page.fill('#a_item', item)
        self.page.fill('#a_price', price)

        if method_id:
            self.page.click(f'label[for="a_method-{method_id}"]')
        if category_id:
            self.page.click(f'label[for="a_category-{category_id}"]')

        # 追加ボタンをクリック
        self.page.click('input[value="追加"]')

        # 一覧が更新されるのを待つ
        self.page.wait_for_selector(f'.data-row:has-text("{item}")')

        # 編集画面に移動
        self.page.locator('.data-row', has_text=item).first.locator('.a-edit a').click()
        self.page.wait_for_load_state('load')

    def test_get(self):
        """編集画面が正しく表示されることを確認"""
        self._login()
        self._add_row_and_goto_edit(day='10', item='編集テスト', price='1000')

        # アプリ名
        self.assertEqual(self.page.inner_text('.header-cont1'), 'test-MoneyBook')
        # 名前表示
        header_cont2_text = self.page.inner_text('.header-cont2')
        self.assertTrue(self.username + 'さん' in header_cont2_text, header_cont2_text)

        # フォームの値を確認
        now = datetime.now()
        self.assertEqual(self.page.input_value('#year'), str(now.year))
        self.assertEqual(self.page.input_value('#month'), str(now.month).zfill(2))
        self.assertEqual(self.page.input_value('#day'), '10')
        self.assertEqual(self.page.input_value('#item'), '編集テスト')
        self.assertEqual(self.page.input_value('#price'), '1000')

        # 支払い方法と分類が正しく選択されていることを確認
        self.assertTrue(self.page.is_checked('input[name="method"][value="2"]'))  # 銀行
        self.assertTrue(self.page.is_checked('input[name="category"][value="1"]'))  # 食費

    def test_edit_item(self):
        """項目名を編集できることを確認"""
        self._login()
        self._add_row_and_goto_edit(item='編集前')

        # 項目名を変更
        self.page.fill('#item', '編集後')
        self.page.click('input[value="更新"]')

        # トップに戻るのを待つ
        self.page.wait_for_url(self.live_server_url + reverse('moneybook:index'))
        self.page.wait_for_selector('.data-row:has-text("編集後")')

        item_text = self.page.locator('.data-row').first.locator('td').nth(1).inner_text()
        self.assertEqual(item_text, '編集後')

    def test_edit_price(self):
        """金額を編集できることを確認"""
        self._login()
        self._add_row_and_goto_edit(price='1000')

        # 金額を変更
        self.page.fill('#price', '5000')
        self.page.click('input[value="更新"]')

        # トップに戻るのを待つ
        self.page.wait_for_url(self.live_server_url + reverse('moneybook:index'))
        self.page.wait_for_selector('.data-row')

        price_text = self.page.locator('.data-row').first.locator('td').nth(2).inner_text()
        self.assertEqual(price_text, '5,000')

    def test_edit_date(self):
        """日付を編集できることを確認"""
        self._login()
        self._add_row_and_goto_edit()

        # 日付を変更
        self.page.fill('#day', '15')
        self.page.click('input[value="更新"]')

        # トップに戻る
        self.page.wait_for_url(self.live_server_url + reverse('moneybook:index'))
        self.page.wait_for_selector('.data-row')

        now = datetime.now()
        date_text = self.page.locator('.data-row').first.locator('td').nth(0).inner_text()
        self.assertEqual(date_text, f'{now.year}/{str(now.month).zfill(2)}/15')

    def test_edit_method(self):
        """支払い方法を編集できることを確認"""
        self._login()
        # データを追加（銀行:2 で登録）
        self._add_row_and_goto_edit(method_id='2')

        # 支払い方法を現金:1 に変更
        self.page.click('label[for="method-1"]')
        self.page.click('input[value="更新"]')

        # トップに戻る
        self.page.wait_for_url(self.live_server_url + reverse('moneybook:index'))
        self.page.wait_for_selector('.data-row')

        method_text = self.page.locator('.data-row').first.locator('td').nth(3).inner_text()
        self.assertEqual(method_text, '現金')

    def test_edit_category(self):
        """カテゴリーを編集できることを確認"""
        self._login()
        # データを追加（食費:1 で登録）
        self._add_row_and_goto_edit(category_id='1')

        # カテゴリーを必需品:2 に変更
        self.page.click('label[for="category-2"]')
        self.page.click('input[value="更新"]')

        # トップに戻る
        self.page.wait_for_url(self.live_server_url + reverse('moneybook:index'))
        self.page.wait_for_selector('.data-row')

        category_text = self.page.locator('.data-row').first.locator('td').nth(4).inner_text()
        self.assertEqual(category_text, '必需品')

    def test_edit_formula_price(self):
        """編集画面で金額入力欄に数式を入力できることを確認"""
        self._login()
        self._add_row_and_goto_edit()

        # 金額を数式で変更 =200*5 → 1000
        self.page.fill('#price', '=200*5')
        self.page.click('input[value="更新"]')

        # トップに戻る
        self.page.wait_for_url(self.live_server_url + reverse('moneybook:index'))
        self.page.wait_for_selector('.data-row')

        price_text = self.page.locator('.data-row').first.locator('td').nth(2).inner_text()
        self.assertEqual(price_text, '1,000')

    def test_edit_enter_date(self):
        """日付入力欄でEnterキーを押すと更新されることを確認"""
        self._login()
        self._add_row_and_goto_edit()

        # 日付を変更してEnter
        self.page.fill('#day', '20')
        self.page.press('#day', 'Enter')

        # トップに戻る
        self.page.wait_for_url(self.live_server_url + reverse('moneybook:index'))
        self.page.wait_for_selector('.data-row')

        now = datetime.now()
        date_text = self.page.locator('.data-row').first.locator('td').nth(0).inner_text()
        self.assertEqual(date_text, f'{now.year}/{str(now.month).zfill(2)}/20')

    def test_edit_enter_item(self):
        """項目入力欄でEnterキーを押すと更新されることを確認"""
        self._login()
        self._add_row_and_goto_edit(item='Enter項目始')

        # 項目を変更してEnter
        self.page.fill('#item', 'Enter項目後')
        self.page.press('#item', 'Enter')

        # トップに戻る
        self.page.wait_for_url(self.live_server_url + reverse('moneybook:index'))
        self.page.wait_for_selector('.data-row:has-text("Enter項目後")')

        item_text = self.page.locator('.data-row').first.locator('td').nth(1).inner_text()
        self.assertEqual(item_text, 'Enter項目後')

    def test_edit_enter_price(self):
        """金額入力欄でEnterキーを押すと更新されることを確認"""
        self._login()
        self._add_row_and_goto_edit(price='1000')

        # 金額を変更してEnter
        self.page.fill('#price', '8000')
        self.page.press('#price', 'Enter')

        # トップに戻る
        self.page.wait_for_url(self.live_server_url + reverse('moneybook:index'))
        self.page.wait_for_selector('.data-row')

        price_text = self.page.locator('.data-row').first.locator('td').nth(2).inner_text()
        self.assertEqual(price_text, '8,000')

    def test_edit_invalid_pk(self):
        """存在しないIDで編集画面にアクセスするとトップにリダイレクトされることを確認"""
        self._login()
        self.page.goto(self.live_server_url + reverse('moneybook:edit', kwargs={'pk': 999999}))

        # トップにリダイレクトされるのを待つ
        self.page.wait_for_url(self.live_server_url + reverse('moneybook:index'))
        self.assertEqual(self.page.url, self.live_server_url + reverse('moneybook:index'))
