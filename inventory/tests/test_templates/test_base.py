from django.test import SimpleTestCase
from django.template import Context, Template
from bs4 import BeautifulSoup
from sekizai.context import SekizaiContext


class BaseTest(SimpleTestCase):
    def setUp(self):
        context = SekizaiContext({})
        template = Template("{% include 'base.html' %}")
        self.rendered = template.render(context)
        self.soup = BeautifulSoup(self.rendered, "html.parser")

    def test_meta(self):
        self.assertInHTML(
            '<meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"/>',
            self.rendered,
        )

    def test_css(self):
        bootstrap_css = self.soup.select(
            'link[href="/static/inventory/css/bootstrap.min.css"]'
        )
        bootstrap_icons_css = self.soup.select(
            'link[href="/static/inventory/css/bootstrap-icons.css"]'
        )

        self.assertEqual(len(bootstrap_css), 1)
        self.assertEqual(len(bootstrap_icons_css), 1)

    def test_javascript(self):
        jquery_js = self.soup.select(
            'script[src="/static/inventory/js/jquery-3.6.0.min.js"]'
        )
        bootstrap_js = self.soup.select(
            'script[src="/static/inventory/js/bootstrap.bundle.min.js"]'
        )
        self.assertEqual(len(jquery_js), 1)
        self.assertEqual(len(bootstrap_js), 1)

    def test_title(self):
        title = self.soup.select_one("title").contents[0]
        self.assertEqual("Inventory", title)

    def test_with_content(self):
        parent_template_context = SekizaiContext()
        parent_template_template = Template(
            "{% extends 'base.html' %}{% block base_content %}<h1>test</h1>{% endblock %}"
        )
        rendered = parent_template_template.render(parent_template_context)
        self.assertInHTML("<h1>test</h1>", rendered)
