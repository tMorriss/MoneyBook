from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.urls import reverse
from moneybook.models import Category, Data, Direction, Method, PeriodicData
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
        expect(self.page.locator('input#btn_add_bulk[value="追加"]')).to_be_visible()
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

    def test_periodic_add_normal(self):
        """定期取引の追加（通常）"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:periodic_edit'))

        self.page.click('#btn_add_row')
        self.page.fill('input[name^="day_new_0"]', '15')
        self.page.fill('input[name^="item_new_0"]', 'テスト定期取引')
        self.page.fill('input[name^="price_new_0"]', '5000')
        self.page.select_option('select[name^="direction_new_0"]', '2')  # 支出
        self.page.select_option('select[name^="method_new_0"]', '2')     # 銀行
        self.page.select_option('select[name^="category_new_0"]', '2')   # 必需品
        self.page.select_option('select[name^="temp_new_0"]', '1')       # あり

        self.page.click('button[type="submit"]')
        expect(self.page).to_have_url(self.live_server_url + reverse('moneybook:periodic'))

        expect(self.page.locator('#periodic_table')).to_contain_text('テスト定期取引')
        expect(self.page.locator('#periodic_table')).to_contain_text('5,000')
        expect(self.page.locator('#periodic_table')).to_contain_text('支出')
        expect(self.page.locator('#periodic_table')).to_contain_text('銀行')
        expect(self.page.locator('#periodic_table')).to_contain_text('必需品')
        expect(self.page.locator('#periodic_table')).to_contain_text('Yes')

    def test_periodic_add_comma(self):
        """定期取引の追加（カンマ入り）"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:periodic_edit'))

        self.page.click('#btn_add_row')
        self.page.fill('input[name^="day_new_0"]', '10')
        self.page.fill('input[name^="item_new_0"]', 'カンマテスト')
        self.page.fill('input[name^="price_new_0"]', '1,234')

        self.page.click('button[type="submit"]')
        expect(self.page).to_have_url(self.live_server_url + reverse('moneybook:periodic'))

        expect(self.page.locator('#periodic_table')).to_contain_text('カンマテスト')
        expect(self.page.locator('#periodic_table')).to_contain_text('1,234')

    def test_periodic_add_formula(self):
        """定期取引の追加（数式）"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:periodic_edit'))

        self.page.click('#btn_add_row')
        self.page.fill('input[name^="day_new_0"]', '20')
        self.page.fill('input[name^="item_new_0"]', '数式テスト')
        self.page.fill('input[name^="price_new_0"]', '=1000+500')

        self.page.click('button[type="submit"]')
        expect(self.page).to_have_url(self.live_server_url + reverse('moneybook:periodic'))

        expect(self.page.locator('#periodic_table')).to_contain_text('数式テスト')
        expect(self.page.locator('#periodic_table')).to_contain_text('1,500')

    def test_periodic_bulk_add(self):
        """定期取引の一括登録と重複登録の確認"""
        # テストデータの準備
        PeriodicData.objects.create(
            day=10,
            item='E2Eテスト家賃',
            price=50000,
            direction=Direction.objects.get(pk=2),
            method=Method.objects.get(pk=1),
            category=Category.objects.get(pk=1),
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

    def test_periodic_bulk_add_default_month(self):
        """デフォルト年月（来月）での一括登録確認"""
        # テストデータの準備
        PeriodicData.objects.create(
            day=25,
            item='デフォルト月テスト',
            price=3000,
            direction=Direction.objects.get(pk=2),
            method=Method.objects.get(pk=1),
            category=Category.objects.get(pk=1),
            temp=False
        )

        self._login()
        self._location(self.live_server_url + reverse('moneybook:periodic'))

        next_month = datetime.now() + relativedelta(months=1)
        # 年月を入力せずに追加ボタンをクリック
        self.page.fill('#target_year', '')
        self.page.fill('#target_month', '')
        self.page.click('#btn_add_bulk')
        expect(self.page.locator('#result_message')).to_contain_text('Success!')

        self.assertEqual(Data.objects.filter(item='デフォルト月テスト', date__year=next_month.year, date__month=next_month.month).count(), 1)

    def test_periodic_edit_save(self):
        """編集して保存できること"""
        PeriodicData.objects.create(
            day=1,
            item='初期アイテム',
            price=1000,
            direction=Direction.objects.get(pk=2),
            method=Method.objects.get(pk=1),
            category=Category.objects.get(pk=1),
            temp=False
        )

        self._login()
        self._location(self.live_server_url + reverse('moneybook:periodic_edit'))

        # 編集対象のpkを取得
        pd_pk = PeriodicData.objects.first().pk

        self.page.fill(f'input[name="item_{pd_pk}"]', '変更保存アイテム')
        self.page.click('button[type="submit"]')

        expect(self.page).to_have_url(self.live_server_url + reverse('moneybook:periodic'))
        # 編集後はpkが変わる可能性があるので、内容で検索
        self.assertEqual(PeriodicData.objects.filter(item='変更保存アイテム').count(), 1)

    def test_periodic_edit_cancel(self):
        """編集してキャンセルすると保存されないこと"""
        pd = PeriodicData.objects.create(
            day=1,
            item='キャンセルアイテム',
            price=1000,
            direction=Direction.objects.get(pk=2),
            method=Method.objects.get(pk=1),
            category=Category.objects.get(pk=1),
            temp=False
        )

        self._login()
        self._location(self.live_server_url + reverse('moneybook:periodic_edit'))

        self.page.fill(f'input[name="item_{pd.pk}"]', '変更キャンセルアイテム')
        self.page.click('text=キャンセル')

        expect(self.page).to_have_url(self.live_server_url + reverse('moneybook:periodic'))
        pd.refresh_from_db()
        self.assertEqual(pd.item, 'キャンセルアイテム')

    def test_periodic_delete_save(self):
        """削除して保存できること"""
        pd = PeriodicData.objects.create(
            day=1,
            item='削除アイテム',
            price=1000,
            direction=Direction.objects.get(pk=2),
            method=Method.objects.get(pk=1),
            category=Category.objects.get(pk=1),
            temp=False
        )

        self._login()
        self._location(self.live_server_url + reverse('moneybook:periodic_edit'))

        self.page.click(f'button.btn-delete-row[data-id="{pd.pk}"]')
        self.page.click('button[type="submit"]')

        expect(self.page).to_have_url(self.live_server_url + reverse('moneybook:periodic'))
        self.assertEqual(PeriodicData.objects.filter(item='削除アイテム').count(), 0)

    def test_periodic_delete_cancel(self):
        """削除してキャンセルすると保存されないこと"""
        pd = PeriodicData.objects.create(
            day=1,
            item='削除キャンセルアイテム',
            price=1000,
            direction=Direction.objects.get(pk=2),
            method=Method.objects.get(pk=1),
            category=Category.objects.get(pk=1),
            temp=False
        )

        self._login()
        self._location(self.live_server_url + reverse('moneybook:periodic_edit'))

        self.page.click(f'button.btn-delete-row[data-id="{pd.pk}"]')
        # DOMから消えていることを確認
        expect(self.page.locator(f'input[name="item_{pd.pk}"]')).to_have_count(0)
        self.page.click('text=キャンセル')

        expect(self.page).to_have_url(self.live_server_url + reverse('moneybook:periodic'))
        self.assertEqual(PeriodicData.objects.filter(pk=pd.pk).count(), 1)
