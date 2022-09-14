from authentication.tests.factories import UserFactory
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from inventory.tests.helpers import get_chrome_driver, chrome_set_value


class LoginTest(LiveServerTestCase):
    def setUp(self):
        self.browser = get_chrome_driver()
        # options = Options()
        # options.add_argument("--headless")
        # options.add_argument("--disable-gpu")
        # self.browser = webdriver.Chrome(options=options)

    def test_login_page_load(self):
        self.browser.get(f"{self.live_server_url}/")
        self.assertEqual(
            self.browser.current_url,
            f"{self.live_server_url}{reverse('authentication:login')}?next=/",
        )
        self.assertIsNone(
            self.browser.get_cookie("sessionid"),
            msg="sessionid exists in cookies before authenticating!",
        )

    def test_login_valid_credentials(self):
        password = "PA$$w0rd"
        user = UserFactory(password=password)
        self.browser.get(f"{self.live_server_url}/")

        chrome_set_value(self.browser, (By.NAME, "username"), user.username)
        chrome_set_value(self.browser, (By.NAME, "password"), password)

        submit_button = self.browser.find_element(by=By.ID, value="submit_button")
        submit_button.click()

        self.assertIsNotNone(
            self.browser.get_cookie("sessionid"),
            msg="Session failed to be created during login with valid credentials!",
        )
        self.assertEqual(self.browser.current_url, f"{self.live_server_url}/")
        self.browser.close()

    def test_login_invalid_credentials(self):
        user = UserFactory(password="correct_password!")
        self.browser.get(f"{self.live_server_url}/")

        chrome_set_value(self.browser, (By.NAME, "username"), user.username)
        chrome_set_value(self.browser, (By.NAME, "password"), "wrong_password!")

        submit_button = self.browser.find_element(by=By.ID, value="submit_button")
        submit_button.click()
        self.assertIsNone(
            self.browser.get_cookie("sessionid"),
            msg="Session was created during login with invalid credentials!",
        )
        self.assertEqual(
            self.browser.current_url, f"{self.live_server_url}/accounts/login/"
        )
        self.browser.close()
