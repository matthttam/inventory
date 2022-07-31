from os import environ

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag
from django.urls import reverse

from authentication.tests.factories import UserFactory
from inventory.tests.web_browser import WebBrowser


class LoginFormTest(StaticLiveServerTestCase):
    def setUp(self):
        environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
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
