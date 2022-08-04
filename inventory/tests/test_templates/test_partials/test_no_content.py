from django.test import SimpleTestCase
from django.template import Context, Template
from bs4 import BeautifulSoup


class NoContentTest(SimpleTestCase):
    def test_default_message(self):
        context = Context({})
        template = Template("{% include 'partials/no_content.html' %}")
        rendered = template.render(context)
        soup = BeautifulSoup(rendered, "html.parser")

        display = soup.select("h1")
        self.assertEqual(len(display), 1)
        self.assertInHTML(display[0].contents[0], "No Content To Display")

    def test_message(self):
        context = Context({"message": "Different Message"})
        template = Template("{% include 'partials/no_content.html' %}")
        rendered = template.render(context)
        soup = BeautifulSoup(rendered, "html.parser")
        display = soup.select("h1")
        self.assertEqual(len(display), 1)
        self.assertInHTML(display[0].contents[0], "Different Message")
