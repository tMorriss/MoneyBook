import os

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from playwright.sync_api import sync_playwright


class PlaywrightBase(StaticLiveServerTestCase):
    fixtures = ['test_case', 'data_test_case']
    username = 'tester'
    # Chromeで警告が出ないように複雑なパスワードを使う
    password = 'GZK-kva_yfj1ahr0tcr'

    def setUp(self):
        super().setUp()

        User.objects.create_user(self.username, self.username + '@hoge.com', self.password)

        self.playwright = sync_playwright().start()
        headless = os.environ.get('HEADLESS') != '0'
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context(viewport={'width': 1920, 'height': 1080})
        self.context.tracing.start(screenshots=True, snapshots=True, sources=True)
        self.page = self.context.new_page()

    def tearDown(self):
        # 失敗時にトレースを保存する
        outcome = self._outcome
        result = outcome.result
        failed = False
        last_failure = None
        if result.failures and result.failures[-1][0] == self:
            last_failure = result.failures[-1]
        elif result.errors and result.errors[-1][0] == self:
            last_failure = result.errors[-1]

        if last_failure:
            failed = True

        if failed:
            artifact_dir = 'playwright-artifact'
            os.makedirs(artifact_dir, exist_ok=True)

            filename = f'{self.__class__.__name__}.{self._testMethodName}_retry0.zip'
            self.context.tracing.stop(path=os.path.join(artifact_dir, filename))
        else:
            self.context.tracing.stop()

        self.browser.close()
        self.playwright.stop()
        super().tearDown()

    def _location(self, url):
        self.page.goto(url, wait_until='load')

    def _login(self):
        self._location(self.live_server_url + reverse('moneybook:login'))
        self.page.fill('#id_username', self.username)
        self.page.fill('#id_password', self.password)
        self.page.click('.btn-green')

    def _assert_common(self):
        # アプリ名
        self.assertEqual(self.page.inner_text('.header-cont1'), 'test-MoneyBook')
        # 名前表示
        header_cont2_text = self.page.inner_text('.header-cont2')
        self.assertTrue(self.username + 'さん' in header_cont2_text, header_cont2_text)

        # タスクバー
        expects = [
            {'href': reverse('moneybook:index'), 'text': 'ホーム'},
            {'href': reverse('moneybook:add'), 'text': '追加'},
            {'href': reverse('moneybook:statistics'), 'text': '統計'},
            {'href': reverse('moneybook:search'), 'text': '検索'},
            {'href': reverse('moneybook:tools'), 'text': 'ツール'}
        ]
        links = self.page.locator('nav.task_bar > ul > li > a').all()
        self.assertEqual(len(links), len(expects))
        for i in range(len(links)):
            with self.subTest(i=i):
                href = links[i].get_attribute('href')
                self.assertEqual(href, self.live_server_url + expects[i]['href'])
                self.assertEqual(links[i].inner_text(), expects[i]['text'])

    def _assert_texts(self, actual_elements, expects):
        self.assertEqual(len(actual_elements), len(expects))
        for i in range(len(actual_elements)):
            with self.subTest(i=i):
                self.assertEqual(actual_elements[i].inner_text(), expects[i])
