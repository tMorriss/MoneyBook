from datetime import datetime

from django.urls import reverse
from moneybook.playwright.base import PlaywrightBase
from playwright.sync_api import expect


class PeriodBalances(PlaywrightBase):
    def test_period_balances_display_and_url_params(self):
        """期間残高画面の初期表示、デフォルト期間、およびURLパラメータの検証"""
        self._login()
        now = datetime.now()

        # 初期表示の確認
        self._location(self.live_server_url + reverse('moneybook:period_balances'))
        self._assert_common()

        # フォームの存在確認
        expect(self.page.locator('#start_year')).to_be_visible()
        expect(self.page.locator('#start_month')).to_be_visible()
        expect(self.page.locator('#end_year')).to_be_visible()
        expect(self.page.locator('#end_month')).to_be_visible()

        # デフォルト値の確認 (去年1月〜今月)
        expect(self.page.locator('#start_year')).to_have_value(str(now.year - 1))
        expect(self.page.locator('#start_month')).to_have_value('1')
        expect(self.page.locator('#end_year')).to_have_value(str(now.year))
        expect(self.page.locator('#end_month')).to_have_value(str(now.month))

        # URLパラメータによる指定
        url_with_params = (
            f"{self.live_server_url}{reverse('moneybook:period_balances')}"
            f"?start_year={now.year}&start_month=2&end_year={now.year}&end_month={now.month}"
        )
        self._location(url_with_params)

        expect(self.page.locator('#start_year')).to_have_value(str(now.year))
        expect(self.page.locator('#start_month')).to_have_value('2')
        expect(self.page.locator('#end_year')).to_have_value(str(now.year))
        expect(self.page.locator('#end_month')).to_have_value(str(now.month))

    def test_update_functionality(self):
        """更新ボタンおよびEnterキーによる表示更新、入力保持の検証"""
        self._login()
        now = datetime.now()

        self._location(self.live_server_url + reverse('moneybook:period_balances'))

        # 1. 更新ボタンをクリック
        self.page.click('input[value="更新"]')
        # グラフが表示されることを確認
        expect(self.page.locator('#lineplot_monthly_balance')).to_be_visible()

        # 2. 期間を変更してEnterキー (年入力欄)
        start_year_input = self.page.locator('#start_year')
        start_year_input.fill(str(now.year))
        start_year_input.dispatch_event('keypress', {'keyCode': 13})

        expect(self.page.locator('#lineplot_monthly_balance')).to_be_visible()
        expect(self.page.locator('#start_year')).to_have_value(str(now.year))

        # 3. 期間を変更してEnterキー (月入力欄)
        start_month_input = self.page.locator('#start_month')
        start_month_input.fill('3')
        start_month_input.dispatch_event('keypress', {'keyCode': 13})

        expect(self.page.locator('#lineplot_monthly_balance')).to_be_visible()
        expect(self.page.locator('#start_month')).to_have_value('3')

    def test_graph_with_various_periods_and_data(self):
        """データがある状態での表示、および様々な期間指定の検証"""
        self._login()
        now = datetime.now()

        # テストデータを追加 (インデックスページから)
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.page.fill('#a_day', '10')
        self.page.fill('#a_item', '期間残高テスト')
        self.page.fill('#a_price', '5000')
        # インデックスページの追加ボタンは input[value="追加"]
        self.page.click('input[value="追加"]')

        # 期間残高画面に移動
        self._location(self.live_server_url + reverse('moneybook:period_balances'))

        # 1. データがある状態での表示確認
        self.page.click('input[value="更新"]')
        expect(self.page.locator('#lineplot_monthly_balance')).to_be_visible()
        # グラフデータ用の隠しリストが空でないことを確認 (サクッとできる範囲の検証)
        expect(self.page.locator('#monthly_balance li')).not_to_have_count(0)

        # 2. 1ヶ月だけの期間を指定
        self.page.fill('#start_year', str(now.year))
        self.page.fill('#start_month', str(now.month))
        self.page.fill('#end_year', str(now.year))
        self.page.fill('#end_month', str(now.month))
        self.page.click('input[value="更新"]')

        expect(self.page.locator('#lineplot_monthly_balance')).to_be_visible()
        # 1ヶ月分なので、リストの項目は1つのはず
        expect(self.page.locator('#monthly_balance li')).to_have_count(1)

        # 3. 複数年にまたがる期間を指定
        self.page.fill('#start_year', str(now.year - 2))
        self.page.fill('#start_month', '1')
        self.page.click('input[value="更新"]')

        expect(self.page.locator('#lineplot_monthly_balance')).to_be_visible()
        # 項目が複数あることを確認
        # (now.year - (now.year - 2)) * 12 + now.month = 2 * 12 + now.month
        expected_count = 2 * 12 + now.month
        expect(self.page.locator('#monthly_balance li')).to_have_count(expected_count)
