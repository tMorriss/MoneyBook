import time

from django.urls import reverse
from moneybook.e2e.base import SeleniumBase
from moneybook.models import Data, PeriodicData
from selenium.webdriver.common.by import By


class Periodic(SeleniumBase):
    def test_get(self):
        """定期取引一覧ページにアクセスできること"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:periodic'))

        # ページタイトル確認
        self.assertIn('定期取引一覧', self.driver.page_source)

        # 追加ボタンと編集ボタンが存在すること
        self.assertTrue(self.driver.find_element(By.ID, 'btn_add_bulk'))
        edit_btn = self.driver.find_element(By.XPATH, '//input[@value="編集"]')
        self.assertTrue(edit_btn)

        # 年月入力欄が存在すること
        year_input = self.driver.find_element(By.ID, 'target_year')
        month_input = self.driver.find_element(By.ID, 'target_month')
        self.assertTrue(year_input)
        self.assertTrue(month_input)

        # placeholderの値を検証（来月）
        from datetime import datetime
        from dateutil.relativedelta import relativedelta
        now = datetime.now()
        next_month = now + relativedelta(months=1)
        self.assertEqual(year_input.get_attribute('placeholder'), str(next_month.year))
        self.assertEqual(month_input.get_attribute('placeholder'), str(next_month.month))

    def test_periodic_navigation(self):
        """タスクバーから定期取引ページに遷移できること"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:tools'))

        # 定期取引リンクをクリック
        periodic_link = self.driver.find_element(By.LINK_TEXT, '定期取引')
        periodic_link.click()
        time.sleep(0.5)

        self.assertEqual(self.driver.current_url, self.live_server_url + reverse('moneybook:periodic'))

    def test_periodic_edit_page_access(self):
        """編集ページに遷移できること"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:periodic'))

        # 編集ボタンをクリック
        edit_btn = self.driver.find_element(By.XPATH, '//input[@value="編集"]')
        edit_btn.click()
        time.sleep(0.5)

        # 編集ページに遷移すること
        self.assertEqual(self.driver.current_url, self.live_server_url + reverse('moneybook:periodic_edit'))
        self.assertIn('定期取引設定', self.driver.page_source)

    def test_periodic_add_and_display(self):
        """定期取引を追加して一覧に表示されること"""
        self._login()

        # 編集画面に遷移
        self._location(self.live_server_url + reverse('moneybook:periodic_edit'))

        # 行を追加ボタンをクリック
        self.driver.find_element(By.ID, 'btn_add_row').click()
        time.sleep(0.5)

        # 新しい行に値を入力
        rows = self.driver.find_elements(By.XPATH, '//table[@class="tbl-common tbl-boarder"]/tbody/tr')
        last_row = rows[-1]

        day_input = last_row.find_element(By.CSS_SELECTOR, 'input[name^="day_new_"]')
        day_input.clear()
        day_input.send_keys('15')

        item_input = last_row.find_element(By.CSS_SELECTOR, 'input[name^="item_new_"]')
        item_input.send_keys('テスト定期取引')

        price_input = last_row.find_element(By.CSS_SELECTOR, 'input[name^="price_new_"]')
        price_input.send_keys('5000')

        # 更新ボタンをクリック
        self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(1.5)

        # 一覧画面にリダイレクトされること
        self.assertEqual(self.driver.current_url, self.live_server_url + reverse('moneybook:periodic'))

        # 追加した定期取引が表示されていること
        self.assertIn('テスト定期取引', self.driver.page_source)
        self.assertIn('5,000', self.driver.page_source)

    def test_periodic_add_comma_and_formula(self):
        """金額にカンマや数式を含めて定期取引を追加できること"""
        self._login()

        # 編集画面に遷移
        self._location(self.live_server_url + reverse('moneybook:periodic_edit'))

        # カンマ入りの行を追加
        self.driver.find_element(By.ID, 'btn_add_row').click()
        time.sleep(0.5)

        rows = self.driver.find_elements(By.XPATH, '//table[@class="tbl-common tbl-boarder"]/tbody/tr')
        row_comma = rows[-1]
        row_comma.find_element(By.CSS_SELECTOR, 'input[name^="day_new_"]').send_keys('10')
        row_comma.find_element(By.CSS_SELECTOR, 'input[name^="item_new_"]').send_keys('カンマテスト')
        row_comma.find_element(By.CSS_SELECTOR, 'input[name^="price_new_"]').send_keys('1,234')

        # 数式入りの行を追加
        self.driver.find_element(By.ID, 'btn_add_row').click()
        time.sleep(0.5)

        rows = self.driver.find_elements(By.XPATH, '//table[@class="tbl-common tbl-boarder"]/tbody/tr')
        row_formula = rows[-1]
        row_formula.find_element(By.CSS_SELECTOR, 'input[name^="day_new_"]').send_keys('20')
        row_formula.find_element(By.CSS_SELECTOR, 'input[name^="item_new_"]').send_keys('数式テスト')
        row_formula.find_element(By.CSS_SELECTOR, 'input[name^="price_new_"]').send_keys('=1000+500')

        # 更新ボタンをクリック
        self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(1.5)

        # 一覧画面にリダイレクトされること
        self.assertEqual(self.driver.current_url, self.live_server_url + reverse('moneybook:periodic'))

        # 表示を確認
        self.assertIn('カンマテスト', self.driver.page_source)
        self.assertIn('1,234', self.driver.page_source)
        self.assertIn('数式テスト', self.driver.page_source)
        self.assertIn('1,500', self.driver.page_source)

    def test_periodic_bulk_add(self):
        """定期取引を一括登録できること"""
        # テスト用の定期取引データを作成
        from moneybook.models import Category, Direction, Method
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

        # 現在のデータ件数を取得
        before_count = Data.objects.count()

        # 年月を入力（2024年5月）
        year_input = self.driver.find_element(By.ID, 'target_year')
        year_input.clear()
        year_input.send_keys('2024')

        month_input = self.driver.find_element(By.ID, 'target_month')
        month_input.clear()
        month_input.send_keys('5')

        # 追加ボタンをクリック
        self.driver.find_element(By.ID, 'btn_add_bulk').click()
        time.sleep(2)

        # 成功メッセージが表示されること
        time.sleep(1)
        self.assertIn('Success!', self.driver.page_source)

        # データが追加されたこと
        after_count = Data.objects.count()
        self.assertEqual(after_count, before_count + 1)

        # 登録されたデータの内容を確認
        new_data = Data.objects.latest('id')
        self.assertEqual(new_data.item, 'E2Eテスト家賃')
        self.assertEqual(new_data.price, 50000)
        self.assertEqual(new_data.date.year, 2024)
        self.assertEqual(new_data.date.month, 5)
        self.assertEqual(new_data.date.day, 10)

    def test_periodic_delete_row(self):
        """定期取引を削除できること"""
        # テスト用の定期取引データを作成
        from moneybook.models import Category, Direction, Method
        PeriodicData.objects.create(
            day=20,
            item='削除テスト',
            price=1000,
            direction=Direction.get(2),
            method=Method.get(1),
            category=Category.get(1),
            temp=False
        )

        self._login()
        self._location(self.live_server_url + reverse('moneybook:periodic_edit'))

        # 削除ボタンをクリック
        delete_buttons = self.driver.find_elements(By.CLASS_NAME, 'btn-delete-row')
        if delete_buttons:
            initial_count = len(self.driver.find_elements(By.XPATH, '//table[@class="tbl-common tbl-boarder"]/tbody/tr'))

            delete_buttons[0].click()
            time.sleep(0.3)

            # 行が削除されたこと（DOMから即座に削除される）
            after_count = len(self.driver.find_elements(By.XPATH, '//table[@class="tbl-common tbl-boarder"]/tbody/tr'))
            self.assertEqual(after_count, initial_count - 1)

            # 更新ボタンをクリック
            self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
            time.sleep(1)

            # 一覧画面に戻ること
            self.assertEqual(self.driver.current_url, self.live_server_url + reverse('moneybook:periodic'))

            # 削除したアイテムが一覧にも表示されていないこと
            self.assertNotIn('削除テスト', self.driver.page_source)

    def test_periodic_default_month(self):
        """年月が未入力の場合、来月がデフォルトとして使用されること"""
        # テスト用の定期取引データを作成
        from datetime import datetime
        from dateutil.relativedelta import relativedelta
        from moneybook.models import Category, Direction, Method

        PeriodicData.objects.create(
            day=25,
            item='デフォルト月テスト',
            price=3000,
            direction=Direction.get(2),
            method=Method.get(1),
            category=Category.get(1),
            temp=False
        )

        self._login()
        self._location(self.live_server_url + reverse('moneybook:periodic'))

        # placeholderの値を確認（来月になっているはず）
        now = datetime.now()
        next_month = now + relativedelta(months=1)
        year_input = self.driver.find_element(By.ID, 'target_year')
        month_input = self.driver.find_element(By.ID, 'target_month')

        self.assertEqual(year_input.get_attribute('placeholder'), str(next_month.year))
        self.assertEqual(month_input.get_attribute('placeholder'), str(next_month.month))

        # 現在のデータ件数を取得
        before_count = Data.objects.count()

        # 年月を入力せずに追加ボタンをクリック（デフォルト値が使用される）
        self.driver.find_element(By.ID, 'btn_add_bulk').click()
        time.sleep(2)

        # 成功メッセージが表示されること
        time.sleep(1)
        self.assertIn('Success!', self.driver.page_source)

        # データが追加されたこと
        after_count = Data.objects.count()
        self.assertEqual(after_count, before_count + 1)

        # 登録されたデータの内容を確認（来月の25日に登録されているはず）
        new_data = Data.objects.latest('id')
        self.assertEqual(new_data.item, 'デフォルト月テスト')
        self.assertEqual(new_data.price, 3000)
        self.assertEqual(new_data.date.year, next_month.year)
        self.assertEqual(new_data.date.month, next_month.month)
        self.assertEqual(new_data.date.day, 25)

    def test_periodic_edit_cancel(self):
        """編集してキャンセルを押すと保存されないこと"""
        # テスト用の定期取引データを作成
        from moneybook.models import Category, Direction, Method
        pd = PeriodicData.objects.create(
            day=15,
            item='キャンセルテスト',
            price=2000,
            direction=Direction.get(2),
            method=Method.get(1),
            category=Category.get(1),
            temp=False
        )

        self._login()
        self._location(self.live_server_url + reverse('moneybook:periodic_edit'))

        # 編集前のDB状態を保存
        original_item = pd.item
        original_price = pd.price

        # 最初の行を編集
        rows = self.driver.find_elements(By.XPATH, '//table[@class="tbl-common tbl-boarder"]/tbody/tr')
        if rows:
            first_row = rows[0]
            item_input = first_row.find_element(By.CSS_SELECTOR, 'input[name^="item_"]')
            item_input.clear()
            item_input.send_keys('変更後')

            price_input = first_row.find_element(By.CSS_SELECTOR, 'input[name^="price_"]')
            price_input.clear()
            price_input.send_keys('9999')

            # キャンセルボタンをクリック
            self.driver.find_element(By.XPATH, '//button[text()="キャンセル"]').click()
            time.sleep(1)

            # 一覧画面に戻ること
            self.assertEqual(self.driver.current_url, self.live_server_url + reverse('moneybook:periodic'))

            # DBの値が変更されていないこと
            pd.refresh_from_db()
            self.assertEqual(pd.item, original_item)
            self.assertEqual(pd.price, original_price)

            # 一覧画面でも元の値が表示されていること
            self.assertIn(original_item, self.driver.page_source)
            self.assertNotIn('変更後', self.driver.page_source)

    def test_periodic_delete_cancel(self):
        """削除ボタンを押してキャンセルすると保存されないこと"""
        # テスト用の定期取引データを2件作成
        from moneybook.models import Category, Direction, Method
        PeriodicData.objects.create(
            day=1,
            item='削除キャンセルテスト1',
            price=1111,
            direction=Direction.get(2),
            method=Method.get(1),
            category=Category.get(1),
            temp=False
        )
        PeriodicData.objects.create(
            day=2,
            item='削除キャンセルテスト2',
            price=2222,
            direction=Direction.get(2),
            method=Method.get(1),
            category=Category.get(1),
            temp=False
        )

        self._login()
        self._location(self.live_server_url + reverse('moneybook:periodic_edit'))

        # 初期件数を確認
        initial_db_count = PeriodicData.objects.count()
        initial_row_count = len(self.driver.find_elements(By.XPATH, '//table[@class="tbl-common tbl-boarder"]/tbody/tr'))

        # 削除ボタンをクリック
        delete_buttons = self.driver.find_elements(By.CLASS_NAME, 'btn-delete-row')
        if delete_buttons:
            delete_buttons[0].click()
            time.sleep(0.3)

            # DOM上では削除されている
            after_click_count = len(self.driver.find_elements(By.XPATH, '//table[@class="tbl-common tbl-boarder"]/tbody/tr'))
            self.assertEqual(after_click_count, initial_row_count - 1)

            # キャンセルボタンをクリック
            self.driver.find_element(By.XPATH, '//button[text()="キャンセル"]').click()
            time.sleep(1)

            # 一覧画面に戻ること
            self.assertEqual(self.driver.current_url, self.live_server_url + reverse('moneybook:periodic'))

            # DBの件数が変わっていないこと
            final_db_count = PeriodicData.objects.count()
            self.assertEqual(final_db_count, initial_db_count)

            # 一覧画面で元のデータが全て表示されていること
            self.assertIn('削除キャンセルテスト1', self.driver.page_source)
            self.assertIn('削除キャンセルテスト2', self.driver.page_source)

    def test_periodic_duplicate_add(self):
        """同じ月に複数回一括登録できること（重複チェックなし）"""
        # テスト用の定期取引データを作成
        from moneybook.models import Category, Direction, Method
        PeriodicData.objects.create(
            day=5,
            item='重複テスト',
            price=5555,
            direction=Direction.get(2),
            method=Method.get(1),
            category=Category.get(1),
            temp=False
        )

        self._login()
        self._location(self.live_server_url + reverse('moneybook:periodic'))

        # 年月を入力（2024年6月）
        year_input = self.driver.find_element(By.ID, 'target_year')
        year_input.clear()
        year_input.send_keys('2024')

        month_input = self.driver.find_element(By.ID, 'target_month')
        month_input.clear()
        month_input.send_keys('6')

        # 1回目の追加
        before_count_1 = Data.objects.count()
        self.driver.find_element(By.ID, 'btn_add_bulk').click()
        time.sleep(2.5)
        after_count_1 = Data.objects.count()
        self.assertEqual(after_count_1, before_count_1 + 1)

        # 2回目の追加（同じ月に再度登録）
        self.driver.find_element(By.ID, 'btn_add_bulk').click()
        time.sleep(2.5)
        after_count_2 = Data.objects.count()
        self.assertEqual(after_count_2, after_count_1 + 1)

        # 2件とも登録されていること
        june_data = Data.objects.filter(date__year=2024, date__month=6, item='重複テスト')
        self.assertEqual(june_data.count(), 2)
