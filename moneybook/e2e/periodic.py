from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.urls import reverse
from moneybook.e2e.base import PlaywrightBase
from playwright.sync_api import expect


class Periodic(PlaywrightBase):
    def _add_periodic_data_via_ui(self, day, item, price):
        """UI操作で定期取引を追加するヘルパーメソッド"""
        self._location(self.live_server_url + reverse('moneybook:periodic_edit'))
        self.page.click('#btn_add_row')
        # 新しく追加された行（index 0）に入力
        self.page.fill('input[name^="day_new_0"]', str(day))
        self.page.fill('input[name^="item_new_0"]', item)
        self.page.fill('input[name^="price_new_0"]', str(price))
        self.page.click('button[type="submit"]')
        expect(self.page).to_have_url(self.live_server_url + reverse('moneybook:periodic'))

    def test_periodic_navigation_and_access(self):
        """定期取引ページへの遷移と表示の確認"""
        self._login()

        # タスクバーからツールページへ
        self._location(self.live_server_url + reverse('moneybook:tools'))
        # 定期取引リンクをクリック
        self.page.click('text=定期取引')
        expect(self.page).to_have_url(self.live_server_url + reverse('moneybook:periodic'))

        # ページタイトル確認
        expect(self.page.locator('section h1')).to_have_text('定期取引一覧')

        # ボタンの存在確認
        expect(self.page.locator('input#btn_add_bulk[value="追加"]')).to_be_visible()
        expect(self.page.locator('input[value="編集"]')).to_be_visible()

        # 年月入力欄とplaceholderの検証
        year_input = self.page.locator('#target_year')
        month_input = self.page.locator('#target_month')
        next_month = datetime.now() + relativedelta(months=1)
        expect(year_input).to_have_attribute('placeholder', str(next_month.year))
        expect(month_input).to_have_attribute('placeholder', str(next_month.month))

    def test_periodic_add_and_bulk_register(self):
        """定期取引の追加、表示、および一括登録の確認"""
        self._login()
        item_name = '一括登録テストアイテム'
        self._add_periodic_data_via_ui(10, item_name, 5000)

        # 一覧に表示されていること
        expect(self.page.locator('#periodic_table')).to_contain_text(item_name)

        # 一括登録実行 (2024年5月)
        self.page.fill('#target_year', '2024')
        self.page.fill('#target_month', '5')
        self.page.click('#btn_add_bulk')
        expect(self.page.locator('#result_message')).to_contain_text('Success!')

        # インデックスページで登録されたことを確認
        self._location(self.live_server_url + reverse('moneybook:index_month', kwargs={'year': 2024, 'month': 5}))
        self.page.wait_for_selector('#transactions table')
        expect(self.page.locator('#transactions')).to_contain_text(item_name)

    def test_periodic_edit(self):
        """定期取引の編集ができること"""
        self._login()
        original_item = '編集前アイテム'
        updated_item = '編集後アイテム'
        self._add_periodic_data_via_ui(1, original_item, 1000)

        # 編集ページへ
        self.page.click('input[value="編集"]')
        # 編集対象の行を探して値を書き換え
        self.page.fill('input[name^="item_"]:not([name*="new"])', updated_item)
        self.page.click('button[type="submit"]')

        expect(self.page).to_have_url(self.live_server_url + reverse('moneybook:periodic'))
        expect(self.page.locator('#periodic_table')).to_contain_text(updated_item)
        expect(self.page.locator('#periodic_table')).not_to_contain_text(original_item)

    def test_periodic_delete(self):
        """定期取引の削除ができること"""
        self._login()
        item_name = '削除テストアイテム'
        self._add_periodic_data_via_ui(1, item_name, 1000)

        # 編集ページへ
        self.page.click('input[value="編集"]')
        # 削除ボタンをクリック
        self.page.click('button.btn-delete-row')
        # DOMから消えたことを確認
        expect(self.page.locator(f'input[value="{item_name}"]')).to_have_count(0)
        self.page.click('button[type="submit"]')

        expect(self.page).to_have_url(self.live_server_url + reverse('moneybook:periodic'))
        expect(self.page.locator('#periodic_table')).not_to_contain_text(item_name)

    def test_periodic_cancel(self):
        """編集をキャンセルすると保存されないこと"""
        self._login()
        item_name = 'キャンセルテストアイテム'
        self._add_periodic_data_via_ui(1, item_name, 1000)

        # 編集ページへ
        self.page.click('input[value="編集"]')
        self.page.fill('input[name^="item_"]:not([name*="new"])', '書き換えテキスト')
        self.page.click('text=キャンセル')

        expect(self.page).to_have_url(self.live_server_url + reverse('moneybook:periodic'))
        expect(self.page.locator('#periodic_table')).to_contain_text(item_name)
        expect(self.page.locator('#periodic_table')).not_to_contain_text('書き換えテキスト')
