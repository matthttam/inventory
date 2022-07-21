from django.test import TestCase
from django.contrib.staticfiles import finders
from inventory.settings import STATIC_URL


class StaticFileAssignmentListJSTest(TestCase):
    def test_valid_path(self):
        abs_path = finders.find("assignments/assignment_list.js")
        self.assertIsNotNone(abs_path)

    def test_valid_lookup(self):
        response = self.client.get(f"{STATIC_URL}assignments/assignment_list.js")
        self.assertEqual(response.status_code, 302)
