from datetime import datetime

from django.urls import reverse
from moneybook.e2e.base import PlaywrightBase
from playwright.sync_api import expect


class Add(PlaywrightBase):
    def _assert_bank_charge_kyash(self, method):
        now = datetime.now()
        self._location(self.live_server_url + reverse('moneybook:index'))
        self._wait_for_ajax()
        self.page.wait_for_selector('#transactions table tbody tr')

        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(3)

        # 1つ目のデータ (移動先への収入)
        tds1 = rows.nth(1).locator('td')
        expect(tds1.nth(0)).to_have_text(f'{now.year}/{str(now.month).zfill(2)}/01')
        expect(tds1.nth(1)).to_have_text(f'{method}チャージ')
        expect(tds1.nth(2)).to_have_text('100')
        expect(tds1.nth(3)).to_have_text(method)
        expect(tds1.nth(4)).to_have_text('内部移動')
        expect(rows.nth(1)).to_have_css('background-color', 'rgba(0, 0, 0, 0)')

        # direction確認 (編集画面へ移動して確認)
        tds1.nth(5).locator('a').click()
        self.page.wait_for_load_state('load')
        # 収入(1つ目のラジオボタン)が選択されていること
        expect(self.page.locator('input[name="direction"]').nth(0)).to_be_checked()

        # 再度インデックスへ
        self._location(self.live_server_url + reverse('moneybook:index'))
        self._wait_for_ajax()
        self.page.wait_for_selector('#transactions table tbody tr')
        rows = self.page.locator('#transactions table tbody tr')

        # 2つ目のデータ (移動元からの支出)
        tds2 = rows.nth(2).locator('td')
        expect(tds2.nth(0)).to_have_text(f'{now.year}/{str(now.month).zfill(2)}/01')
        expect(tds2.nth(1)).to_have_text(f'{method}チャージ')
        expect(tds2.nth(2)).to_have_text('100')
        expect(tds2.nth(3)).to_have_text('銀行')
        expect(tds2.nth(4)).to_have_text('内部移動')
        expect(rows.nth(2)).to_have_css('background-color', 'rgba(0, 0, 0, 0)')

        # direction確認
        tds2.nth(5).locator('a').click()
        self.page.wait_for_load_state('load')
        # 支出(2つ目のラジオボタン)が選択されていること
        expect(self.page.locator('input[name="direction"]').nth(1)).to_be_checked()

    def _assert_intra_move(self):
        now = datetime.now()
        self._location(self.live_server_url + reverse('moneybook:index'))
        self._wait_for_ajax()
        self.page.wait_for_selector('#transactions table tbody tr')

        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(3)

        # 1つ目のデータ (移動先への収入)
        tds1 = rows.nth(1).locator('td')
        expect(tds1.nth(0)).to_have_text(f'{now.year}/{str(now.month).zfill(2)}/02')
        expect(tds1.nth(1)).to_have_text('ないぶいどう')
        expect(tds1.nth(2)).to_have_text('200')
        expect(tds1.nth(3)).to_have_text('Kyash')
        expect(tds1.nth(4)).to_have_text('内部移動')
        expect(rows.nth(1)).to_have_css('background-color', 'rgba(0, 0, 0, 0)')

        # direction確認
        tds1.nth(5).locator('a').click()
        self.page.wait_for_load_state('load')
        expect(self.page.locator('input[name="direction"]').nth(0)).to_be_checked()

        # 再度インデックスへ
        self._location(self.live_server_url + reverse('moneybook:index'))
        self._wait_for_ajax()
        self.page.wait_for_selector('#transactions table tbody tr')
        rows = self.page.locator('#transactions table tbody tr')

        # 2つ目のデータ (移動元からの支出)
        tds2 = rows.nth(2).locator('td')
        expect(tds2.nth(0)).to_have_text(f'{now.year}/{str(now.month).zfill(2)}/02')
        expect(tds2.nth(1)).to_have_text('ないぶいどう')
        expect(tds2.nth(2)).to_have_text('200')
        expect(tds2.nth(3)).to_have_text('現金')
        expect(tds2.nth(4)).to_have_text('内部移動')
        expect(rows.nth(2)).to_have_css('background-color', 'rgba(0, 0, 0, 0)')

        # direction確認
        tds2.nth(5).locator('a').click()
        self.page.wait_for_load_state('load')
        expect(self.page.locator('input[name="direction"]').nth(1)).to_be_checked()

    def test_get(self):
        now = datetime.now()
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self._assert_common()

        # 銀行チャージフォーム
        expect(self.page.locator('#c_year')).to_have_value(str(now.year))
        expect(self.page.locator('#c_month')).to_have_value(str(now.month))
        expect(self.page.locator('#c_day')).to_have_value('')
        expect(self.page.locator('#c_price')).to_have_value('')
        expects = ['Kyash', 'PayPay']
        # labels for c_method
        actuals = self.page.locator('input[name="c_method"] + label')
        expect(actuals).to_have_text(expects)

        # 内部移動フォーム
        expect(self.page.locator('#m_year')).to_have_value(str(now.year))
        expect(self.page.locator('#m_month')).to_have_value(str(now.month))
        expect(self.page.locator('#m_day')).to_have_value('')
        expect(self.page.locator('#m_item')).to_have_value('')
        expect(self.page.locator('#m_price')).to_have_value('')
        expects = ['銀行', '現金', 'Kyash', 'PayPay']
        expect(self.page.locator('input[name="m_before_method"] + label')).to_have_text(expects)
        expect(self.page.locator('input[name="m_after_method"] + label')).to_have_text(expects)

        # ショートカットフォーム
        expect(self.page.locator('#s_year')).to_have_value(str(now.year))
        expect(self.page.locator('#s_month')).to_have_value(str(now.month))
        expect(self.page.locator('#s_day')).to_have_value('')
        expect(self.page.locator('#s_day')).to_have_attribute('placeholder', str(now.day))
        expect(self.page.locator('#s_price')).to_have_value('')
        expect(self.page.locator('#s_price')).to_have_attribute('placeholder', '1000')
        expect(self.page.locator('input[onclick*="Suicaチャージ"]')).to_have_value('Suicaチャージ')

        # 収入支出追加フォーム
        expect(self.page.locator('#a_year')).to_have_value(str(now.year))
        expect(self.page.locator('#a_month')).to_have_value(str(now.month))
        expect(self.page.locator('#a_day')).to_have_value('')
        expect(self.page.locator('#a_item')).to_have_value('')
        expect(self.page.locator('#a_price')).to_have_value('')
        expect(self.page.locator('input[name="a_direction"] + label')).to_have_text(['収入', '支出'])
        expect(self.page.locator('input[name="a_method"] + label')).to_have_text(['銀行', '現金', 'Kyash', 'PayPay'])
        expects = ['食費', '必需品', '交通費', 'その他', '内部移動', '貯金', '計算外', '収入']
        expect(self.page.locator('input[name="a_category"] + label')).to_have_text(expects)
        expect(self.page.locator('input[name="a_temp"] + label')).to_have_text(['No', 'Yes'])

    def test_bank_charge_click(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#c_day', '1')
        self.page.fill('#c_price', '100')
        self.page.click('h1:has-text("銀行チャージ") + form input[type="button"]')

        self._assert_bank_charge_kyash('Kyash')

    def test_bank_charge_year_enter(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#c_day', '1')
        self.page.fill('#c_price', '100')
        self.page.press('#c_year', 'Enter')

        self._assert_bank_charge_kyash('Kyash')

    def test_bank_charge_month_enter(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#c_day', '1')
        self.page.fill('#c_price', '100')
        self.page.press('#c_month', 'Enter')

        self._assert_bank_charge_kyash('Kyash')

    def test_bank_charge_day_enter(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#c_day', '1')
        self.page.fill('#c_price', '100')
        self.page.press('#c_day', 'Enter')

        self._assert_bank_charge_kyash('Kyash')

    def test_bank_charge_price_enter(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#c_day', '1')
        self.page.fill('#c_price', '100')
        self.page.press('#c_price', 'Enter')

        self._assert_bank_charge_kyash('Kyash')

    def test_bank_charge_method_enter(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#c_day', '1')
        self.page.fill('#c_price', '100')
        # 最初のメソッド(Kyash)のinput要素でEnter
        self.page.locator('input[name="c_method"]').nth(0).press('Enter')

        self._assert_bank_charge_kyash('Kyash')

    def test_bank_charge_select(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#c_day', '1')
        self.page.fill('#c_price', '100')
        # PayPayを選択 (2番目のラベル)
        self.page.locator('input[name="c_method"] + label').nth(1).click()
        self.page.click('h1:has-text("銀行チャージ") + form input[type="button"]')

        self._assert_bank_charge_kyash('PayPay')

    def test_bank_charge_reset(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#c_day', '1')
        self.page.fill('#c_price', '100')
        self.page.locator('input[name="c_method"] + label').nth(1).click()  # PayPay
        self.page.click('h1:has-text("銀行チャージ") + form input[type="button"]')

        # 成功後に1番目(Kyash)が選択されていること
        # AJAXでの更新を待つ
        expect(self.page.locator('input[name="c_method"]').nth(0)).to_be_checked()
        expect(self.page.locator('input[name="c_method"]').nth(1)).not_to_be_checked()

    def test_intra_move_click(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#m_day', '2')
        self.page.fill('#m_item', 'ないぶいどう')
        self.page.fill('#m_price', '200')
        self.page.locator('input[name="m_before_method"] + label').nth(1).click()  # 現金
        self.page.locator('input[name="m_after_method"] + label').nth(2).click()  # Kyash
        self.page.click('h1:has-text("内部移動追加") + form input[type="button"]')

        self._assert_intra_move()

    def test_intra_move_year(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#m_day', '2')
        self.page.fill('#m_item', 'ないぶいどう')
        self.page.fill('#m_price', '200')
        self.page.locator('input[name="m_before_method"] + label').nth(1).click()
        self.page.locator('input[name="m_after_method"] + label').nth(2).click()
        self.page.press('#m_year', 'Enter')

        self._assert_intra_move()

    def test_intra_move_month(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#m_day', '2')
        self.page.fill('#m_item', 'ないぶいどう')
        self.page.fill('#m_price', '200')
        self.page.locator('input[name="m_before_method"] + label').nth(1).click()
        self.page.locator('input[name="m_after_method"] + label').nth(2).click()
        self.page.press('#m_month', 'Enter')

        self._assert_intra_move()

    def test_intra_move_day(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#m_day', '2')
        self.page.fill('#m_item', 'ないぶいどう')
        self.page.fill('#m_price', '200')
        self.page.locator('input[name="m_before_method"] + label').nth(1).click()
        self.page.locator('input[name="m_after_method"] + label').nth(2).click()
        self.page.press('#m_day', 'Enter')

        self._assert_intra_move()

    def test_intra_move_item(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#m_day', '2')
        self.page.fill('#m_item', 'ないぶいどう')
        self.page.fill('#m_price', '200')
        self.page.locator('input[name="m_before_method"] + label').nth(1).click()
        self.page.locator('input[name="m_after_method"] + label').nth(2).click()
        self.page.press('#m_item', 'Enter')

        self._assert_intra_move()

    def test_intra_move_price(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#m_day', '2')
        self.page.fill('#m_item', 'ないぶいどう')
        self.page.fill('#m_price', '200')
        self.page.locator('input[name="m_before_method"] + label').nth(1).click()
        self.page.locator('input[name="m_after_method"] + label').nth(2).click()
        self.page.press('#m_price', 'Enter')

        self._assert_intra_move()

    def test_intra_move_before(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#m_day', '2')
        self.page.fill('#m_item', 'ないぶいどう')
        self.page.fill('#m_price', '200')
        self.page.locator('input[name="m_before_method"] + label').nth(1).click()
        self.page.locator('input[name="m_after_method"] + label').nth(2).click()
        # 移動元のinputでEnter
        self.page.locator('input[name="m_before_method"]').nth(1).press('Enter')

        self._assert_intra_move()

    def test_intra_move_after(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#m_day', '2')
        self.page.fill('#m_item', 'ないぶいどう')
        self.page.fill('#m_price', '200')
        self.page.locator('input[name="m_before_method"] + label').nth(1).click()
        self.page.locator('input[name="m_after_method"] + label').nth(2).click()
        # 移動先のinputでEnter
        self.page.locator('input[name="m_after_method"]').nth(2).press('Enter')

        self._assert_intra_move()

    def test_suica_charge(self):
        now = datetime.now()
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#s_day', '4')
        self.page.fill('#s_price', '400')
        self.page.click('input[value="Suicaチャージ"]')

        self._location(self.live_server_url + reverse('moneybook:index'))
        self._wait_for_ajax()
        self.page.wait_for_selector('#transactions table tbody tr')
        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(2)
        tds = rows.nth(1).locator('td')
        expect(tds.nth(0)).to_have_text(f'{now.year}/{str(now.month).zfill(2)}/04')
        expect(tds.nth(1)).to_have_text('Suicaチャージ')
        expect(tds.nth(2)).to_have_text('400')
        expect(tds.nth(3)).to_have_text('銀行')
        expect(tds.nth(4)).to_have_text('交通費')
        expect(rows.nth(1)).to_have_css('background-color', 'rgba(0, 0, 0, 0)')

        # direction確認
        tds.nth(5).locator('a').click()
        self.page.wait_for_load_state('load')
        # 支出(2つ目のラジオボタン)が選択されていること
        expect(self.page.locator('input[name="direction"]').nth(1)).to_be_checked()

    def test_suica_charge_default_day(self):
        now = datetime.now()
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#s_price', '400')
        self.page.click('input[value="Suicaチャージ"]')

        self._location(self.live_server_url + reverse('moneybook:index'))
        self._wait_for_ajax()
        self.page.wait_for_selector('#transactions table tbody tr')
        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(2)
        tds = rows.nth(1).locator('td')
        expect(tds.nth(0)).to_have_text(f'{now.year}/{str(now.month).zfill(2)}/{str(now.day).zfill(2)}')
        expect(tds.nth(1)).to_have_text('Suicaチャージ')
        expect(tds.nth(2)).to_have_text('400')
        expect(tds.nth(3)).to_have_text('銀行')
        expect(tds.nth(4)).to_have_text('交通費')

    def test_suica_charge_default_price(self):
        now = datetime.now()
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#s_day', '5')
        self.page.click('input[value="Suicaチャージ"]')

        self._location(self.live_server_url + reverse('moneybook:index'))
        self._wait_for_ajax()
        self.page.wait_for_selector('#transactions table tbody tr')
        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(2)
        tds = rows.nth(1).locator('td')
        expect(tds.nth(0)).to_have_text(f'{now.year}/{str(now.month).zfill(2)}/05')
        expect(tds.nth(1)).to_have_text('Suicaチャージ')
        expect(tds.nth(2)).to_have_text('1,000')
        expect(tds.nth(3)).to_have_text('銀行')
        expect(tds.nth(4)).to_have_text('交通費')

    def test_suica_charge_all_defaults(self):
        now = datetime.now()
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.click('input[value="Suicaチャージ"]')

        self._location(self.live_server_url + reverse('moneybook:index'))
        self._wait_for_ajax()
        self.page.wait_for_selector('#transactions table tbody tr')
        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(2)
        tds = rows.nth(1).locator('td')
        expect(tds.nth(0)).to_have_text(f'{now.year}/{str(now.month).zfill(2)}/{str(now.day).zfill(2)}')
        expect(tds.nth(1)).to_have_text('Suicaチャージ')
        expect(tds.nth(2)).to_have_text('1,000')
        expect(tds.nth(3)).to_have_text('銀行')
        expect(tds.nth(4)).to_have_text('交通費')

    def test_train_fare_shortcut(self):
        now = datetime.now()
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#s_day', '6')
        self.page.fill('#s_price', '600')
        self.page.click('input[value="電車代"]')

        self._location(self.live_server_url + reverse('moneybook:index'))
        self._wait_for_ajax()
        self.page.wait_for_selector('#transactions table tbody tr')
        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(2)
        tds = rows.nth(1).locator('td')
        expect(tds.nth(0)).to_have_text(f'{now.year}/{str(now.month).zfill(2)}/06')
        expect(tds.nth(1)).to_have_text('電車代')
        expect(tds.nth(2)).to_have_text('600')
        expect(tds.nth(3)).to_have_text('銀行')
        expect(tds.nth(4)).to_have_text('交通費')

        # direction確認
        tds.nth(5).locator('a').click()
        self.page.wait_for_load_state('load')
        expect(self.page.locator('input[name="direction"]').nth(1)).to_be_checked()

    def test_train_fare_shortcut_default_day(self):
        now = datetime.now()
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#s_price', '600')
        self.page.click('input[value="電車代"]')

        self._location(self.live_server_url + reverse('moneybook:index'))
        self._wait_for_ajax()
        self.page.wait_for_selector('#transactions table tbody tr')
        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(2)
        tds = rows.nth(1).locator('td')
        expect(tds.nth(0)).to_have_text(f'{now.year}/{str(now.month).zfill(2)}/{str(now.day).zfill(2)}')
        expect(tds.nth(1)).to_have_text('電車代')
        expect(tds.nth(2)).to_have_text('600')
        expect(tds.nth(3)).to_have_text('銀行')
        expect(tds.nth(4)).to_have_text('交通費')

    def test_train_fare_shortcut_default_price(self):
        now = datetime.now()
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#s_day', '7')
        self.page.click('input[value="電車代"]')

        self._location(self.live_server_url + reverse('moneybook:index'))
        self._wait_for_ajax()
        self.page.wait_for_selector('#transactions table tbody tr')
        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(2)
        tds = rows.nth(1).locator('td')
        expect(tds.nth(0)).to_have_text(f'{now.year}/{str(now.month).zfill(2)}/07')
        expect(tds.nth(1)).to_have_text('電車代')
        expect(tds.nth(2)).to_have_text('1,000')
        expect(tds.nth(3)).to_have_text('銀行')
        expect(tds.nth(4)).to_have_text('交通費')

    def test_train_fare_shortcut_all_defaults(self):
        now = datetime.now()
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.click('input[value="電車代"]')

        self._location(self.live_server_url + reverse('moneybook:index'))
        self._wait_for_ajax()
        self.page.wait_for_selector('#transactions table tbody tr')
        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(2)
        tds = rows.nth(1).locator('td')
        expect(tds.nth(0)).to_have_text(f'{now.year}/{str(now.month).zfill(2)}/{str(now.day).zfill(2)}')
        expect(tds.nth(1)).to_have_text('電車代')
        expect(tds.nth(2)).to_have_text('1,000')
        expect(tds.nth(3)).to_have_text('銀行')
        expect(tds.nth(4)).to_have_text('交通費')

    def test_manual_add_click(self):
        now = datetime.now()
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#a_day', '5')
        self.page.fill('#a_item', 'マニュアルテスト')
        self.page.fill('#a_price', '500')
        self.page.locator('input[name="a_direction"] + label').nth(1).click()  # 支出
        self.page.locator('input[name="a_method"] + label').nth(1).click()  # 現金
        self.page.locator('input[name="a_category"] + label').nth(1).click()  # 必需品
        self.page.click('h1:has-text("収入支出追加") + form input[type="button"]')

        self._location(self.live_server_url + reverse('moneybook:index'))
        self._wait_for_ajax()
        self.page.wait_for_selector('#transactions table tbody tr')
        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(2)
        tds = rows.nth(1).locator('td')
        expect(tds.nth(0)).to_have_text(f'{now.year}/{str(now.month).zfill(2)}/05')
        expect(tds.nth(1)).to_have_text('マニュアルテスト')
        expect(tds.nth(2)).to_have_text('500')
        expect(tds.nth(3)).to_have_text('現金')
        expect(tds.nth(4)).to_have_text('必需品')
        expect(rows.nth(1)).to_have_css('background-color', 'rgba(0, 0, 0, 0)')

        # direction確認
        tds.nth(5).locator('a').click()
        self.page.wait_for_load_state('load')
        expect(self.page.locator('input[name="direction"]').nth(1)).to_be_checked()

    def test_manual_add_year(self):
        now = datetime.now()
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#a_day', '5')
        self.page.fill('#a_item', 'マニュアルテスト')
        self.page.fill('#a_price', '500')
        self.page.press('#a_year', 'Enter')

        self._location(self.live_server_url + reverse('moneybook:index'))
        self._wait_for_ajax()
        self.page.wait_for_selector('#transactions table tbody tr')
        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(2)
        tds = rows.nth(1).locator('td')
        expect(tds.nth(0)).to_have_text(f'{now.year}/{str(now.month).zfill(2)}/05')
        expect(tds.nth(1)).to_have_text('マニュアルテスト')
        expect(tds.nth(2)).to_have_text('500')
        expect(tds.nth(3)).to_have_text('銀行')
        expect(tds.nth(4)).to_have_text('食費')
        expect(rows.nth(1)).to_have_css('background-color', 'rgba(0, 0, 0, 0)')

        # direction確認
        tds.nth(5).locator('a').click()
        self.page.wait_for_load_state('load')
        # 収入(1つ目のラジオボタン)が選択されていること
        expect(self.page.locator('input[name="direction"]').nth(0)).to_be_checked()

    def test_manual_add_month(self):
        now = datetime.now()
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#a_day', '5')
        self.page.fill('#a_item', 'マニュアルテスト')
        self.page.fill('#a_price', '500')
        self.page.press('#a_month', 'Enter')

        self._location(self.live_server_url + reverse('moneybook:index'))
        self._wait_for_ajax()
        self.page.wait_for_selector('#transactions table tbody tr')
        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(2)
        tds = rows.nth(1).locator('td')
        expect(tds.nth(0)).to_have_text(f'{now.year}/{str(now.month).zfill(2)}/05')
        expect(tds.nth(1)).to_have_text('マニュアルテスト')
        expect(tds.nth(2)).to_have_text('500')
        expect(tds.nth(3)).to_have_text('銀行')
        expect(tds.nth(4)).to_have_text('食費')
        expect(rows.nth(1)).to_have_css('background-color', 'rgba(0, 0, 0, 0)')

        # direction確認
        tds.nth(5).locator('a').click()
        self.page.wait_for_load_state('load')
        expect(self.page.locator('input[name="direction"]').nth(0)).to_be_checked()

    def test_manual_add_day(self):
        now = datetime.now()
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#a_day', '5')
        self.page.fill('#a_item', 'マニュアルテスト')
        self.page.fill('#a_price', '500')
        self.page.press('#a_day', 'Enter')

        self._location(self.live_server_url + reverse('moneybook:index'))
        self._wait_for_ajax()
        self.page.wait_for_selector('#transactions table tbody tr')
        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(2)
        tds = rows.nth(1).locator('td')
        expect(tds.nth(0)).to_have_text(f'{now.year}/{str(now.month).zfill(2)}/05')
        expect(tds.nth(1)).to_have_text('マニュアルテスト')
        expect(tds.nth(2)).to_have_text('500')
        expect(tds.nth(3)).to_have_text('銀行')
        expect(tds.nth(4)).to_have_text('食費')
        expect(rows.nth(1)).to_have_css('background-color', 'rgba(0, 0, 0, 0)')

        # direction確認
        tds.nth(5).locator('a').click()
        self.page.wait_for_load_state('load')
        expect(self.page.locator('input[name="direction"]').nth(0)).to_be_checked()

    def test_manual_add_item(self):
        now = datetime.now()
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#a_day', '5')
        self.page.fill('#a_item', 'マニュアルテスト')
        self.page.fill('#a_price', '500')
        self.page.press('#a_item', 'Enter')

        self._location(self.live_server_url + reverse('moneybook:index'))
        self._wait_for_ajax()
        self.page.wait_for_selector('#transactions table tbody tr')
        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(2)
        tds = rows.nth(1).locator('td')
        expect(tds.nth(0)).to_have_text(f'{now.year}/{str(now.month).zfill(2)}/05')
        expect(tds.nth(1)).to_have_text('マニュアルテスト')
        expect(tds.nth(2)).to_have_text('500')
        expect(tds.nth(3)).to_have_text('銀行')
        expect(tds.nth(4)).to_have_text('食費')
        expect(rows.nth(1)).to_have_css('background-color', 'rgba(0, 0, 0, 0)')

        # direction確認
        tds.nth(5).locator('a').click()
        self.page.wait_for_load_state('load')
        expect(self.page.locator('input[name="direction"]').nth(0)).to_be_checked()

    def test_manual_add_price(self):
        now = datetime.now()
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#a_day', '5')
        self.page.fill('#a_item', 'マニュアルテスト')
        self.page.fill('#a_price', '500')
        self.page.press('#a_price', 'Enter')

        self._location(self.live_server_url + reverse('moneybook:index'))
        self._wait_for_ajax()
        self.page.wait_for_selector('#transactions table tbody tr')
        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(2)
        tds = rows.nth(1).locator('td')
        expect(tds.nth(0)).to_have_text(f'{now.year}/{str(now.month).zfill(2)}/05')
        expect(tds.nth(1)).to_have_text('マニュアルテスト')
        expect(tds.nth(2)).to_have_text('500')
        expect(tds.nth(3)).to_have_text('銀行')
        expect(tds.nth(4)).to_have_text('食費')
        expect(rows.nth(1)).to_have_css('background-color', 'rgba(0, 0, 0, 0)')

        # direction確認
        tds.nth(5).locator('a').click()
        self.page.wait_for_load_state('load')
        expect(self.page.locator('input[name="direction"]').nth(0)).to_be_checked()

    def test_manual_add_tmp(self):
        now = datetime.now()
        self._login()
        self._location(self.live_server_url + reverse('moneybook:add'))

        self.page.fill('#a_day', '5')
        self.page.fill('#a_item', 'マニュアルテスト')
        self.page.fill('#a_price', '500')
        self.page.locator('input[name="a_temp"] + label').nth(1).click()  # Yes
        self.page.click('h1:has-text("収入支出追加") + form input[type="button"]')

        self._location(self.live_server_url + reverse('moneybook:index'))
        self._wait_for_ajax()
        self.page.wait_for_selector('#transactions table tbody tr')
        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(2)
        tds = rows.nth(1).locator('td')
        expect(tds.nth(0)).to_have_text(f'{now.year}/{str(now.month).zfill(2)}/05')
        expect(tds.nth(1)).to_have_text('マニュアルテスト')
        expect(tds.nth(2)).to_have_text('500')
        expect(tds.nth(3)).to_have_text('銀行')
        expect(tds.nth(4)).to_have_text('立替')
        expect(rows.nth(1)).to_have_css('background-color', 'rgba(0, 0, 0, 0)')

        # direction確認
        tds.nth(5).locator('a').click()
        self.page.wait_for_load_state('load')
        # 収入(1つ目のラジオボタン)が選択されていること (立替Yes + 食費(支出) = 収入)
        expect(self.page.locator('input[name="direction"]').nth(0)).to_be_checked()

    def test_add_formula_normal_form(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index'))
        self._wait_for_ajax()
        # count() は Locator の現在の要素数を即座に返す。
        # _wait_for_ajax しているが、テーブルがレンダリングされるまで待つ必要がある。
        self.page.wait_for_selector('#transactions table tbody tr')
        initial_count = self.page.locator('#transactions table tbody tr').count()

        self._location(self.live_server_url + reverse('moneybook:add'))
        self.page.fill('#a_day', '15')
        self.page.fill('#a_item', 'add数式')
        self.page.fill('#a_price', '=50*3')
        self.page.click('h1:has-text("収入支出追加") + form input[type="button"]')
        # 送信後の待ち。result_messageの出現を待つ
        expect(self.page.locator('#result_message')).to_be_visible()

        self._location(self.live_server_url + reverse('moneybook:index'))
        self._wait_for_ajax()
        self.page.wait_for_selector('#transactions table tbody tr')
        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(initial_count + 1)
        tds = rows.nth(1).locator('td')
        expect(tds.nth(1)).to_have_text('add数式')
        expect(tds.nth(2)).to_have_text('150')

    def test_add_formula_internal_transfer(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index'))
        self._wait_for_ajax()
        self.page.wait_for_selector('#transactions table tbody tr')
        initial_count = self.page.locator('#transactions table tbody tr').count()

        self._location(self.live_server_url + reverse('moneybook:add'))
        self.page.fill('#m_day', '16')
        self.page.fill('#m_item', 'add数式')
        self.page.fill('#m_price', '=100+200')
        self.page.click('h1:has-text("内部移動追加") + form input[type="button"]')
        expect(self.page.locator('#result_message')).to_be_visible()

        self._location(self.live_server_url + reverse('moneybook:index'))
        self._wait_for_ajax()
        self.page.wait_for_selector('#transactions table tbody tr')
        rows = self.page.locator('#transactions table tbody tr')
        # 内部移動は2件追加される
        expect(rows).to_have_count(initial_count + 2)
        tds = rows.nth(1).locator('td')
        expect(tds.nth(1)).to_have_text('add数式')
        expect(tds.nth(2)).to_have_text('300')

    def test_add_formula_charge(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index'))
        self._wait_for_ajax()
        self.page.wait_for_selector('#transactions table tbody tr')
        initial_count = self.page.locator('#transactions table tbody tr').count()

        self._location(self.live_server_url + reverse('moneybook:add'))
        self.page.fill('#c_day', '17')
        self.page.fill('#c_price', '=1000/4')
        self.page.click('h1:has-text("銀行チャージ") + form input[type="button"]')
        expect(self.page.locator('#result_message')).to_be_visible()

        self._location(self.live_server_url + reverse('moneybook:index'))
        self._wait_for_ajax()
        self.page.wait_for_selector('#transactions table tbody tr')
        rows = self.page.locator('#transactions table tbody tr')
        # チャージも2件追加される
        expect(rows).to_have_count(initial_count + 2)
        tds = rows.nth(1).locator('td')
        expect(tds.nth(2)).to_have_text('250')
