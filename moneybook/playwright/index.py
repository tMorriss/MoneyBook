import re
from datetime import datetime

from django.urls import reverse
from moneybook.playwright.base import PlaywrightBase
from playwright.sync_api import expect


class Index(PlaywrightBase):
    def _assert_initialized_add_mini(self, year, month):
        """入力欄が初期値であることを確認"""
        expect(self.page.locator('#a_year')).to_have_value(str(year))
        expect(self.page.locator('#a_month')).to_have_value(str(month))
        expect(self.page.locator('#a_day')).to_have_value('')
        expect(self.page.locator('#a_item')).to_have_value('')
        expect(self.page.locator('#a_price')).to_have_value('')

        # 支払い方法、分類、立替の最初のラジオボタンがチェックされていること
        expect(self.page.locator('input[name="a_method"]').first).to_be_checked()
        expect(self.page.locator('input[name="a_category"]').first).to_be_checked()
        expect(self.page.locator('input[name="a_temp"]').first).to_be_checked()

    def _assert_add(self, item, method, category):
        now = datetime.now()
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index'))

        expect(self.page.locator('#transactions table tbody tr')).to_have_count(1)

        # 1件追加
        self.page.fill('#a_day', '3')
        self.page.fill('#a_item', item)
        self.page.fill('#a_price', '1000')

        self.page.locator(f'label:has-text("{method}")').first.click()
        self.page.locator(f'label:has-text("{category}")').first.click()

        self.page.click('input[value="追加"]')

        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(2)
        tds = rows.nth(1).locator('td')
        expect(tds.nth(0)).to_have_text(f'{now.year}/{str(now.month).zfill(2)}/03')
        expect(tds.nth(1)).to_have_text(item)
        expect(tds.nth(2)).to_have_text('1,000')
        expect(tds.nth(3)).to_have_text(method)
        expect(tds.nth(4)).to_have_text(category)

        # 未チェック確認 (背景色)
        expect(rows.nth(1)).to_have_css('background-color', 'rgba(0, 0, 0, 0)')

        # 入力欄が戻っていることを確認
        self._assert_initialized_add_mini(now.year, now.month)

    def _assert_invalid_add(self, year, month, day, item, price):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index'))

        expect(self.page.locator('#transactions table tbody tr')).to_have_count(1)

        # 1件追加
        self.page.fill('#a_year', str(year))
        self.page.fill('#a_month', str(month))
        self.page.fill('#a_day', str(day))
        self.page.fill('#a_item', str(item))
        self.page.fill('#a_price', str(price))

        # 適当なラベルを選択（2番目以降）
        self.page.locator('input[name="a_method"] + label').nth(1).click()
        self.page.locator('input[name="a_category"] + label').nth(1).click()
        self.page.click('input[value="追加"]')

        # 入力欄がそのままであることを確認
        expect(self.page.locator('#a_year')).to_have_value(str(year))
        expect(self.page.locator('#a_month')).to_have_value(str(month))
        expect(self.page.locator('#a_day')).to_have_value(str(day))
        expect(self.page.locator('#a_item')).to_have_value(str(item))
        expect(self.page.locator('#a_price')).to_have_value(str(price))

        # 追加されていないことを確認
        expect(self.page.locator('#transactions table tbody tr')).to_have_count(1)

    def _assert_index_date(self, year, month):
        self._assert_common()

        expect(self.page.locator('#a_year')).to_have_value(str(year))
        expect(self.page.locator('#a_month')).to_have_value(str(month))
        expect(self.page.locator('#a_day')).to_have_value('')

        expect(self.page.locator('#jump_year')).to_have_value(str(year))
        expect(self.page.locator('#jump_month')).to_have_value(str(month))

    def _assert_is_displayed(self, rows, expects):
        # ヘッダ行があるので count は len(expects) + 1
        expect(rows).to_have_count(len(expects) + 1)
        for i, expected_visible in enumerate(expects):
            if expected_visible:
                expect(rows.nth(i + 1)).not_to_have_class(re.compile(r'hidden-row'))
            else:
                expect(rows.nth(i + 1)).to_have_class(re.compile(r'hidden-row'))

    def test_index(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index'))

        # 日付だけ確認
        now = datetime.now()
        self._assert_index_date(now.year, now.month)

        # あとplaceholder
        expect(self.page.locator('#a_day')).to_have_attribute('placeholder', str(now.day))

    def test_index_month(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index_month', kwargs={'year': 2000, 'month': 1}))
        self._assert_common()

        # 追加部分
        self._assert_initialized_add_mini(2000, 1)

        methods = ['銀行', '現金', 'Kyash', 'PayPay']
        expect(self.page.locator('input[name="a_method"] + label')).to_have_text(methods)

        categories = ['食費', '必需品', '交通費', 'その他', '内部移動', '貯金', '計算外', '収入']
        expect(self.page.locator('input[name="a_category"] + label')).to_have_text(categories)

        # フィルタ
        expect(self.page.locator('a[href="' + reverse('moneybook:index_month', kwargs={'year': 1999, 'month': 12}) + '"]')).to_be_visible()
        expect(self.page.locator('a[href="' + reverse('moneybook:index_month', kwargs={'year': 2000, 'month': 2}) + '"]')).to_be_visible()

        expect(self.page.locator('#jump_year')).to_have_value('2000')
        expect(self.page.locator('#jump_month')).to_have_value('1')
        expect(self.page.locator('#filter-item')).to_have_value('')

        expect(self.page.locator('.view-filter input[name="filter-direction[]"] + label')).to_have_text(['収入', '支出'])
        inputs = self.page.locator('.view-filter input[name="filter-direction[]"]')
        for i in range(inputs.count()):
            expect(inputs.nth(i)).to_be_checked()

        expect(self.page.locator('.view-filter input[name="filter-method[]"] + label')) \
            .to_have_text(['銀行', '現金', 'Kyash', 'PayPay', 'nanaco', 'Edy'])
        inputs = self.page.locator('.view-filter input[name="filter-method[]"]')
        for i in range(inputs.count()):
            expect(inputs.nth(i)).to_be_checked()

        expect(self.page.locator('.view-filter input[name="filter-class[]"] + label')) \
            .to_have_text(categories)
        inputs = self.page.locator('.view-filter input[name="filter-class[]"]')
        for i in range(inputs.count()):
            expect(inputs.nth(i)).to_be_checked()

        # 一覧表示
        expected_items = ['立替分2', '立替分1', '水道代', 'ガス代', '電気代', 'PayPayチャージ', 'PayPayチャージ',
                          '貯金', '計算外', 'スーパー', '銀行収入', '現金収入', '必需品2', '必需品1', 'その他1', 'コンビニ', '給与']
        expect(self.page.locator('.data_item')).to_have_text(expected_items)

        # 背景色
        expected_colors = [1, 0, 2, 2, 2, 0, 1, 0, 0, 0, 1, 1, 2, 0, 2, 2, 1]
        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(len(expected_colors) + 1)
        for i, color_type in enumerate(expected_colors):
            c = 'rgba(0, 0, 0, 0)'
            if color_type == 1:
                c = 'rgb(153, 255, 153)'  # #9f9
            elif color_type == 2:
                c = 'rgb(255, 102, 136)'  # #f68
            expect(rows.nth(i + 1)).to_have_css('background-color', c)

        # 残高
        expect(self.page.locator('.tbl-all-balance tr td:nth-child(2)')).to_have_text('46,694円')
        expect(self.page.locator('#statistic-fixed table.tbl-common').first.locator('tr:nth-child(1) th')) \
            .to_have_text(['銀行', '現金', 'Kyash', 'PayPay'])
        expect(self.page.locator('#statistic-fixed table.tbl-common').first.locator('tr:nth-child(2) td')) \
            .to_have_text(['52,424円', '-3,930円', '0円', '-1,800円'])

        # 統計 (amCharts data)
        chart_data = self.page.locator('#chart_container_data ul#chart_data li')
        expected_chart_data = [
            'その他,30',
            '食費,2500',
            '必需品,5390',
            '交通費,0'
        ]
        expect(chart_data).to_have_text(expected_chart_data)

        summary_rows = self.page.locator('#tbl-parameters tr')
        expected_summary = [
            ('収入合計', '32,993'),
            ('支出合計', '7,920'),
            ('収支', '+25,073'),
            ('貯金額', '130'),
            ('生活費', '2,500'),
            ('変動費', '5,390'),
            ('生活費残額', '-1,500'),
            ('変動残額', '25,103'),
            ('全収入', '34,123'),
            ('全支出', '9,550')
        ]
        for i, (title, value) in enumerate(expected_summary):
            expect(summary_rows.nth(i).locator('th')).to_have_text(title)
            expect(summary_rows.nth(i).locator('td')).to_have_text(value)

        expect(self.page.locator('#statistic-fixed table.tbl-common').last.locator('tr:nth-child(1) th')) \
            .to_have_text(['', '銀行', '現金', 'Kyash', 'PayPay'])
        expect(self.page.locator('#statistic-fixed table.tbl-common').last.locator('tr:nth-child(2) td')) \
            .to_have_text(['31,723', '3,000', '0', '400'])
        expect(self.page.locator('#statistic-fixed table.tbl-common').last.locator('tr:nth-child(3) td')) \
            .to_have_text(['3,120', '6,430', '0', '1,000'])

    def test_index_month_out_of_range(self):
        """存在しない日付に飛ぶとtopにリダイレクト"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index_month', kwargs={'year': 2000, 'month': 13}))
        expect(self.page).to_have_url(self.live_server_url + reverse('moneybook:index'))

    def test_add_bank_food(self):
        self._assert_add('テスト1', '銀行', '食費')

    def test_add_cash_necessary(self):
        self._assert_add('テスト', '現金', '必需品')

    def test_add_paypay_other(self):
        self._assert_add('テスト1', 'PayPay', 'その他')

    def test_add_bank_intra(self):
        self._assert_add('テスト1', '銀行', '内部移動')

    def test_add_cash_deposit(self):
        self._assert_add('テスト1', '現金', '貯金')

    def test_add_paypay_out(self):
        self._assert_add('テスト1', 'PayPay', '計算外')

    def test_add_escape(self):
        self._assert_add('テ&ス<>ト', '銀行', '食費')

    def test_add_temp(self):
        now = datetime.now()
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index'))

        expect(self.page.locator('#transactions table tbody tr')).to_have_count(1)

        # 1件追加 (立替=Yes, 食費=支出)
        self.page.fill('#a_day', '5')
        self.page.fill('#a_item', '立替テスト')
        self.page.fill('#a_price', '1500')
        self.page.locator('label:has-text("銀行")').first.click()
        self.page.locator('label:has-text("食費")').first.click()
        self.page.locator('label:has-text("Yes")').first.click()
        self.page.click('input[value="追加"]')

        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(2)
        tds = rows.nth(1).locator('td')
        expect(tds.nth(0)).to_have_text(f'{now.year}/{str(now.month).zfill(2)}/05')
        expect(tds.nth(1)).to_have_text('立替テスト')
        expect(tds.nth(2)).to_have_text('1,500')
        expect(tds.nth(3)).to_have_text('銀行')
        expect(tds.nth(4)).to_have_text('立替')

        # 立替フラグがYesで、方向が収入に逆転していることを確認
        expect(rows.nth(1)).to_have_class(re.compile(r'filter-direction-1'))

    def test_add_temp_income(self):
        """収入カテゴリで立替フラグをYesにすると、方向が支出に逆転することを確認"""
        now = datetime.now()
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index'))

        expect(self.page.locator('#transactions table tbody tr')).to_have_count(1)

        # 1件追加 (立替=Yes, 収入=収入)
        self.page.fill('#a_day', '6')
        self.page.fill('#a_item', '収入立替テスト')
        self.page.fill('#a_price', '2000')
        self.page.locator('label:has-text("銀行")').first.click()
        self.page.locator('label:has-text("収入")').first.click()
        self.page.locator('label:has-text("Yes")').first.click()
        self.page.click('input[value="追加"]')

        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(2)
        tds = rows.nth(1).locator('td')
        expect(tds.nth(0)).to_have_text(f'{now.year}/{str(now.month).zfill(2)}/06')
        expect(tds.nth(1)).to_have_text('収入立替テスト')
        expect(tds.nth(2)).to_have_text('2,000')
        expect(tds.nth(3)).to_have_text('銀行')
        expect(tds.nth(4)).to_have_text('立替')

        # 立替フラグがYesで、収入カテゴリの方向が支出に逆転していることを確認
        expect(rows.nth(1)).to_have_class(re.compile(r'filter-direction-2'))

    def test_add_income_no_temp(self):
        """収入カテゴリで立替フラグをNoのままにすると、方向が収入になることを確認"""
        now = datetime.now()
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index'))

        expect(self.page.locator('#transactions table tbody tr')).to_have_count(1)

        # 1件追加 (立替=No, 収入=収入)
        self.page.fill('#a_day', '7')
        self.page.fill('#a_item', '収入テスト')
        self.page.fill('#a_price', '3000')
        self.page.locator('label:has-text("銀行")').first.click()
        self.page.locator('label:has-text("収入")').first.click()
        # 立替フラグはデフォルトのNoのまま変更しない
        self.page.click('input[value="追加"]')

        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(2)
        tds = rows.nth(1).locator('td')
        expect(tds.nth(0)).to_have_text(f'{now.year}/{str(now.month).zfill(2)}/07')
        expect(tds.nth(1)).to_have_text('収入テスト')
        expect(tds.nth(2)).to_have_text('3,000')
        expect(tds.nth(3)).to_have_text('銀行')
        expect(tds.nth(4)).to_have_text('収入')

        # 立替フラグがNoで、収入カテゴリの方向が収入のままであることを確認
        expect(rows.nth(1)).to_have_class(re.compile(r'filter-direction-1'))

    def test_add_empty_day_today(self):
        now = datetime.now()
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index'))

        self.page.fill('#a_item', 'テスト2')
        self.page.fill('#a_price', '3000')
        self.page.locator('label:has-text("Kyash")').first.click()
        self.page.locator('label:has-text("食費")').first.click()
        self.page.click('input[value="追加"]')

        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(2)
        tds = rows.nth(1).locator('td')
        expect(tds.nth(0)).to_have_text(f'{now.year}/{str(now.month).zfill(2)}/{str(now.day).zfill(2)}')
        expect(tds.nth(1)).to_have_text('テスト2')
        expect(tds.nth(2)).to_have_text('3,000')
        expect(tds.nth(3)).to_have_text('Kyash')
        expect(tds.nth(4)).to_have_text('食費')

    def test_invalid_add_str_year(self):
        now = datetime.now()
        self._assert_invalid_add('a', now.month, now.day, 'テスト1', 100)

    def test_invalid_add_empty_year(self):
        now = datetime.now()
        self._assert_invalid_add('', now.month, now.day, 'テスト1', 100)

    def test_invalid_add_str_month(self):
        now = datetime.now()
        self._assert_invalid_add(now.year, 'a', now.day, 'テスト1', 100)

    def test_invalid_add_empty_month(self):
        now = datetime.now()
        self._assert_invalid_add(now.year, '', now.day, 'テスト1', 100)

    def test_invalid_add_str_day(self):
        now = datetime.now()
        self._assert_invalid_add(now.year, now.month, 'a', 'テスト1', 100)

    def test_invalid_add_empty_day(self):
        self._assert_invalid_add(2000, 1, '', 'テスト1', 100)

    def test_invalid_add_str_price(self):
        now = datetime.now()
        self._assert_invalid_add(now.year, now.month, now.day, 'テスト1', 'a')

    def test_invalid_add_empty_item(self):
        now = datetime.now()
        self._assert_invalid_add(now.year, now.month, now.day, '', 100)

    def test_invalid_add_empty_price(self):
        now = datetime.now()
        self._assert_invalid_add(now.year, now.month, now.day, 'テスト1', '')

    def test_filter_button(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index'))

        self.page.fill('#jump_year', '2000')
        self.page.fill('#jump_month', '1')
        self.page.click('.view-filter tr:nth-child(1) input[type="button"]')
        self._assert_index_date(2000, 1)

    def test_filter_year_enter(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index'))

        self.page.fill('#jump_year', '2000')
        self.page.fill('#jump_month', '1')
        self.page.press('#jump_year', 'Enter')
        self._assert_index_date(2000, 1)

    def test_filter_month_enter(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index'))

        self.page.fill('#jump_year', '2000')
        self.page.fill('#jump_month', '1')
        self.page.press('#jump_month', 'Enter')
        self._assert_index_date(2000, 1)

    def test_filter_jump_last(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index_month', kwargs={'year': 2000, 'month': 1}))
        self.page.click('a[href="' + reverse('moneybook:index_month', kwargs={'year': 1999, 'month': 12}) + '"]')
        self._assert_index_date(1999, 12)

    def test_filter_jump_next(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index_month', kwargs={'year': 2000, 'month': 12}))
        self.page.click('a[href="' + reverse('moneybook:index_month', kwargs={'year': 2001, 'month': 1}) + '"]')
        self._assert_index_date(2001, 1)

    def test_index_filter_inout(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index_month', kwargs={'year': 2000, 'month': 1}))
        is_income = [True, True, False, False, False, False, True, False, False, False, True, True, False, False, False, False, True]

        rows = self.page.locator('#transactions table tbody tr')

        # 収入だけ表示 (デフォルトは両方チェックされているので、支出(pk=2)のラベルをクリックして外す)
        # label for filter-direction-2
        self.page.click('label[for="filter-direction-2"]')
        self._assert_is_displayed(rows, is_income)

        # どちらも非表示 (収入(pk=1)のラベルもクリックして外す)
        self.page.click('label[for="filter-direction-1"]')
        self._assert_is_displayed(rows, [False] * 17)

        # 支出だけ表示 (支出(pk=2)のラベルをクリックして付ける)
        self.page.click('label[for="filter-direction-2"]')
        self._assert_is_displayed(rows, [not i for i in is_income])

    def test_index_filter_method_none(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index_month', kwargs={'year': 2000, 'month': 1}))

        # 全部非表示
        labels = self.page.locator('.view-filter input[name="filter-method[]"] + label')
        for i in range(labels.count()):
            labels.nth(i).click()

        rows = self.page.locator('#transactions table tbody tr')
        self._assert_is_displayed(rows, [False] * 17)

    def test_index_filter_bank(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index_month', kwargs={'year': 2000, 'month': 1}))

        # 銀行のみ表示 (銀行(pk=1)以外をすべてクリックして外す)
        labels = self.page.locator('.view-filter input[name="filter-method[]"] + label')
        # 0番目が銀行なので、1番目以降をクリック
        for i in range(1, labels.count()):
            labels.nth(i).click()

        expects = [True, False, True, True, True, False, True, True, True, False, True, False, False, True, False, False, True]
        rows = self.page.locator('#transactions table tbody tr')
        self._assert_is_displayed(rows, expects)

    def test_index_filter_bank_paypay(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index_month', kwargs={'year': 2000, 'month': 1}))

        # 銀行(pk=1)とPayPay(pk=3)以外をすべて外す
        labels = self.page.locator('.view-filter input[name="filter-method[]"] + label')
        # インデックス: 0:銀行, 1:現金, 2:Kyash, 3:PayPay, 4:nanaco, 5:Edy
        labels.nth(1).click()  # 現金
        labels.nth(2).click()  # Kyash
        labels.nth(4).click()  # nanaco
        labels.nth(5).click()  # Edy

        expects = [True, True, True, True, True, True, True, True, True, False, True, False, False, True, False, False, True]
        rows = self.page.locator('#transactions table tbody tr')
        self._assert_is_displayed(rows, expects)

    def test_index_filter_category_none(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index_month', kwargs={'year': 2000, 'month': 1}))

        # 全部非表示
        labels = self.page.locator('.view-filter input[name="filter-class[]"] + label')
        for i in range(labels.count()):
            labels.nth(i).click()

        rows = self.page.locator('#transactions table tbody tr')
        self._assert_is_displayed(rows, [False] * 17)

    def test_index_filter_category_food(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index_month', kwargs={'year': 2000, 'month': 1}))

        # 食費(pk=1)のみ表示
        labels = self.page.locator('.view-filter input[name="filter-class[]"] + label')
        for i in range(1, labels.count()):
            labels.nth(i).click()

        expects = [False, True, False, False, False, False, False, False, False, True, False, False, False, False, False, True, False]
        rows = self.page.locator('#transactions table tbody tr')
        self._assert_is_displayed(rows, expects)

    def test_index_filter_category_food_necessary(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index_month', kwargs={'year': 2000, 'month': 1}))

        # 食費(pk=1)と必需品(pk=2)
        labels = self.page.locator('.view-filter input[name="filter-class[]"] + label')
        for i in range(2, labels.count()):
            labels.nth(i).click()

        expects = [True, True, True, True, True, False, False, False, False, True, True, True, True, True, False, True, False]
        rows = self.page.locator('#transactions table tbody tr')
        self._assert_is_displayed(rows, expects)

    def test_index_filter_category_food_necessary_intra(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index_month', kwargs={'year': 2000, 'month': 1}))

        # 食費(pk=1)と必需品(pk=2)と内部移動(pk=4)
        labels = self.page.locator('.view-filter input[name="filter-class[]"] + label')
        # 0:食費, 1:必需品, 2:交通費, 3:その他, 4:内部移動, 5:貯金, 6:計算外, 7:収入
        labels.nth(2).click()  # 交通費
        labels.nth(3).click()  # その他
        labels.nth(5).click()  # 貯金
        labels.nth(6).click()  # 計算外
        labels.nth(7).click()  # 収入

        expects = [True, True, True, True, True, True, True, False, False, True, True, True, True, True, False, True, False]
        rows = self.page.locator('#transactions table tbody tr')
        self._assert_is_displayed(rows, expects)

    def test_index_filter_all(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index_month', kwargs={'year': 2000, 'month': 1}))

        # 全解除
        self.page.click('.view-filter input[value="全解除"]')
        rows = self.page.locator('#transactions table tbody tr')
        self._assert_is_displayed(rows, [False] * 17)

        # 全選択
        self.page.click('.view-filter input[value="全選択"]')
        self._assert_is_displayed(rows, [True] * 17)

    def test_move_edit(self):
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index_month', kwargs={'year': 2000, 'month': 1}))
        self.page.click('#transactions table tbody tr:nth-child(2) td:nth-child(6) a')

        expect(self.page).to_have_url(self.live_server_url + reverse('moneybook:edit', kwargs={'pk': 18}))

    def test_add_formula_mini_addition(self):
        """金額入力欄に足し算の数式を入力できることを確認（_add_mini）"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index'))

        # 初期状態: 1件のみ
        expect(self.page.locator('#transactions table tbody tr')).to_have_count(1)

        # 簡単な足し算 =100+200 → 300
        self.page.fill('#a_day', '10')
        self.page.fill('#a_item', '数式テスト')
        self.page.fill('#a_price', '=100+200')
        self.page.click('input[value="追加"]')

        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(2)
        tds = rows.nth(1).locator('td')
        expect(tds.nth(1)).to_have_text('数式テスト')
        expect(tds.nth(2)).to_have_text('300')

    def test_add_formula_mini_multiplication_with_parentheses(self):
        """金額入力欄に掛け算と括弧の数式を入力できることを確認（_add_mini）"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index'))

        # 初期状態: 1件のみ
        expect(self.page.locator('#transactions table tbody tr')).to_have_count(1)

        # 掛け算と括弧 =(100+200)*3 → 900
        self.page.fill('#a_day', '11')
        self.page.fill('#a_item', '数式テスト')
        self.page.fill('#a_price', '=(100+200)*3')
        self.page.click('input[value="追加"]')

        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(2)
        tds = rows.nth(1).locator('td')
        expect(tds.nth(1)).to_have_text('数式テスト')
        expect(tds.nth(2)).to_have_text('900')

    def test_add_formula_mini_division(self):
        """金額入力欄に割り算の数式を入力できることを確認（_add_mini）"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index'))

        # 初期状態: 1件のみ
        expect(self.page.locator('#transactions table tbody tr')).to_have_count(1)

        # 割り算 =1000/4 → 250
        self.page.fill('#a_day', '12')
        self.page.fill('#a_item', '数式テスト')
        self.page.fill('#a_price', '=1000/4')
        self.page.click('input[value="追加"]')

        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(2)
        tds = rows.nth(1).locator('td')
        expect(tds.nth(1)).to_have_text('数式テスト')
        expect(tds.nth(2)).to_have_text('250')

    def test_add_formula_mini_with_commas(self):
        """金額入力欄にカンマ付き数値の数式を入力できることを確認（_add_mini）"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index'))

        # 初期状態: 1件のみ
        expect(self.page.locator('#transactions table tbody tr')).to_have_count(1)

        # カンマ付き数値 =1,000+2,000 → 3000
        self.page.fill('#a_day', '13')
        self.page.fill('#a_item', '数式テスト')
        self.page.fill('#a_price', '=1,000+2,000')
        self.page.click('input[value="追加"]')

        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(2)
        tds = rows.nth(1).locator('td')
        expect(tds.nth(1)).to_have_text('数式テスト')
        expect(tds.nth(2)).to_have_text('3,000')

    def test_summary_table(self):
        """フィルタの下のサマリーテーブルが正しく表示・更新されることを確認"""
        self._login()
        now = datetime.now()
        self._location(self.live_server_url + reverse('moneybook:index_month', kwargs={'year': now.year, 'month': now.month}))

        # 初期状態
        expect(self.page.locator('#summary-count')).to_have_text('0件')
        expect(self.page.locator('#summary-income')).to_have_text('収入: 0円')
        expect(self.page.locator('#summary-outgo')).to_have_text('支出: 0円')

        # 収入データ追加
        self.page.fill('#a_day', '1')
        self.page.fill('#a_item', 'Test Income')
        self.page.fill('#a_price', '1000')
        # 収入カテゴリ (pk=7)
        self.page.click('#lbl_a_category-7')
        self.page.click('input[value="追加"]')

        # 支出データ追加
        self.page.fill('#a_day', '2')
        self.page.fill('#a_item', 'Test Outgo')
        self.page.fill('#a_price', '500')
        # 食費カテゴリ (pk=1)
        self.page.click('#lbl_a_category-1')
        self.page.click('input[value="追加"]')

        # サマリー確認
        expect(self.page.locator('#summary-count')).to_have_text('2件')
        expect(self.page.locator('#summary-income')).to_have_text('収入: 1,000円')
        expect(self.page.locator('#summary-outgo')).to_have_text('支出: 500円')

        # フィルタリング (Outgoのみ)
        self.page.fill('#filter-item', 'Outgo')
        expect(self.page.locator('#summary-count')).to_have_text('1件')
        expect(self.page.locator('#summary-income')).to_have_text('収入: 0円')
        expect(self.page.locator('#summary-outgo')).to_have_text('支出: 500円')

        # フィルタリング解除
        self.page.fill('#filter-item', '')
        expect(self.page.locator('#summary-count')).to_have_text('2件')
