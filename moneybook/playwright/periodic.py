from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.urls import reverse
from moneybook.models import Data, PeriodicData, Category, Direction, Method
from moneybook.playwright.base import PlaywrightBase
from playwright.sync_api import expect


class PeriodicTest(PlaywrightBase):
    def test_periodic_navigation_and_access(self):
        """定期取引ページへの遷移と表示の確認"""
        self._login()

        # タスクバーからツールページへ
        self._location(self.live_server_url + reverse('moneybook:tools'))
        # 定期取引リンクをクリック
        self.page.click('text=定期取引')
        expect(self.page).to_have_url(self.live_server_url + reverse('moneybook:periodic'))

        # ページタイトル確認 (h1が複数あるのでsection内のものを指定)
        expect(self.page.locator('section h1')).to_have_text('定期取引一覧')

        # ボタンの存在確認
        expect(self.page.locator('#btn_add_bulk')).to_be_visible()
        expect(self.page.locator('input[value="編集"]')).to_be_visible()

        # 年月入力欄とplaceholderの検証
        year_input = self.page.locator('#target_year')
        month_input = self.page.locator('#target_month')
        next_month = datetime.now() + relativedelta(months=1)
        expect(year_input).to_have_attribute('placeholder', str(next_month.year))
        expect(month_input).to_have_attribute('placeholder', str(next_month.month))

        # 編集ページへの遷移
        self.page.click('input[value="編集"]')
        expect(self.page).to_have_url(self.live_server_url + reverse('moneybook:periodic_edit'))
        expect(self.page.locator('h2')).to_have_text('定期取引設定')

    def test_periodic_add_variations(self):
        """定期取引の追加（通常、カンマ入り、数式）"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:periodic_edit'))

        # 1. 通常の追加
        self.page.click('#btn_add_row')
        # name^="day_new_" は index.js 側で動的に付与される
        self.page.fill('input[name^="day_new_0"]', '15')
        self.page.fill('input[name^="item_new_0"]', 'テスト定期取引')
        self.page.fill('input[name^="price_new_0"]', '5000')
        self.page.select_option('select[name^="temp_new_0"]', '0')

        # 2. カンマ入りの追加
        self.page.click('#btn_add_row')
        self.page.fill('input[name^="day_new_1"]', '10')
        self.page.fill('input[name^="item_new_1"]', 'カンマテスト')
        self.page.fill('input[name^="price_new_1"]', '1,234')

        # 3. 数式の追加
        self.page.click('#btn_add_row')
        self.page.fill('input[name^="day_new_2"]', '20')
        self.page.fill('input[name^="item_new_2"]', '数式テスト')
        self.page.fill('input[name^="price_new_2"]', '=1000+500')

        # 更新
        self.page.click('button[type="submit"]')
        expect(self.page).to_have_url(self.live_server_url + reverse('moneybook:periodic'))

        # 表示の確認
        expect(self.page.locator('body')).to_contain_text('テスト定期取引')
        expect(self.page.locator('body')).to_contain_text('5,000')
        expect(self.page.locator('body')).to_contain_text('カンマテスト')
        expect(self.page.locator('body')).to_contain_text('1,234')
        expect(self.page.locator('body')).to_contain_text('数式テスト')
        expect(self.page.locator('body')).to_contain_text('1,500')

    def test_periodic_bulk_add_and_defaults(self):
        """一括登録、デフォルト年月、重複登録の確認"""
        # テストデータの準備
        PeriodicData.objects.create(
            day=10,
            item='E2Eテスト家賃',
            price=50000,
            direction=Direction.get(2),
            method=Method.get(1),
            category=Category.get(1),
            temp=False
        )

        self._login()
        self._location(self.live_server_url + reverse('moneybook:periodic'))

        # 1. 指定年月での一括登録
        before_count = Data.objects.count()
        self.page.fill('#target_year', '2024')
        self.page.fill('#target_month', '5')
        self.page.click('#btn_add_bulk')

        # 成功メッセージ待ち (jQuery AJAX)
        expect(self.page.locator('#result_message')).to_contain_text('Success!')

        self.assertEqual(Data.objects.filter(item='E2Eテスト家賃', date__year=2024, date__month=5).count(), 1)
        after_count = Data.objects.count()
        self.assertEqual(after_count, before_count + 1)

        # 2. 重複登録
        self.page.click('#btn_add_bulk')
        expect(self.page.locator('#result_message')).to_contain_text('Success!')
        self.assertEqual(Data.objects.filter(item='E2Eテスト家賃', date__year=2024, date__month=5).count(), 2)

        # 3. デフォルト年月（来月）での登録
        next_month = datetime.now() + relativedelta(months=1)
        self.page.fill('#target_year', '')
        self.page.fill('#target_month', '')
        self.page.click('#btn_add_bulk')
        expect(self.page.locator('#result_message')).to_contain_text('Success!')

        self.assertEqual(Data.objects.filter(item='E2Eテスト家賃', date__year=next_month.year, date__month=next_month.month).count(), 1)

    def test_periodic_edit_delete_and_cancel(self):
        """編集、削除、キャンセルの動作確認"""
        # テストデータの準備
        pd = PeriodicData.objects.create(
            day=1,
            item='初期アイテム',
            price=1000,
            direction=Direction.get(2),
            method=Method.get(1),
            category=Category.get(1),
            temp=False
        )

        self._login()

        # 1. 編集してキャンセル
        self._location(self.live_server_url + reverse('moneybook:periodic_edit'))
        self.page.fill(f'input[name="item_{pd.pk}"]', '変更されたアイテム')
        self.page.click('text=キャンセル')
        expect(self.page).to_have_url(self.live_server_url + reverse('moneybook:periodic'))

        pd.refresh_from_db()
        self.assertEqual(pd.item, '初期アイテム')
        expect(self.page.locator('body')).to_contain_text('初期アイテム')

        # 2. 削除してキャンセル
        self._location(self.live_server_url + reverse('moneybook:periodic_edit'))
        self.page.click(f'button.btn-delete-row[data-id="{pd.pk}"]')
        # DOMから消えていることを確認
        expect(self.page.locator(f'input[name="item_{pd.pk}"]')).to_have_count(0)
        self.page.click('text=キャンセル')

        expect(self.page).to_have_url(self.live_server_url + reverse('moneybook:periodic'))
        self.assertEqual(PeriodicData.objects.filter(pk=pd.pk).count(), 1)
        expect(self.page.locator('body')).to_contain_text('初期アイテム')

        # 3. 削除して保存
        self._location(self.live_server_url + reverse('moneybook:periodic_edit'))
        self.page.click(f'button.btn-delete-row[data-id="{pd.pk}"]')
        self.page.click('button[type="submit"]')

        expect(self.page).to_have_url(self.live_server_url + reverse('moneybook:periodic'))
        self.assertEqual(PeriodicData.objects.filter(pk=pd.pk).count(), 0)
        expect(self.page.locator('body')).not_to_contain_text('初期アイテム')
