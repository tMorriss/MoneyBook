from http import HTTPStatus

from django.urls import reverse
from moneybook.e2e.base import PlaywrightBase
from playwright.sync_api import expect


class Login(PlaywrightBase):
    def _assert_login_success(self):
        # ログイン成功の証拠（ログアウトボタンの存在）を待つ
        self.page.wait_for_selector('button.link-button:has-text("ログアウト")')
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


class Logout(PlaywrightBase):
    def test_logout(self):
        self._login()
        self.page.click('button.link-button:has-text("ログアウト")')
        # ログアウト後はログイン画面に遷移することを確認
        expect(self.page).to_have_url(self.live_server_url + reverse('moneybook:login'))

    def test_logout_csrf_failure(self):
        self._login()

        # CSRFトークンを削除してPOSTリクエストを送信する
        self.page.evaluate("""() => {
            const form = document.querySelector('form[action$="/logout"]');
            const csrfInput = form.querySelector('input[name="csrfmiddlewaretoken"]');
            if (csrfInput) {
                csrfInput.remove();
            }
        }""")

        # ログアウトボタンをクリック
        self.page.click('button.link-button:has-text("ログアウト")')

        # CSRF検証エラー（403 Forbidden）が発生することを確認
        # Djangoのデフォルトの403ページが表示されるはず
        expect(self.page.locator('body')).to_contain_text(str(HTTPStatus.FORBIDDEN.value))
