from django.template import Context, Template
from django.test import SimpleTestCase
from bs4 import BeautifulSoup


class DashboardNavUserTest(SimpleTestCase):
    """Tests the nav profile partial template"""

    def setUp(self) -> None:
        self.template = Template('{% include "dashboard/partials/_top_nav.html" %}')
        self.context = Context({"user": {"profile": {"display_name": "test_name"}}})
        self.rendered = self.template.render(self.context)
        self.soup = BeautifulSoup(self.rendered, "html.parser")

    def test_brand(self):
        brand = self.soup.select_one("a.navbar-brand")
        self.assertEqual("/", brand.attrs.get("href"))
        self.assertInHTML("OPS Inventory", brand.text)

    def test_user_display_name(self):
        dropdown = self.soup.select_one("a#userDropdown")
        self.assertInHTML("test_name", dropdown.text)

    def test_profile_link(self):
        profile_links = self.soup.select('a[href="/profile/"]')
        self.assertEqual(len(profile_links), 1)
        self.assertInHTML("Settings", profile_links[0].text)

    def test_logout_link(self):
        logout_links = self.soup.select('a[href="/accounts/logout/"]')
        self.assertEqual(len(logout_links), 1)
        self.assertInHTML("Logout", logout_links[0].text)
