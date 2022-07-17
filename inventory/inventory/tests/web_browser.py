from ast import Raise
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright
import os
from authentication.tests.factories import UserFactory
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse


class StateNotFound(Exception):
    """Raised when a WebBrowser does not have the requested named state"""

    def __init__(self, name, *args: object) -> None:
        self.message = f"State not found: {name}"
        super().__init__(self.message)

    pass


# Singleton WebBrowser for Testing
class WebBrowser(object):

    _storage_states: dict = {}

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)

        return cls.instance

    def __init__(self):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.webkit.launch()

    def close(self):
        self.browser.close()
        self.playwright.stop()

    def save_state(self, name, page):
        self._storage_states[name] = page.context.storage_state()

    def apply_state(self, name):
        storage_state = self._storage_states.get(name)
        if not storage_state:
            raise StateNotFound(name)
        self.browser.new_context(storage_state=storage_state)

    def login(self, page, live_server_url, user: User = None, password: str = None):
        if not user:
            password = "PA$$w0rd"
            user = UserFactory(password=password)
        page.goto(f"{live_server_url}{reverse('authentication:login')}")
        page.fill("[name=username]", user.username)
        page.fill("[name=password]", password)
        page.click("id=submit_button")
        self.save_state("authenticated", page)
