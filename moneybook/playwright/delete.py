import re

from django.urls import reverse
from moneybook.playwright.base import PlaywrightBase
from playwright.sync_api import expect


class Delete(PlaywrightBase):
    def test_delete_from_edit_page(self):
        """編集画面から削除できることを確認"""
        self._login()
        # データを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.page.wait_for_selector('#transactions table')

        self.page.fill('#a_day', '10')
        self.page.fill('#a_item', '削除テスト')
        self.page.fill('#a_price', '1000')
        self.page.click('input[value="追加"]')

        # データが追加されたことを確認
        rows = self.page.locator('#transactions table tbody tr')
        # ヘッダー + 1件。
        expect(rows).to_have_count(2, timeout=10000)

        # 編集画面に移動 (2行目の 6列目)
        self.page.click('#transactions table tbody tr:nth-child(2) td:nth-child(6) a')
        expect(self.page).to_have_url(re.compile(r'/edit/\d+'))

        # 削除ボタンをクリック
        self.page.click('input[value="削除"]')

        # トップに戻って削除されたことを確認
        # edit.js の sendDeleteRow は window.location.href = document.referrer; を呼ぶ
        self.page.wait_for_url(self.live_server_url + reverse('moneybook:index'))
        self.page.wait_for_selector('#transactions table')

        expect(self.page.locator('#transactions table tbody tr')).to_have_count(1)

    def test_delete_multiple_data(self):
        """複数のデータのうち1件だけ削除できることを確認"""
        self._login()
        # データを2件追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.page.wait_for_selector('#transactions table')

        # 1件目
        self.page.fill('#a_day', '10')
        self.page.fill('#a_item', '残すデータ')
        self.page.fill('#a_price', '3000')
        self.page.click('input[value="追加"]')
        expect(self.page.locator('#transactions table tbody tr')).to_have_count(2, timeout=10000)

        # 2件目
        self.page.fill('#a_day', '11')
        self.page.fill('#a_item', '削除するデータ')
        self.page.fill('#a_price', '4000')
        self.page.click('input[value="追加"]')
        expect(self.page.locator('#transactions table tbody tr')).to_have_count(3, timeout=10000)

        # 2件目（削除するデータ）の編集画面に移動
        self.page.click('#transactions table tbody tr:nth-child(2) td:nth-child(6) a')

        # 削除ボタンをクリック
        self.page.click('input[value="削除"]')

        # トップに戻って1件だけ削除されたことを確認
        self.page.wait_for_url(self.live_server_url + reverse('moneybook:index'))
        self.page.wait_for_selector('#transactions table')

        rows = self.page.locator('#transactions table tbody tr')
        expect(rows).to_have_count(2)
        expect(rows.nth(1).locator('td').nth(1)).to_have_text('残すデータ')
