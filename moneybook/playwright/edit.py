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

    def _wait_for_index_ajax(self):
        # jQuery AJAXの完了を待つ
        super()._wait_for_ajax()
        # summary-count が "件" 以外の数字を含む状態になるまで待つ (表示更新待ち)
        # 稀にデータが0件で "0件" となる場合があるため、それも許容する
        # ただ初期状態が "件" なので、何らかの数字が入るのを待つ
        try:
            self.page.wait_for_selector('#summary-count:not(:text-is("件"))', timeout=10000)
        except Exception:
            pass

    def _add_row_and_goto_edit(self, day='10', item='編集テスト', price='1000', method_id='2', category_id='1'):
        # 指定の年月に移動
        url = f'{self.live_server_url}/{self.test_year}/{self.test_month}'

        # 移動
        self.page.goto(url)
        # ログインしていることを確認
        self.page.wait_for_selector(f'body > header .header-cont2:has-text("{self.username}さん")')
        # AJAXロード待ち
        self._wait_for_index_ajax()

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

    def _assert_edit_form(self, year=None, month=None, day=None, item=None, price=None, method_id=None, category_id=None):
        if year:
            self.assertEqual(self.page.input_value('#year'), str(year))
        if month:
            self.assertEqual(self.page.input_value('#month'), str(month).zfill(2))
        if day:
            self.assertEqual(self.page.input_value('#day'), str(day))
        if item:
            self.assertEqual(self.page.input_value('#item'), item)
        if price:
            self.assertEqual(self.page.input_value('#price'), str(price))
        if method_id:
            self.assertTrue(self.page.is_checked(f'input[name="method"][value="{method_id}"]'))
        if category_id:
            self.assertTrue(self.page.is_checked(f'input[name="category"][value="{category_id}"]'))

    def _assert_data_row(self, item_text, date=None, price=None, method=None, category=None):
        self.page.wait_for_selector(f'.data-row:has-text("{item_text}")')
        row = self.page.locator('.data-row', has_text=item_text).first
        row.wait_for(state='visible')
        if date:
            self.assertEqual(row.locator('td').nth(0).inner_text(), date)
        if item_text:
            self.assertEqual(row.locator('td').nth(1).inner_text(), item_text)
        if price:
            self.assertEqual(row.locator('td').nth(2).inner_text(), price)
        if method:
            self.assertEqual(row.locator('td').nth(3).inner_text(), method)
        if category:
            self.assertEqual(row.locator('td').nth(4).inner_text(), category)

    def test_get(self):
        """編集画面が正しく表示されることを確認"""
        self._login()
        # ログイン後のリダイレクト待ち
        self.page.wait_for_url('**/')
        self._wait_for_index_ajax()

        item_name = self._get_unique_item('get')
        self._add_row_and_goto_edit(day='10', item=item_name, price='1000')

        # 名前表示
        header_cont2_text = self.page.inner_text('body > header .header-cont2')
        self.assertTrue(self.username + 'さん' in header_cont2_text)

        # フォームの値を確認
        self._assert_edit_form(
            year=self.test_year,
            month=self.test_month,
            day=10,
            item=item_name,
            price=1000,
            method_id='2',
            category_id='1'
        )

    def test_edit_item(self):
        """項目名を編集できることを確認"""
        self._login()
        self.page.wait_for_url('**/')
        self._wait_for_index_ajax()

        item_before = self._get_unique_item('edit_item_b')
        item_after = self._get_unique_item('edit_item_a')
        self._add_row_and_goto_edit(day='10', item=item_before, price='1000', method_id='2', category_id='1')

        # 項目名を変更
        self.page.fill('#item', item_after)
        with self.page.expect_navigation():
            self.page.click('input[value="更新"]')

        # トップに戻って確認
        self._wait_for_index_ajax()
        self._assert_data_row(
            item_text=item_after,
            date=f'{self.test_year}/{str(self.test_month).zfill(2)}/10',
            price='1,000',
            method='銀行',
            category='食費'
        )

    def test_edit_price(self):
        """金額を編集できることを確認"""
        self._login()
        self.page.wait_for_url('**/')
        self._wait_for_index_ajax()

        item_name = self._get_unique_item('edit_price')
        self._add_row_and_goto_edit(day='10', item=item_name, price='1000', method_id='2', category_id='1')

        # 金額を変更
        self.page.fill('#price', '5000')
        with self.page.expect_navigation():
            self.page.click('input[value="更新"]')

        # トップに戻って確認
        self._wait_for_index_ajax()
        self._assert_data_row(
            item_text=item_name,
            date=f'{self.test_year}/{str(self.test_month).zfill(2)}/10',
            price='5,000',
            method='銀行',
            category='食費'
        )

    def test_edit_date(self):
        """日付を編集できることを確認"""
        self._login()
        self.page.wait_for_url('**/')
        self._wait_for_index_ajax()

        item_name = self._get_unique_item('edit_date')
        self._add_row_and_goto_edit(day='10', item=item_name, price='1000', method_id='2', category_id='1')

        # 日付を変更
        self.page.fill('#day', '15')
        with self.page.expect_navigation():
            self.page.click('input[value="更新"]')

        # トップに戻る
        self._wait_for_index_ajax()
        self._assert_data_row(
            item_text=item_name,
            date=f'{self.test_year}/{str(self.test_month).zfill(2)}/15',
            price='1,000',
            method='銀行',
            category='食費'
        )

    def test_edit_method(self):
        """支払い方法を編集できることを確認"""
        self._login()
        self.page.wait_for_url('**/')
        self._wait_for_index_ajax()

        item_name = self._get_unique_item('edit_method')
        self._add_row_and_goto_edit(day='10', item=item_name, price='1000', method_id='2', category_id='1')

        # 支払い方法を現金:1 に変更
        self.page.click('label[for="method-1"]')
        with self.page.expect_navigation():
            self.page.click('input[value="更新"]')

        # トップに戻って確認
        self._wait_for_index_ajax()
        self._assert_data_row(
            item_text=item_name,
            date=f'{self.test_year}/{str(self.test_month).zfill(2)}/10',
            price='1,000',
            method='現金',
            category='食費'
        )

    def test_edit_category(self):
        """カテゴリーを編集できることを確認"""
        self._login()
        self.page.wait_for_url('**/')
        self._wait_for_index_ajax()

        item_name = self._get_unique_item('edit_cat')
        self._add_row_and_goto_edit(day='10', item=item_name, price='1000', method_id='2', category_id='1')

        # カテゴリーを必需品:2 に変更
        self.page.click('label[for="category-2"]')
        with self.page.expect_navigation():
            self.page.click('input[value="更新"]')

        # トップに戻って確認
        self._wait_for_index_ajax()
        self._assert_data_row(
            item_text=item_name,
            date=f'{self.test_year}/{str(self.test_month).zfill(2)}/10',
            price='1,000',
            method='銀行',
            category='必需品'
        )

    def test_edit_formula_price(self):
        """編集画面で金額入力欄に数式を入力できることを確認"""
        self._login()
        self.page.wait_for_url('**/')
        self._wait_for_index_ajax()

        item_name = self._get_unique_item('edit_formula')
        self._add_row_and_goto_edit(day='10', item=item_name, price='1000', method_id='2', category_id='1')

        # 金額を数式で変更 =200*5 → 1000
        self.page.fill('#price', '=200*5')
        with self.page.expect_navigation():
            self.page.click('input[value="更新"]')

        # トップに戻って確認
        self._wait_for_index_ajax()
        self._assert_data_row(
            item_text=item_name,
            date=f'{self.test_year}/{str(self.test_month).zfill(2)}/10',
            price='1,000',
            method='銀行',
            category='食費'
        )

    def test_edit_enter_date(self):
        """日付入力欄でEnterキーを押すと更新されることを確認"""
        self._login()
        self.page.wait_for_url('**/')
        self._wait_for_index_ajax()

        item_name = self._get_unique_item('enter_date')
        self._add_row_and_goto_edit(day='10', item=item_name, price='1000', method_id='2', category_id='1')

        # 日付を変更してEnter
        self.page.fill('#day', '20')
        with self.page.expect_navigation():
            self.page.press('#day', 'Enter')

        # トップに戻る
        self._wait_for_index_ajax()
        self._assert_data_row(
            item_text=item_name,
            date=f'{self.test_year}/{str(self.test_month).zfill(2)}/20',
            price='1,000',
            method='銀行',
            category='食費'
        )

    def test_edit_enter_item(self):
        """項目入力欄でEnterキーを押すと更新されることを確認"""
        self._login()
        self.page.wait_for_url('**/')
        self._wait_for_index_ajax()

        item_before = self._get_unique_item('enter_item_b')
        item_after = self._get_unique_item('enter_item_a')
        self._add_row_and_goto_edit(day='10', item=item_before, price='1000', method_id='2', category_id='1')

        # 項目を変更してEnter
        self.page.fill('#item', item_after)
        with self.page.expect_navigation():
            self.page.press('#item', 'Enter')

        # トップに戻る
        self._wait_for_index_ajax()
        self._assert_data_row(
            item_text=item_after,
            date=f'{self.test_year}/{str(self.test_month).zfill(2)}/10',
            price='1,000',
            method='銀行',
            category='食費'
        )

    def test_edit_enter_price(self):
        """金額入力欄でEnterキーを押すと更新されることを確認"""
        self._login()
        self.page.wait_for_url('**/')
        self._wait_for_index_ajax()

        item_name = self._get_unique_item('enter_price')
        self._add_row_and_goto_edit(day='10', item=item_name, price='1000', method_id='2', category_id='1')

        # 金額を変更してEnter
        self.page.fill('#price', '8000')
        with self.page.expect_navigation():
            self.page.press('#price', 'Enter')

        # トップに戻る
        self._wait_for_index_ajax()
        self._assert_data_row(
            item_text=item_name,
            date=f'{self.test_year}/{str(self.test_month).zfill(2)}/10',
            price='8,000',
            method='銀行',
            category='食費'
        )

    def test_edit_invalid_pk(self):
        """存在しないIDで編集画面にアクセスするとトップにリダイレクトされることを確認"""
        self._login()
        self.page.wait_for_url('**/')
        self.page.goto(self.live_server_url + reverse('moneybook:edit', kwargs={'pk': 999999}))

        # トップにリダイレクトされるのを待つ
        self.page.wait_for_url(self.live_server_url + reverse('moneybook:index'))
        self.assertEqual(self.page.url, self.live_server_url + reverse('moneybook:index'))
