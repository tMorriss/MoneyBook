import os
import time

import chromedriver_binary  # noqa: F401
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By


class SeleniumBase(StaticLiveServerTestCase):
    fixtures = ['data_test_case']
    username = 'tester'
    password = 'GZK-kva_yfj1ahr0tcr'  # Chromeで警告が出ちゃうので複雑なパスワードを使う

    def setUp(self):
        super().setUp()

        User.objects.create_user(self.username, self.username + '@hoge.com', self.password)

        options = webdriver.ChromeOptions()
        if os.environ.get('HEADLESS') != '0':
            options.add_argument('--headless')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()
        super().tearDown()

    def _location(self, url):
        self.driver.get(url)
        time.sleep(0.5)

    def _login(self):
        self._location(self.live_server_url + reverse('moneybook:login'))
        username_input = self.driver.find_element(By.ID, 'id_username')
        username_input.send_keys(self.username)
        password_input = self.driver.find_element(By.ID, 'id_password')
        password_input.send_keys(self.password)
        time.sleep(0.5)
        self.driver.find_element(By.CLASS_NAME, 'btn-apply').click()
        time.sleep(0.5)

    def _assert_common(self):
        # アプリ名
        self.assertEqual(self.driver.find_element(By.CLASS_NAME, "header-cont1").text, 'test-MoneyBook')
        # 名前表示
        self.assertTrue(self.username + "さん" in self.driver.find_element(By.CLASS_NAME, "header-cont2").text,
                        self.driver.find_element(By.CLASS_NAME, "header-cont2").text)
        # タスクバー
        expects = [
            {'href': reverse('moneybook:index'), 'text': 'ホーム'},
            {'href': reverse('moneybook:add'), 'text': '追加'},
            {'href': reverse('moneybook:statistics'), 'text': '統計'},
            {'href': reverse('moneybook:periodic_list'), 'text': '定期取引'},
            {'href': reverse('moneybook:search'), 'text': '検索'},
            {'href': reverse('moneybook:tools'), 'text': 'ツール'}
        ]
        lis = self.driver.find_elements(By.XPATH, '//nav[@class="task_bar"]/ul/li')
        for i in range(len(lis)):
            with self.subTest(i=i):
                a = lis[i].find_element(By.TAG_NAME, 'a')
                self.assertEqual(a.get_attribute('href'), self.live_server_url + expects[i]['href'])
                self.assertEqual(a.text, expects[i]['text'])

    def _assert_texts(self, actuals, expects):
        self.assertEqual(len(actuals), len(expects))
        for i in range(len(actuals)):
            with self.subTest(i=i):
                self.assertEqual(actuals[i].text, expects[i])
