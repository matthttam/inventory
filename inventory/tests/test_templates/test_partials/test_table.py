from django.http import HttpResponse
from django.test import SimpleTestCase
from django.template import Context, Template
from bs4 import BeautifulSoup
from unittest.mock import MagicMock, Mock


class TableTest(SimpleTestCase):
    def setUp(self):
        context = Context({})
        template = Template("{% include 'partials/table.html' %}")
        self.rendered = template.render(context)
        # self.assertNotIn("<h1>test</h1>", self.rendered)

    def test_extends_base_table(self):
        # response = MagicMock(HttpResponse)
        # self.assertTemplateUsed(self.rendered, "base_table.html")
        print(dir(self.rendered))
        pass
        # self.assertTemplateUsed()
