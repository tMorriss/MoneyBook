import os

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from playwright.sync_api import expect, sync_playwright


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
        self.page.set_default_timeout(60000)

    def tearDown(self):
        # 失敗時にトレースとスクリーンショットを保存する
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

            # スクリーンショット
            screenshot_path = os.path.join(artifact_dir, f'{self.__class__.__name__}.{self._testMethodName}_failure.png')
            self.page.screenshot(path=screenshot_path)

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
        # ログインボタンをクリック。遷移を待つ。
        self.page.click('input[value="ログイン"]')
        # ログイン成功の証拠（ログアウトリンクの存在）を待つ。タイムアウトはデフォルト(30s)
        self.page.wait_for_selector('a[href="' + reverse('moneybook:logout') + '"]')

    def _assert_common(self):
        # アプリ名
        expect(self.page.locator('body > header .header-cont1')).to_have_text(settings.APP_NAME)
        # 名前表示
        expect(self.page.locator('body > header .header-cont2')).to_contain_text(self.username + 'さん')

        # タスクバー
        expected_links = [
            {'href': reverse('moneybook:index'), 'text': 'ホーム'},
            {'href': reverse('moneybook:add'), 'text': '追加'},
            {'href': reverse('moneybook:statistics'), 'text': '統計'},
            {'href': reverse('moneybook:search'), 'text': '検索'},
            {'href': reverse('moneybook:tools'), 'text': 'ツール'}
        ]
        links = self.page.locator('nav.task_bar > ul > li > a')
        expect(links).to_have_count(len(expected_links))
        for i in range(len(expected_links)):
            expect(links.nth(i)).to_have_attribute('href', expected_links[i]['href'])
            expect(links.nth(i)).to_have_text(expected_links[i]['text'])

    def _assert_texts(self, actual_elements, expected_texts):
        # actual_elements が Locator の場合を想定
        expect(actual_elements).to_have_text(expected_texts)

    def _wait_for_ajax(self):
        # jQuery AJAXの完了を待つ
        # タイムアウトを少し長めにする
        self.page.wait_for_function('window.jQuery && window.jQuery.active == 0', timeout=20000)
