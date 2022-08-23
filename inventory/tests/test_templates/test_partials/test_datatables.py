from django.test import SimpleTestCase
from django.template import Context, Template
from bs4 import BeautifulSoup
from inventory.settings import STATIC_URL


class DatatablesTest(SimpleTestCase):
    def setUp(self) -> None:
        context = Context({})
        template = Template("{% include 'partials/datatables.html' %}")
        self.rendered = template.render(context)
        self.soup = BeautifulSoup(self.rendered, "html.parser")

    def test_css(self):
        datatables_css = self.soup.select(
            'link[href="https://cdn.datatables.net/v/bs5/jszip-2.5.0/dt-1.12.1/af-2.4.0/b-2.2.3/b-colvis-2.2.3/b-html5-2.2.3/b-print-2.2.3/cr-1.5.6/date-1.1.2/fc-4.1.0/fh-3.2.4/kt-2.7.0/r-2.3.0/rg-1.2.0/rr-1.2.8/sc-2.0.7/sb-1.3.4/sp-2.0.2/sl-1.4.0/sr-1.1.1/datatables.min.css"]'
        )
        self.assertEqual(len(datatables_css), 1)

    def test_javascript(self):
        pdfmake_js = self.soup.select(
            'script[src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.36/pdfmake.min.js"]'
        )
        vfx_fonts_js = self.soup.select(
            'script[src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.36/vfs_fonts.js"]'
        )
        datatables_js = self.soup.select(
            'script[src="https://cdn.datatables.net/v/bs5/jszip-2.5.0/dt-1.12.1/af-2.4.0/b-2.2.3/b-colvis-2.2.3/b-html5-2.2.3/b-print-2.2.3/cr-1.5.6/date-1.1.2/fc-4.1.0/fh-3.2.4/kt-2.7.0/r-2.3.0/rg-1.2.0/rr-1.2.8/sc-2.0.7/sb-1.3.4/sp-2.0.2/sl-1.4.0/sr-1.1.1/datatables.min.js"]'
        )
        static_inventory_datatable_defaults_js = self.soup.select(
            f'script[src="/{STATIC_URL}inventory/js/datatable_defaults.js"]'
        )

        self.assertEqual(len(pdfmake_js), 1)
        self.assertEqual(len(vfx_fonts_js), 1)
        self.assertEqual(len(datatables_js), 1)
        self.assertEqual(len(static_inventory_datatable_defaults_js), 1)
