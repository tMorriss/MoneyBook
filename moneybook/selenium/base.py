import chromedriver_binary  # noqa: F401
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver


class SeleniumBase(StaticLiveServerTestCase):
    fixtures = ['data_test_case']
    username = 'tester'
    password = 'password'

    def setUp(self):
        super().setUp()

        User.objects.create_user(self.username, self.username + '@hoge.com', self.password)

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()
        super().tearDown()

    def _login(self):
        self.driver.get(self.live_server_url + reverse('moneybook:login'))
        username_input = self.driver.find_element_by_id('id_username')
        username_input.send_keys(self.username)
        password_input = self.driver.find_element_by_id('id_password')
        password_input.send_keys(self.password)
        self.driver.find_element_by_class_name('btn-apply').click()

    def _assert_common(self):
        # アプリ名
        self.assertEqual(self.driver.find_element_by_class_name("header-cont1").text, 'test-MoneyBook')
        # 名前表示
        self.assertTrue(self.username + "さん" in self.driver.find_element_by_class_name("header-cont2").text,
                        self.driver.find_element_by_class_name("header-cont2").text)
        # タスクバー
        expects = [
            {'href': reverse('moneybook:index'), 'text': 'ホーム'},
            {'href': reverse('moneybook:add'), 'text': '追加'},
            {'href': reverse('moneybook:statistics'), 'text': '統計'},
            {'href': reverse('moneybook:search'), 'text': '検索'},
            {'href': reverse('moneybook:tools'), 'text': 'ツール'}
        ]
        lis = self.driver.find_elements_by_xpath('//nav[@class="task_bar"]/ul/li')
        for i in range(len(lis)):
            with self.subTest(i=i):
                a = lis[i].find_element_by_tag_name('a')
                self.assertEqual(a.get_attribute('href'), self.live_server_url + expects[i]['href'])
                self.assertEqual(a.text, expects[i]['text'])

    def _assert_texts(self, actuals, expects):
        self.assertEqual(len(actuals), len(expects))
        for i in range(len(actuals)):
            with self.subTest(i=i):
                self.assertEqual(actuals[i].text, expects[i])
