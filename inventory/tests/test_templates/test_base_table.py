from django.test import SimpleTestCase
from django.template import Context, Template
from bs4 import BeautifulSoup


class BaseTableTest(SimpleTestCase):
    def setUp(self):
        context = Context({})
        template = Template("{% include 'base_table.html' %}")
        self.rendered = template.render(context)
        self.assertNotIn("<h1>test</h1>", self.rendered)

    def test_block_tbody(self):
        parent_template_context = Context()
        parent_template_template = Template(
            "{% extends 'base_table.html' %}{% block tbody %}<h1>test</h1>{% endblock %}"
        )
        rendered = parent_template_template.render(parent_template_context)
        self.assertInHTML("<tbody><h1>test</h1></tbody>", rendered)

    def test_block_thead(self):
        parent_template_context = Context()
        parent_template_template = Template(
            "{% extends 'base_table.html' %}{% block thead %}<h1>test</h1>{% endblock %}"
        )
        rendered = parent_template_template.render(parent_template_context)
        self.assertInHTML("<thead><h1>test</h1></thead>", rendered)

    def test_without_headers(self):
        context = Context({})
        template = Template("{% include 'base_table.html' %}")
        rendered = template.render(context)
        self.assertInHTML("<thead>No Headers Provided for Template</thead>", rendered)

    def test_with_headers(self):
        context = Context({"headers": ["a", "b", "c"]})
        template = Template("{% include 'base_table.html' %}")
        rendered = template.render(context)
        self.assertInHTML("<thead><th>a</th><th>b</th><th>c</th></thead>", rendered)

    def test_block_table_id(self):
        parent_template_context = Context()
        parent_template_template = Template(
            "{% extends 'base_table.html' %}{% block table_id %}test_id{% endblock %}"
        )
        rendered = parent_template_template.render(parent_template_context)
        soup = BeautifulSoup(rendered, "html.parser")
        tables_by_id = soup.select("#test_id")
        self.assertEqual(len(tables_by_id), 1)

    def test_block_table_class(self):
        parent_template_context = Context()
        parent_template_template = Template(
            "{% extends 'base_table.html' %}{% block table_class %}no_class{% endblock %}"
        )
        rendered = parent_template_template.render(parent_template_context)
        soup = BeautifulSoup(rendered, "html.parser")
        tables_by_id = soup.select("table.no_class")
        self.assertEqual(len(tables_by_id), 1)

    def test_block_table_style(self):
        parent_template_context = Context()
        parent_template_template = Template(
            "{% extends 'base_table.html' %}{% block table_style %}text-align:top{% endblock %}"
        )
        rendered = parent_template_template.render(parent_template_context)
        soup = BeautifulSoup(rendered, "html.parser")
        tables_by_id = soup.select('table[style="text-align:top"]')
        self.assertEqual(len(tables_by_id), 1)
