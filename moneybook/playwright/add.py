import os
import re
import time
from datetime import datetime

from django.urls import reverse
from moneybook.models import Data
from moneybook.playwright.base import PlaywrightBase
from playwright.sync_api import expect


class Add(PlaywrightBase):
    fixtures = ['test_case']

    def setUp(self):
        os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'
        super().setUp()
        self.page.set_default_timeout(40000)
        # ログ出力
        self.page.on('console', lambda msg: print(f'BROWSER CONSOLE: {msg.text}'))

    def _robust_clear_data(self):
        """SQLiteのロックを考慮しつつデータを全削除"""
        self.page.goto('about:blank')
        for i in range(10):
            try:
                Data.objects.all().delete()
                time.sleep(0.5)
                if Data.objects.count() == 0:
                    return
            except Exception as e:
                print(f'Cleanup failed (attempt {i}): {e}')
                time.sleep(0.5)

    def _goto_index_and_wait(self, expected_count):
        """一覧ページへ移動し、指定された件数が表示されるまで待機"""
        now = datetime.now()
        url = self.live_server_url + reverse('moneybook:index_month', kwargs={'year': now.year, 'month': now.month})

        for i in range(5):
            self.page.goto(url, wait_until='load')
            # AJAX完了待ち
            try:
                self.page.wait_for_function('() => window.jQuery && window.jQuery.active === 0', timeout=10000)
            except Exception:
                pass

            try:
                rows = self.page.locator('#transactions table tr.data-row')
                # 行数を検証
                expect(rows).to_have_count(expected_count, timeout=10000)
                # 集計欄が更新されていることを確認
                expect(self.page.locator('#summary-count')).to_have_text(f'{expected_count}件', timeout=5000)
                return rows
            except Exception as e:
                db_count = Data.objects.count()
                print(f'Index sync attempt {i+1} failed. Expected {expected_count}, DB has {db_count}. Error: {e}')
                if i == 4:
                    raise
                time.sleep(2)

    def _goto_add(self):
        """追加ページへ移動し、準備完了を待機"""
        url = self.live_server_url + reverse('moneybook:add')
        for i in range(3):
            self.page.goto(url, wait_until='load')
            try:
                # 明示的に追加画面の要素を待つ
                expect(self.page.get_by_role('heading', name='銀行チャージ')).to_be_visible(timeout=10000)
                return
            except Exception:
                if i == 2:
                    raise
                time.sleep(2)

    def test_add_functionalities(self):
        """全ての追加操作を1つの連続したシナリオでテストする"""
        self._login()
        self._robust_clear_data()

        # --- 1. 追加ページ表示 ---
        self._goto_add()
        now = datetime.now()
        expect(self.page.locator('#c_year')).to_have_value(str(now.year))

        # --- 2. 銀行チャージ (Click) ---
        self.page.fill('#c_day', '1')
        self.page.fill('#c_price', '1000')
        with self.page.expect_response(re.compile(r'.*/api/add/intra-move')):
            self.page.locator('form').nth(0).get_by_role('button', name='追加').click()
        expect(self.page.locator('#result_message')).to_have_text('Success!')

        rows = self._goto_index_and_wait(2)
        expect(self.page.locator('#transactions').get_by_text('Kyashチャージ').first).to_be_visible()

        # 編集ページでの方向確認
        rows.nth(1).get_by_role('link', name='編集').click()
        self.page.wait_for_url(re.compile(r'.*/edit/\d+'), wait_until='load')
        expect(self.page.locator('#direction-2')).to_be_checked()

        # --- 3. 内部移動 (Enter) ---
        self._goto_add()
        self.page.fill('#m_day', '2')
        self.page.fill('#m_item', 'move-test')
        self.page.fill('#m_price', '2000')
        self.page.locator('#lbl_m_before_method-1').click()  # 現金
        self.page.locator('#lbl_m_after_method-6').click()   # Kyash
        with self.page.expect_response(re.compile(r'.*/api/add/intra-move')):
            self.page.press('#m_item', 'Enter')
        expect(self.page.locator('#result_message')).to_have_text('Success!')
        self._goto_index_and_wait(4)  # 2 + 2 = 4
        expect(self.page.locator('#transactions').get_by_text('move-test').first).to_be_visible()

        # --- 4. 通常追加 (Click + 立替) ---
        self._goto_add()
        self.page.fill('#a_day', '5')
        self.page.fill('#a_item', 'man-tmp')
        self.page.fill('#a_price', '500')
        self.page.locator('#lbl_a_temp-1').click()  # Yes
        with self.page.expect_response(re.compile(r'.*/api/add$')):
            self.page.locator('form').nth(3).get_by_role('button', name='追加').click()
        expect(self.page.locator('#result_message')).to_have_text('Success!')
        rows = self._goto_index_and_wait(5)
        expect(rows.first.get_by_text('立替')).to_be_visible()

        # --- 5. ショートカット & デフォルト ---
        self._robust_clear_data()
        self._goto_add()
        with self.page.expect_response(re.compile(r'.*/api/add$')):
            self.page.get_by_role('button', name='Suicaチャージ').click()
        expect(self.page.locator('#result_message')).to_have_text('Success!')
        self._goto_index_and_wait(1)
        expect(self.page.locator('#transactions').get_by_text('1,000')).to_be_visible()

        # --- 6. 電車代 ---
        self._goto_add()
        self.page.fill('#s_day', '10')
        self.page.fill('#s_price', '600')
        with self.page.expect_response(re.compile(r'.*/api/add$')):
            self.page.get_by_role('button', name='電車代').click()
        expect(self.page.locator('#result_message')).to_have_text('Success!')
        self._goto_index_and_wait(2)
        expect(self.page.locator('#transactions').get_by_text('電車代').first).to_be_visible()

        # --- 7. 計算式 ---
        self._goto_add()
        self.page.fill('#a_day', '15')
        self.page.fill('#a_item', 'formula-test')
        self.page.fill('#a_price', '=50*4')
        with self.page.expect_response(re.compile(r'.*/api/add$')):
            self.page.locator('form').nth(3).get_by_role('button', name='追加').click()
        expect(self.page.locator('#result_message')).to_have_text('Success!')
        self._goto_index_and_wait(3)
        expect(self.page.locator('#transactions').get_by_text('200').first).to_be_visible()
