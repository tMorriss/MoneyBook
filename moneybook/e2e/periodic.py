import time

from django.urls import reverse
from moneybook.e2e.base import SeleniumBase
from moneybook.models import Data, PeriodicData
from selenium.webdriver.common.by import By


class Periodic(SeleniumBase):
    def test_periodic_list_access(self):
        """定期取引一覧ページにアクセスできること"""
        self._login()
        self._location(self.live_server_url + reverse('moneybook:periodic'))

        # ページタイトル確認
        self.assertIn('定期取引一覧', self.driver.page_source)

        # 追加ボタンと編集ボタンが存在すること
        self.assertTrue(self.driver.find_element(By.ID, 'btn_add_bulk'))
        edit_btn = self.driver.find_element(By.XPATH, '//input[@value="編集"]')
        self.assertTrue(edit_btn)

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
