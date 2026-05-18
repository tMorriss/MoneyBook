import re
from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.urls import reverse
from moneybook.e2e.base import PlaywrightBase
from playwright.sync_api import expect


class LivingCostMarkTest(PlaywrightBase):
    def test_living_cost_mark_basic_flow(self):
        self._login()

        # 1. living_cost_mark画面が表示できる
        self.page.goto(self.live_server_url + reverse('moneybook:living_cost_mark'))
        expect(self.page.locator('section h1')).to_contain_text('生活費目標')

        # 2. 編集ボタンからliving_cost_mark_edit画面に遷移できる
        self.page.click('#btn_edit')
        expect(self.page.locator('section h1')).to_contain_text('生活費目標編集')

        # 既存データを削除
        while self.page.locator('.btn-delete-row:visible').count() > 0:
            self.page.locator('.btn-delete-row:visible').first.click()

        # 3. 行追加ができる。追加するデータは3つ
        # データ1: 開始日がnull、終了日設定 (今月の前月)
        now = datetime.now()
        last_month = now - relativedelta(months=1)

        self.page.click('#btn_add_row')
        # 最初の一行目
        row1 = self.page.locator('#mark_table_body tr').last
        row1.locator('input[name^="end_year_"]').fill(str(last_month.year))
        row1.locator('input[name^="end_month_"]').fill(str(last_month.month))
        row1.locator('input[name^="price_"]').fill('100000')

        # データ2: 開始日が↑の次月 (今月) & 終了日設定 (今月)
        this_month = now
        self.page.click('#btn_add_row')
        row2 = self.page.locator('#mark_table_body tr').last
        row2.locator('input[name^="start_year_"]').fill(str(this_month.year))
        row2.locator('input[name^="start_month_"]').fill(str(this_month.month))
        row2.locator('input[name^="end_year_"]').fill(str(this_month.year))
        row2.locator('input[name^="end_month_"]').fill(str(this_month.month))
        row2.locator('input[name^="price_"]').fill('110000')

        # データ3: 開始日が↑の次月 (来月) & 終了日未設定
        next_month = now + relativedelta(months=1)
        self.page.click('#btn_add_row')
        row3 = self.page.locator('#mark_table_body tr').last
        row3.locator('input[name^="start_year_"]').fill(str(next_month.year))
        row3.locator('input[name^="start_month_"]').fill(str(next_month.month))
        row3.locator('input[name^="price_"]').fill('120000')

        # 更新
        self.page.click('button:has-text("更新")')
        expect(self.page).to_have_url(re.compile(reverse('moneybook:living_cost_mark') + '$'))

        # 4. living_cost_mark画面上で上記の3データが反映されていることを確認 (priceだけでなく開始日、終了日も確認)
        rows = self.page.locator('table.tbl-data tbody tr')
        expect(rows).to_have_count(3)

        # Row 1: Start null, End last_month, Price 100,000
        expect(rows.nth(0).locator('td').nth(0)).to_have_text('')
        expect(rows.nth(0).locator('td').nth(1)).to_have_text(last_month.strftime('%Y年%-m月'))
        expect(rows.nth(0).locator('td').nth(2)).to_have_text('100,000')

        # Row 2: Start this_month, End this_month, Price 110,000
        expect(rows.nth(1).locator('td').nth(0)).to_have_text(this_month.strftime('%Y年%-m月'))
        expect(rows.nth(1).locator('td').nth(1)).to_have_text(this_month.strftime('%Y年%-m月'))
        expect(rows.nth(1).locator('td').nth(2)).to_have_text('110,000')

        # Row 3: Start next_month, End null, Price 120,000
        expect(rows.nth(2).locator('td').nth(0)).to_have_text(next_month.strftime('%Y年%-m月'))
        expect(rows.nth(2).locator('td').nth(1)).to_have_text('')
        expect(rows.nth(2).locator('td').nth(2)).to_have_text('120,000')

        # 5. 上記で追加した月のindex画面に遷移し、index画面上で設定値が反映されていることを確認
        # 今月の前月
        self.page.goto(self.live_server_url + reverse('moneybook:index_month', kwargs={'year': last_month.year, 'month': last_month.month}))
        self._wait_for_ajax()
        # 統計パネルが出るまで待つ
        self.page.wait_for_selector('#tbl-parameters')
        expect(self.page.locator('#tbl-parameters tr').filter(has_text='生活費目標額').locator('td')).to_have_text('100,000')

        # 今月
        self.page.goto(self.live_server_url + reverse('moneybook:index_month', kwargs={'year': this_month.year, 'month': this_month.month}))
        self._wait_for_ajax()
        self.page.wait_for_selector('#tbl-parameters')
        expect(self.page.locator('#tbl-parameters tr').filter(has_text='生活費目標額').locator('td')).to_have_text('110,000')

        # 来月
        self.page.goto(self.live_server_url + reverse('moneybook:index_month', kwargs={'year': next_month.year, 'month': next_month.month}))
        self._wait_for_ajax()
        self.page.wait_for_selector('#tbl-parameters')
        expect(self.page.locator('#tbl-parameters tr').filter(has_text='生活費目標額').locator('td')).to_have_text('120,000')

    def test_living_cost_mark_delete_and_add_single(self):
        self._login()
        # 再度edit画面に遷移し、既存のデータを削除し別のデータを追加。
        self.page.goto(self.live_server_url + reverse('moneybook:living_cost_mark_edit'))
        while self.page.locator('.btn-delete-row:visible').count() > 0:
            self.page.locator('.btn-delete-row:visible').first.click()

        self.page.click('#btn_add_row')
        row_new = self.page.locator('#mark_table_body tr').last
        row_new.locator('input[name^="price_"]').fill('200000')  # Start null, End null
        self.page.click('button:has-text("更新")')

        expect(self.page.locator('td:has-text("200,000")')).to_be_visible()
        expect(self.page.locator('table.tbl-data tbody tr')).to_have_count(1)

    def test_living_cost_mark_sort_order(self):
        self._login()
        now = datetime.now()
        this_month = now
        next_month = now + relativedelta(months=1)

        # 再度edit画面に遷移し、時系列が逆順でデータを追加
        self.page.goto(self.live_server_url + reverse('moneybook:living_cost_mark_edit'))
        while self.page.locator('.btn-delete-row:visible').count() > 0:
            self.page.locator('.btn-delete-row:visible').first.click()

        # 来月を先に追加
        self.page.click('#btn_add_row')
        row_next = self.page.locator('#mark_table_body tr').last
        row_next.locator('input[name^="start_year_"]').fill(str(next_month.year))
        row_next.locator('input[name^="start_month_"]').fill(str(next_month.month))
        row_next.locator('input[name^="price_"]').fill('120000')

        # 今月を後に追加
        self.page.click('#btn_add_row')
        row_this = self.page.locator('#mark_table_body tr').last
        row_this.locator('input[name^="start_year_"]').fill(str(this_month.year))
        row_this.locator('input[name^="start_month_"]').fill(str(this_month.month))

        row_this.locator('input[name^="end_year_"]').fill(str(this_month.year))
        row_this.locator('input[name^="end_month_"]').fill(str(this_month.month))
        row_this.locator('input[name^="price_"]').fill('110000')

        self.page.click('button:has-text("更新")')

        # living_cost_mark画面に遷移すると時系列順にソートされている
        rows = self.page.locator('table.tbl-data tbody tr')
        expect(rows.nth(0)).to_contain_text('110,000')
        expect(rows.nth(1)).to_contain_text('120,000')

    def test_error_multiple_null_start_date(self):
        self._login()
        self.page.goto(self.live_server_url + reverse('moneybook:living_cost_mark_edit'))

        while self.page.locator('.btn-delete-row:visible').count() > 0:
            self.page.locator('.btn-delete-row:visible').first.click()

        self.page.click('#btn_add_row')
        self.page.locator('#mark_table_body tr').last.locator('input[name^="price_"]').fill('100')
        self.page.click('#btn_add_row')
        self.page.locator('#mark_table_body tr').last.locator('input[name^="price_"]').fill('200')

        self.page.click('button:has-text("更新")')
        expect(self.page.locator('p[style="color: red;"]')).to_contain_text('開始年月が空のデータは1行だけ指定できます')

    def test_error_partial_input(self):
        self._login()
        self.page.goto(self.live_server_url + reverse('moneybook:living_cost_mark_edit'))

        while self.page.locator('.btn-delete-row:visible').count() > 0:
            self.page.locator('.btn-delete-row:visible').first.click()

        self.page.click('#btn_add_row')
        row = self.page.locator('#mark_table_body tr').first
        row.locator('input[name^="start_year_"]').fill('2024')
        row.locator('input[name^="start_month_"]').clear()
        row.locator('input[name^="price_"]').fill('10000')

        self.page.click('button:has-text("更新")')
        expect(self.page.locator('p[style="color: red;"]')).to_contain_text('開始年月の入力が不完全です')

    def test_error_overlap_gaps(self):
        self._login()
        self.page.goto(self.live_server_url + reverse('moneybook:living_cost_mark_edit'))

        while self.page.locator('.btn-delete-row:visible').count() > 0:
            self.page.locator('.btn-delete-row:visible').first.click()

        self.page.click('#btn_add_row')
        r1 = self.page.locator('#mark_table_body tr').last
        r1.locator('input[name^="start_year_"]').fill('2024')
        r1.locator('input[name^="start_month_"]').fill('1')
        r1.locator('input[name^="end_year_"]').fill('2024')
        r1.locator('input[name^="end_month_"]').fill('3')
        r1.locator('input[name^="price_"]').fill('100')

        self.page.click('#btn_add_row')
        r2 = self.page.locator('#mark_table_body tr').last
        r2.locator('input[name^="start_year_"]').fill('2024')
        r2.locator('input[name^="start_month_"]').fill('5')  # Gap in April
        r2.locator('input[name^="price_"]').fill('200')

        self.page.click('button:has-text("更新")')
        expect(self.page.locator('p[style="color: red;"]')).to_contain_text('期間に隙間または重複があります')

    def test_error_missing_intermediate_end_date(self):
        self._login()
        self.page.goto(self.live_server_url + reverse('moneybook:living_cost_mark_edit'))

        while self.page.locator('.btn-delete-row:visible').count() > 0:
            self.page.locator('.btn-delete-row:visible').first.click()

        self.page.click('#btn_add_row')
        r1 = self.page.locator('#mark_table_body tr').last
        r1.locator('input[name^="price_"]').fill('100')  # Start null, End null

        self.page.click('#btn_add_row')
        r2 = self.page.locator('#mark_table_body tr').last
        r2.locator('input[name^="start_year_"]').fill('2024')
        r2.locator('input[name^="start_month_"]').fill('1')
        r2.locator('input[name^="price_"]').fill('200')

        self.page.click('button:has-text("更新")')
        expect(self.page.locator('p[style="color: red;"]')).to_contain_text('途中のデータの終了年月は必須です')

    def test_error_multiple_null_end_date(self):
        self._login()
        self.page.goto(self.live_server_url + reverse('moneybook:living_cost_mark_edit'))

        while self.page.locator('.btn-delete-row:visible').count() > 0:
            self.page.locator('.btn-delete-row:visible').first.click()

        self.page.click('#btn_add_row')
        r1 = self.page.locator('#mark_table_body tr').last
        r1.locator('input[name^="start_year_"]').fill('2024')
        r1.locator('input[name^="start_month_"]').fill('1')
        r1.locator('input[name^="price_"]').fill('100')  # Start 2024/01, End null

        self.page.click('#btn_add_row')
        r2 = self.page.locator('#mark_table_body tr').last
        r2.locator('input[name^="start_year_"]').fill('2024')
        r2.locator('input[name^="start_month_"]').fill('5')
        r2.locator('input[name^="price_"]').fill('200')  # Start 2024/05, End null

        self.page.click('button:has-text("更新")')
        # This will trigger either '途中のデータの終了年月は必須です' or '期間に隙間または重複があります'
        # depending on sort order and which one is checked first.
        # Marks are sorted by start_date.
        # r1 (2024-01) comes before r2 (2024-05).
        # r1.end_date is None, and it is not the last one in the list.
        # So '途中のデータの終了年月は必須です' should be returned.
        expect(self.page.locator('p[style="color: red;"]')).to_contain_text('途中のデータの終了年月は必須です')
