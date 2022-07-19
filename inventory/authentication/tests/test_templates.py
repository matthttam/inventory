from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from playwright.sync_api import sync_playwright
import os
from authentication.tests.factories import UserFactory
from django.contrib import auth
from inventory.tests.web_browser import WebBrowser


class LoginFormTest(StaticLiveServerTestCase):
    # @classmethod
    # def setUpClass(cls):
    #    cls.web_browser = WebBrowser()
    # os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    # super().setUpClass()
    # cls.playwright = sync_playwright().start()
    # cls.browser = cls.playwright.webkit.launch()

    # @classmethod
    # def tearDownClass(cls):
    #    cls.web_browser.close()
    # super().tearDownClass()
    # cls.browser.close()
    # cls.playwright.stop()

    def setUp(self):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        self.web_browser = WebBrowser()
        self.addCleanup(self.web_browser.close)

    def test_login_invalid_credentials(self):
        page = self.web_browser.browser.new_page()
        page.goto(f"{self.live_server_url}/")
        page.fill("[name=username]", "myuser")
        page.fill("[name=password]", "secret")
        page.click("id=submit_button")
        self.assertInHTML(
            "Your username and password didn't match. Please try again.", page.content()
        )
        storage_state = page.context.storage_state()

        cookie_names = [c.get("name") for c in storage_state.get("cookies")]
        self.assertNotIn("sessionid", cookie_names)
        self.assertEqual(
            page.url, f"{self.live_server_url}{reverse('authentication:login')}"
        )
        page.close()

    def test_login_valid_credentials(self):
        password = "PA$$w0rd"
        user = UserFactory(password=password)
        page = self.web_browser.browser.new_page()
        page.goto(f"{self.live_server_url}/")
        self.assertEqual(
            page.url, f"{self.live_server_url}{reverse('authentication:login')}?next=/"
        )
        page.fill("[name=username]", user.username)
        page.fill("[name=password]", password)
        page.click("id=submit_button")

        self.assertNotIn(
            "Your username and password didn't match. Please try again.", page.content()
        )
        storage_state = page.context.storage_state()
        self.assertIn("cookies", storage_state.keys())
        cookie_names = [c["name"] for c in storage_state["cookies"]]
        self.assertIn("sessionid", cookie_names)
        self.assertEqual(page.url, f"{self.live_server_url}/")
        page.close()


#
#    with sync_playwright() as p:
#        browser = p.webkit.launch()
#        page = browser.new_page()
#        username = page.locator("#id_username")
#        password = page.locator("#id_password")
#        page.goto("http://127.0.0.1:8000/")
#        print(page.title())
#        browser.close()

## submit = selenium.find_element(By.ID, "submit_button")
## username.send_keys("fake_username")
## password.send_keys("fake_password")
## submit.send_keys(Keys.RETURN)
# self.assertInHTML(
#    "Your username and password didn't match. Please try again.",
#    selenium.page_source,
# )
# selenium.close()


# with sync_playwright() as p:
#    browser = p.webkit.launch()
#    page = browser.new_page()
#    page.goto("http://whatsmyuseragent.org/")
#    page.screenshot(path="example.png")
#    browser.close()

# with sync_playwright() as p:
#    browser = p.webkit.launch()
#    page = browser.new_page()
#    page.goto("http://playwright.dev")
#    print(page.title())
#    browser.close()

# with sync_playwright() as p:
#    browser = p.firefox.launch()
#    page = browser.new_page()
#    page.goto("http://playwright.dev")
#    print(page.title())
#    browser.close()

# with sync_playwright() as p:
#    browser = p.chromium.launch()
#    page = browser.new_page()
#    page.goto("http://playwright.dev")
#    print(page.title())
#    browser.close()
## with sync_playwright() as p:
##    browser = p.firefox.launch()
#    page = browser.new_page()
#    # page.goto("http://127.0.0.1:8000/")
#    # print(page.title())
#    browser.close()
#
# def test_example_is_working(page):
#    page.goto("https://example.com")
#    assert page.inner_text("h1") == "Example Domain"
#    page.click("text=More information")


# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.service import Service

# from chromedriver_py import binary_path
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# import chromedriver_binary

# import chromedriver_binary

# Create your tests here.
# class LoginFormTest(StaticLiveServerTestCase):
#    def testFormInvalidCredentials(self):
#        ## Setup chrome options
#        # chrome_options.add_argument("")
#        # binary_path = "/usr/bin/google-chrome-beta"
#        # service_object = Service(binary_path)
#        # selenium = webdriver.Chrome(service=service_object, options=chrome_options)
#        self.assertTrue(True)
#        # chrome_options = Options()
#        chrome_options = webdriver.ChromeOptions()
#        chrome_options.add_argument("--headless")  # Ensure GUI is off
#        chrome_options.add_argument("--window-size=1920,1200")
#        chrome_options.add_argument("--disable-dev-shm-usage")
#        chrome_options.add_argument("--no-sandbox")
#        chrome_options.add_argument("--no-proxy-server")
#        chrome_options.add_argument("--proxy-server='direct://'")
#        chrome_options.add_argument("--proxy-bypass-list=*")
#        selenium = webdriver.Chrome(options=chrome_options)
#        # selenium.get("http://127.0.0.1:8000/")
#        ## username = selenium.find_element(By.ID, "id_username")
#        ## password = selenium.find_element(By.ID, "id_password")
#        ## submit = selenium.find_element(By.ID, "submit_button")
#        ## username.send_keys("fake_username")
#        ## password.send_keys("fake_password")
#        ## submit.send_keys(Keys.RETURN)
#        # self.assertInHTML(
#        #    "Your username and password didn't match. Please try again.",
#        #    selenium.page_source,
#        # )
#        # selenium.close()
#
