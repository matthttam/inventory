from django.http import HttpResponse
from django.test import SimpleTestCase
from django.template import Context, Template
from bs4 import BeautifulSoup
from unittest.mock import MagicMock, Mock


# class TableTest(SimpleTestCase):
#    def setUp(self):
#        context = Context({})
#        self.template = Template("{% include 'partials/table.html' %}")
#        self.rendered = self.template.render(context)
#
