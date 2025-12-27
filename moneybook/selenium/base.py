import os
import shutil

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


class SeleniumBase(StaticLiveServerTestCase):
    fixtures = ['data_test_case']
    username = 'tester'
    password = 'password'

    def setUp(self):
        super().setUp()

        User.objects.create_user(self.username, self.username + '@hoge.com', self.password)

        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-extensions')

        # Find ChromeDriver - works on both Windows and Linux
        chromedriver_path = self._find_chromedriver()
        if chromedriver_path:
            service = Service(chromedriver_path)
            self.driver = webdriver.Chrome(service=service, options=options)
        else:
            # Let Selenium's built-in driver management handle it
            self.driver = webdriver.Chrome(options=options)

        self.driver.implicitly_wait(10)

    def _find_chromedriver(self):
        """Find ChromeDriver in common locations for Windows and Linux."""
        # Check if chromedriver is in PATH
        chromedriver_in_path = shutil.which('chromedriver')
        if chromedriver_in_path:
            return chromedriver_in_path

        # Common locations to check
        common_paths = [
            '/usr/bin/chromedriver',  # Linux (CI)
            '/usr/local/bin/chromedriver',  # Linux
            'C:\\chromedriver.exe',  # Windows (root)
            os.path.expanduser('~\\chromedriver.exe'),  # Windows (user home)
        ]

        for path in common_paths:
            if os.path.isfile(path):
                return path

        return None

    def tearDown(self):
        self.driver.quit()
        super().tearDown()

    def _login(self):
        self.driver.get(self.live_server_url + reverse('moneybook:login'))
        # Wait for the login form to be ready
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.ID, 'id_username'))
        )
        username_input = self.driver.find_element(By.ID, 'id_username')
        username_input.send_keys(self.username)
        password_input = self.driver.find_element(By.ID, 'id_password')
        password_input.send_keys(self.password)
        self.driver.find_element(By.CLASS_NAME, 'btn-apply').click()
        # Wait for the redirect to complete
        WebDriverWait(self.driver, 10).until(
            expected_conditions.url_changes(self.live_server_url + reverse('moneybook:login'))
        )

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
