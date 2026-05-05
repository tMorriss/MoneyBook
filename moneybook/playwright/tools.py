from django.urls import reverse
from moneybook.playwright.base import PlaywrightBase
from playwright.sync_api import expect


class Tools(PlaywrightBase):
    def test_get(self):
        """ツール画面が正しく表示されることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:tools'))

        self._assert_common()

    def test_sections_display(self):
        """各セクションが表示されることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:tools'))

        # 実際の現金残高
        expect(self.page.locator('#actual_balance')).to_be_visible()
        # チェック日の表
        expect(self.page.locator('#checked-date')).to_be_visible()
        # チェック日の入力フィールド
        expect(self.page.locator('#check_year')).to_be_visible()
        expect(self.page.locator('#check_month')).to_be_visible()
        expect(self.page.locator('#check_day')).to_be_visible()
        # 生活費目標額
        expect(self.page.locator('#txt_living_cost')).to_be_visible()

    def test_update_actual_cash(self):
        """実際の現金残高を更新できることを確認 (ボタンクリック)"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:tools'))

        # 実際の現金残高を入力
        actual_cash_input = self.page.locator('#actual_balance')
        actual_cash_input.click()  # focus to unseparate
        actual_cash_input.fill('5000')

        # 計算ボタンをクリック (value="計算")
        self.page.click('input[value="計算"]')

        # 差額が更新されるのを待つ (内部的には $.post 完了後に更新される)
        # 入力欄がカンマ区切りになるのを待つことでAJAX完了を確認
        expect(actual_cash_input).to_have_value('5,000')

        # ページをリロードして値が保持されていることを確認
        self.page.reload()
        expect(self.page.locator('#actual_balance')).to_have_value('5,000')

    def test_update_actual_cash_enter(self):
        """Enterキーで実際の現金残高を更新できることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:tools'))

        # 実際の現金残高を入力してEnter
        actual_cash_input = self.page.locator('#actual_balance')
        actual_cash_input.focus()
        actual_cash_input.fill('10000')
        actual_cash_input.dispatch_event('keypress', {'keyCode': 13})

        # AJAX完了を待つ (updateDiff完了後にseparateValueが呼ばれる)
        expect(actual_cash_input).to_have_value('10,000', timeout=10000)

        self.page.reload()
        expect(self.page.locator('#actual_balance')).to_have_value('10,000')

    def test_update_living_cost_mark(self):
        """生活費目標額を更新できることを確認 (ボタンクリック)"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:tools'))

        # 生活費目標額を入力
        living_cost_input = self.page.locator('#txt_living_cost')
        living_cost_input.click()
        living_cost_input.fill('30000')

        # 更新ボタンをクリック
        # updateLivingCostMark は location.reload() を呼ぶ
        self.page.locator('h1:has-text("生活費目標額") + table').locator('input[value="更新"]').click()

        # 値が保持されていることを確認 (リロードされるので Playwright が解決し直す)
        expect(self.page.locator('#txt_living_cost')).to_have_value('30,000', timeout=10000)

    def test_update_living_cost_mark_enter(self):
        """Enterキーで生活費目標額を更新できることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:tools'))

        # 生活費目標額を入力してEnter
        living_cost_input = self.page.locator('#txt_living_cost')
        living_cost_input.focus()
        living_cost_input.fill('40000')
        living_cost_input.dispatch_event('keypress', {'keyCode': 13})

        # 値が保持されていることを確認
        expect(self.page.locator('#txt_living_cost')).to_have_value('40,000', timeout=10000)

    def test_link_from_taskbar(self):
        """タスクバーからツール画面に遷移できることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:index'))

        # タスクバーのツールリンクをクリック
        # base.py の _assert_common でも確認しているが、実際にクリックして遷移することを確認
        self.page.locator('nav.task_bar').get_by_role('link', name='ツール').click()

        # ツール画面に遷移したことを確認
        expect(self.page).to_have_url(self.live_server_url + reverse('moneybook:tools'))

    def test_multiple_updates(self):
        """複数の値を連続して更新できることを確認"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:tools'))

        # 実際の現金残高を更新
        actual_balance = self.page.locator('#actual_balance')
        actual_balance.click()
        actual_balance.fill('15000')
        self.page.click('input[value="計算"]')
        # カンマ区切りになるのを待つことでAJAX完了を確認
        expect(actual_balance).to_have_value('15,000', timeout=10000)

        # 生活費目標額を更新
        living_cost = self.page.locator('#txt_living_cost')
        living_cost.click()
        living_cost.fill('50000')
        update_button = self.page.locator('h1:has-text("生活費目標額") + table').locator('input[value="更新"]')
        update_button.click()

        # ページをリロードして両方の値が保持されていることを確認
        expect(self.page.locator('#actual_balance')).to_have_value('15,000', timeout=10000)
        expect(self.page.locator('#txt_living_cost')).to_have_value('50,000', timeout=10000)
