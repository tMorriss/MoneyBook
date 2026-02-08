import time

from django.urls import reverse
from moneybook.selenium.base import SeleniumBase
from selenium.webdriver.common.by import By


class Delete(SeleniumBase):
    def test_delete_from_edit_page(self):
        '''編集画面から削除できることを確認'''
        self._login()
        # データを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('削除テスト')
        self.driver.find_element(By.ID, 'a_price').send_keys('1000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # データが追加されたことを確認
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        initial_count = len(rows)
        self.assertEqual(initial_count, 2)  # ヘッダー + 1件

        # 編集画面に移動
        self.driver.find_element(By.XPATH, '//*[@id="transactions"]/table/tbody/tr[2]/td[6]/a').click()
        time.sleep(1)

        # 削除ボタンをクリック
        self.driver.find_element(By.XPATH, '//input[@value="削除"]').click()
        time.sleep(1)

        # アラートを承認
        alert = self.driver.switch_to.alert
        alert.accept()
        time.sleep(2)

        # トップに戻って削除されたことを確認
        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        self.assertEqual(len(rows), 1)  # ヘッダーのみ

    def test_delete_cancel(self):
        '''削除確認ダイアログでキャンセルすると削除されないことを確認'''
        self._login()
        # データを追加
        self._location(self.live_server_url + reverse('moneybook:index'))
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('キャンセルテスト')
        self.driver.find_element(By.ID, 'a_price').send_keys('2000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # データが追加されたことを確認
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        self.assertEqual(len(rows), 2)  # ヘッダー + 1件

        # 編集画面に移動
        self.driver.find_element(By.XPATH, '//*[@id="transactions"]/table/tbody/tr[2]/td[6]/a').click()
        time.sleep(1)

        # 削除ボタンをクリック
        self.driver.find_element(By.XPATH, '//input[@value="削除"]').click()
        time.sleep(1)

        # アラートをキャンセル
        alert = self.driver.switch_to.alert
        alert.dismiss()
        time.sleep(1)

        # トップに戻ってデータがまだ存在することを確認
        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        self.assertEqual(len(rows), 2)  # ヘッダー + 1件
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[1].text, 'キャンセルテスト')

    def test_delete_multiple_data(self):
        '''複数のデータのうち1件だけ削除できることを確認'''
        self._login()
        # データを2件追加
        self._location(self.live_server_url + reverse('moneybook:index'))

        # 1件目
        self.driver.find_element(By.ID, 'a_day').send_keys('10')
        self.driver.find_element(By.ID, 'a_item').send_keys('残すデータ')
        self.driver.find_element(By.ID, 'a_price').send_keys('3000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 2件目
        self.driver.find_element(By.ID, 'a_day').send_keys('11')
        self.driver.find_element(By.ID, 'a_item').send_keys('削除するデータ')
        self.driver.find_element(By.ID, 'a_price').send_keys('4000')
        self.driver.find_element(By.XPATH, '//*[@id="filter-fixed"]/form/input[@value="追加"]').click()
        time.sleep(2)

        # 2件追加されたことを確認
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        self.assertEqual(len(rows), 3)  # ヘッダー + 2件

        # 2件目（削除するデータ）の編集画面に移動
        self.driver.find_element(By.XPATH, '//*[@id="transactions"]/table/tbody/tr[2]/td[6]/a').click()
        time.sleep(1)

        # 削除ボタンをクリック
        self.driver.find_element(By.XPATH, '//input[@value="削除"]').click()
        time.sleep(1)

        # アラートを承認
        alert = self.driver.switch_to.alert
        alert.accept()
        time.sleep(2)

        # トップに戻って1件だけ削除されたことを確認
        self._location(self.live_server_url + reverse('moneybook:index'))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="transactions"]/table/tbody/tr')
        self.assertEqual(len(rows), 2)  # ヘッダー + 1件
        tds = rows[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[1].text, '残すデータ')
