from django.urls import reverse
from playwright.sync_api import expect
from moneybook.playwright.base import PlaywrightBase


class Login(PlaywrightBase):
    def _assert_login_success(self):
        # ログインできたらトップに移動
        expect(self.page).to_have_url(self.live_server_url + reverse('moneybook:index'))
        # 名前表示
        expect(self.page.locator('.header-cont2')).to_contain_text(self.username + 'さん')

    def test_login_button(self):
        self._login()
        self._assert_login_success()

    def test_login_enter_username(self):
        self._location(self.live_server_url + reverse('moneybook:login'))
        self.page.fill('#id_username', self.username)
        self.page.fill('#id_password', self.password)
        self.page.press('#id_username', 'Enter')
        self._assert_login_success()

    def test_login_enter_password(self):
        self._location(self.live_server_url + reverse('moneybook:login'))
        self.page.fill('#id_username', self.username)
        self.page.fill('#id_password', self.password)
        self.page.press('#id_password', 'Enter')
        self._assert_login_success()
