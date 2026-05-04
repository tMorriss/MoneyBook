from datetime import datetime

from django.urls import reverse
from moneybook.playwright.base import PlaywrightBase


class EditTest(PlaywrightBase):
    def setUp(self):
        super().setUp()
        self.test_year = 2000
        self.test_month = 1
        self._test_counter = 0

    def _get_unique_item(self, prefix):
        self._test_counter += 1
        return f'{prefix}_{self._test_counter}_{datetime.now().strftime("%H%M%S")}'

    def _wait_for_ajax(self):
        # jQuery AJAXの完了を待つ
        self.page.wait_for_function('window.jQuery && window.jQuery.active == 0')
        # summary-count が "件" 以外の数字を含む状態になるまで待つ (表示更新待ち)
        self.page.wait_for_selector('#summary-count:not(:text-is("件"))', timeout=10000)

    def _add_row_and_goto_edit(self, day='10', item='編集テスト', price='1000', method_id=None, category_id=None):
        # 指定の年月に移動
        url = f'{self.live_server_url}/{self.test_year}/{self.test_month}'

        # 移動
        self.page.goto(url)
        # ログインしていることを確認
        self.page.wait_for_selector(f'.header-cont2:has-text("{self.username}さん")')
        # AJAXロード待ち
        self._wait_for_ajax()

        # フォーム入力
        self.page.fill('#a_day', day)
        self.page.fill('#a_item', item)
        self.page.fill('#a_price', price)

        if method_id:
            self.page.click(f'label[for="a_method-{method_id}"]')
        if category_id:
            self.page.click(f'label[for="a_category-{category_id}"]')

        # 追加ボタンをクリック。APIのレスポンスを待つ
        with self.page.expect_response(lambda r: '_data_table' in r.url and r.status == 200):
            self.page.click('input[value="追加"]')

        # テーブルの更新完了を待つ (追加した品目が表示されるまで)
        target_row = self.page.locator('.data-row', has_text=item).first
        target_row.wait_for(state='visible')

        # 編集画面に移動
        target_row.locator('.a-edit a').click()
        # 編集画面のロード完了（要素の出現）を待つ
        self.page.wait_for_selector('#item', state='visible')

    def test_get(self):
        """編集画面が正しく表示されることを確認"""
        self._login()
        # ログイン後のリダイレクト待ち
        self.page.wait_for_url('**/')
        self._wait_for_ajax()

        item_name = self._get_unique_item('get')
        self._add_row_and_goto_edit(day='10', item=item_name, price='1000')

        # 名前表示
        header_cont2_text = self.page.inner_text('.header-cont2')
        self.assertTrue(self.username + 'さん' in header_cont2_text)

        # フォームの値を確認
        self.assertEqual(self.page.input_value('#year'), str(self.test_year))
        self.assertEqual(self.page.input_value('#month'), str(self.test_month).zfill(2))
        self.assertEqual(self.page.input_value('#day'), '10')
        self.assertEqual(self.page.input_value('#item'), item_name)
        self.assertEqual(self.page.input_value('#price'), '1000')

        # 支払い方法と分類が正しく選択されていることを確認
        self.assertTrue(self.page.is_checked('input[name="method"][value="2"]'))  # 銀行
        self.assertTrue(self.page.is_checked('input[name="category"][value="1"]'))  # 食費

    def test_edit_item(self):
        """項目名を編集できることを確認"""
        self._login()
        self.page.wait_for_url('**/')
        self._wait_for_ajax()

        item_before = self._get_unique_item('edit_item_b')
        item_after = self._get_unique_item('edit_item_a')
        self._add_row_and_goto_edit(item=item_before)

        # 項目名を変更
        self.page.fill('#item', item_after)
        with self.page.expect_navigation():
            self.page.click('input[value="更新"]')

        # トップに戻って確認
        # AJAXロード待ち
        self._wait_for_ajax()
        self.page.wait_for_selector(f'.data-row:has-text("{item_after}")')
        item_text = self.page.locator('.data-row', has_text=item_after).first.locator('td').nth(1).inner_text()
        self.assertEqual(item_text, item_after)

    def test_edit_price(self):
        """金額を編集できることを確認"""
        self._login()
        self.page.wait_for_url('**/')
        self._wait_for_ajax()

        item_name = self._get_unique_item('edit_price')
        self._add_row_and_goto_edit(price='1000', item=item_name)

        # 金額を変更
        self.page.fill('#price', '5000')
        with self.page.expect_navigation():
            self.page.click('input[value="更新"]')

        # トップに戻って確認
        self._wait_for_ajax()
        self.page.wait_for_selector(f'.data-row:has-text("{item_name}")')
        row = self.page.locator('.data-row', has_text=item_name).filter(has_text='5,000').first
        row.wait_for()
        price_text = row.locator('td').nth(2).inner_text()
        self.assertEqual(price_text, '5,000')

    def test_edit_date(self):
        """日付を編集できることを確認"""
        self._login()
        self.page.wait_for_url('**/')
        self._wait_for_ajax()

        item_name = self._get_unique_item('edit_date')
        self._add_row_and_goto_edit(item=item_name)

        # 日付を変更
        self.page.fill('#day', '15')
        with self.page.expect_navigation():
            self.page.click('input[value="更新"]')

        # トップに戻る
        self._wait_for_ajax()
        target_date = f'{self.test_year}/{str(self.test_month).zfill(2)}/15'
        self.page.wait_for_selector(f'.data-row:has-text("{item_name}")')
        row = self.page.locator('.data-row', has_text=item_name).filter(has_text=target_date).first
        row.wait_for()
        date_text = row.locator('td').nth(0).inner_text()
        self.assertEqual(date_text, target_date)

    def test_edit_method(self):
        """支払い方法を編集できることを確認"""
        self._login()
        self.page.wait_for_url('**/')
        self._wait_for_ajax()

        item_name = self._get_unique_item('edit_method')
        self._add_row_and_goto_edit(method_id='2', item=item_name)

        # 支払い方法を現金:1 に変更
        self.page.click('label[for="method-1"]')
        with self.page.expect_navigation():
            self.page.click('input[value="更新"]')

        # トップに戻って確認
        self._wait_for_ajax()
        self.page.wait_for_selector(f'.data-row:has-text("{item_name}")')
        row = self.page.locator('.data-row', has_text=item_name).filter(has_text='現金').first
        row.wait_for()
        method_text = row.locator('td').nth(3).inner_text()
        self.assertEqual(method_text, '現金')

    def test_edit_category(self):
        """カテゴリーを編集できることを確認"""
        self._login()
        self.page.wait_for_url('**/')
        self._wait_for_ajax()

        item_name = self._get_unique_item('edit_cat')
        self._add_row_and_goto_edit(category_id='1', item=item_name)

        # カテゴリーを必需品:2 に変更
        self.page.click('label[for="category-2"]')
        with self.page.expect_navigation():
            self.page.click('input[value="更新"]')

        # トップに戻って確認
        self._wait_for_ajax()
        self.page.wait_for_selector(f'.data-row:has-text("{item_name}")')
        row = self.page.locator('.data-row', has_text=item_name).filter(has_text='必需品').first
        row.wait_for()
        category_text = row.locator('td').nth(4).inner_text()
        self.assertEqual(category_text, '必需品')

    def test_edit_formula_price(self):
        """編集画面で金額入力欄に数式を入力できることを確認"""
        self._login()
        self.page.wait_for_url('**/')
        self._wait_for_ajax()

        item_name = self._get_unique_item('edit_formula')
        self._add_row_and_goto_edit(item=item_name)

        # 金額を数式で変更 =200*5 → 1000
        self.page.fill('#price', '=200*5')
        with self.page.expect_navigation():
            self.page.click('input[value="更新"]')

        # トップに戻って確認
        self._wait_for_ajax()
        self.page.wait_for_selector(f'.data-row:has-text("{item_name}")')
        row = self.page.locator('.data-row', has_text=item_name).filter(has_text='1,000').first
        row.wait_for()
        price_text = row.locator('td').nth(2).inner_text()
        self.assertEqual(price_text, '1,000')

    def test_edit_enter_date(self):
        """日付入力欄でEnterキーを押すと更新されることを確認"""
        self._login()
        self.page.wait_for_url('**/')
        self._wait_for_ajax()

        item_name = self._get_unique_item('enter_date')
        self._add_row_and_goto_edit(item=item_name)

        # 日付を変更してEnter
        self.page.fill('#day', '20')
        with self.page.expect_navigation():
            self.page.press('#day', 'Enter')

        # トップに戻る
        self._wait_for_ajax()
        target_date = f'{self.test_year}/{str(self.test_month).zfill(2)}/20'
        self.page.wait_for_selector(f'.data-row:has-text("{item_name}")')
        row = self.page.locator('.data-row', has_text=item_name).filter(has_text=target_date).first
        row.wait_for()
        date_text = row.locator('td').nth(0).inner_text()
        self.assertEqual(date_text, target_date)

    def test_edit_enter_item(self):
        """項目入力欄でEnterキーを押すと更新されることを確認"""
        self._login()
        self.page.wait_for_url('**/')
        self._wait_for_ajax()

        item_before = self._get_unique_item('enter_item_b')
        item_after = self._get_unique_item('enter_item_a')
        self._add_row_and_goto_edit(item=item_before)

        # 項目を変更してEnter
        self.page.fill('#item', item_after)
        with self.page.expect_navigation():
            self.page.press('#item', 'Enter')

        # トップに戻る
        self._wait_for_ajax()
        self.page.wait_for_selector(f'.data-row:has-text("{item_after}")')
        item_text = self.page.locator('.data-row', has_text=item_after).first.locator('td').nth(1).inner_text()
        self.assertEqual(item_text, item_after)

    def test_edit_enter_price(self):
        """金額入力欄でEnterキーを押すと更新されることを確認"""
        self._login()
        self.page.wait_for_url('**/')
        self._wait_for_ajax()

        item_name = self._get_unique_item('enter_price')
        self._add_row_and_goto_edit(price='1000', item=item_name)

        # 金額を変更してEnter
        self.page.fill('#price', '8000')
        with self.page.expect_navigation():
            self.page.press('#price', 'Enter')

        # トップに戻る
        self._wait_for_ajax()
        self.page.wait_for_selector(f'.data-row:has-text("{item_name}")')
        row = self.page.locator('.data-row', has_text=item_name).filter(has_text='8,000').first
        row.wait_for()
        price_text = row.locator('td').nth(2).inner_text()
        self.assertEqual(price_text, '8,000')

    def test_edit_invalid_pk(self):
        """存在しないIDで編集画面にアクセスするとトップにリダイレクトされることを確認"""
        self._login()
        self.page.wait_for_url('**/')
        self.page.goto(self.live_server_url + reverse('moneybook:edit', kwargs={'pk': 999999}))

        # トップにリダイレクトされるのを待つ
        self.page.wait_for_url(self.live_server_url + reverse('moneybook:index'))
        self.assertEqual(self.page.url, self.live_server_url + reverse('moneybook:index'))
