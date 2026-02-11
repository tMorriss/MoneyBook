from django.urls import reverse
from moneybook.e2e.base import SeleniumBase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Login(SeleniumBase):
    def test_login_button(self):
        self._login()

        # ログインできたらトップに移動
        self.assertEqual(self.driver.current_url, self.live_server_url + reverse('moneybook:index'))
        # 名前表示
        self.assertTrue(self.username + "さん" in self.driver.find_element(By.CLASS_NAME, "header-cont2").text,
                        self.driver.find_element(By.CLASS_NAME, "header-cont2").text)

    def test_login_enter_username(self):
        self._location(self.live_server_url + reverse('moneybook:login'))
        username_input = self.driver.find_element(By.ID, 'id_username')
        username_input.send_keys(self.username)
        password_input = self.driver.find_element(By.ID, 'id_password')
        password_input.send_keys(self.password)
        username_input.send_keys(Keys.RETURN)

        # ログインできたらトップに移動
        self.assertEqual(self.driver.current_url, self.live_server_url + reverse('moneybook:index'))
        # 名前表示
        self.assertTrue(self.username + "さん" in self.driver.find_element(By.CLASS_NAME, "header-cont2").text,
                        self.driver.find_element(By.CLASS_NAME, "header-cont2").text)

    def test_login_enter_password(self):
        self._location(self.live_server_url + reverse('moneybook:login'))
        username_input = self.driver.find_element(By.ID, 'id_username')
        username_input.send_keys(self.username)
        password_input = self.driver.find_element(By.ID, 'id_password')
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.RETURN)

        # ログインできたらトップに移動
        self.assertEqual(self.driver.current_url, self.live_server_url + reverse('moneybook:index'))
        # 名前表示
        self.assertTrue(self.username + "さん" in self.driver.find_element(By.CLASS_NAME, "header-cont2").text,
                        self.driver.find_element(By.CLASS_NAME, "header-cont2").text)
