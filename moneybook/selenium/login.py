from django.urls import reverse
from moneybook.selenium.base import SeleniumBase

from selenium.webdriver.common.keys import Keys


class Login(SeleniumBase):
    def test_login_button(self):
        self.driver.get(self.live_server_url + reverse('moneybook:login'))
        username_input = self.driver.find_element_by_id('id_username')
        username_input.send_keys(self.username)
        password_input = self.driver.find_element_by_id('id_password')
        password_input.send_keys(self.password)
        self.driver.find_element_by_class_name('btn-apply').click()

        # ログインできたらトップに移動
        self.assertEqual(self.driver.current_url, self.live_server_url + reverse('moneybook:index'))
        # 名前表示
        self.assertTrue(self.username + "さん" in self.driver.find_element_by_class_name("header-cont2").text,
                        self.driver.find_element_by_class_name("header-cont2").text)

    def test_login_enter_username(self):
        self.driver.get(self.live_server_url + reverse('moneybook:login'))
        username_input = self.driver.find_element_by_id('id_username')
        username_input.send_keys(self.username)
        password_input = self.driver.find_element_by_id('id_password')
        password_input.send_keys(self.password)
        username_input.send_keys(Keys.RETURN)

        # ログインできたらトップに移動
        self.assertEqual(self.driver.current_url, self.live_server_url + reverse('moneybook:index'))
        # 名前表示
        self.assertTrue(self.username + "さん" in self.driver.find_element_by_class_name("header-cont2").text,
                        self.driver.find_element_by_class_name("header-cont2").text)

    def test_login_enter_password(self):
        self.driver.get(self.live_server_url + reverse('moneybook:login'))
        username_input = self.driver.find_element_by_id('id_username')
        username_input.send_keys(self.username)
        password_input = self.driver.find_element_by_id('id_password')
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.RETURN)

        # ログインできたらトップに移動
        self.assertEqual(self.driver.current_url, self.live_server_url + reverse('moneybook:index'))
        # 名前表示
        self.assertTrue(self.username + "さん" in self.driver.find_element_by_class_name("header-cont2").text,
                        self.driver.find_element_by_class_name("header-cont2").text)
