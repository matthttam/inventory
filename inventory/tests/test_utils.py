from django.test import TestCase

from unittest.mock import MagicMock, Mock, create_autospec, patch

from django.urls import reverse

from inventory.utils import (
    get_history_table_context,
    get_table_context,
)


class TestUtils(TestCase):
    def test_get_history_table_context(self):
        expected_outcome = {
            "test_id": {
                "id": "test_id",
                "headers": ["Date", "Actor", "Field", "From", "To"],
            }
        }
        context = get_history_table_context("test_id")
        self.assertEqual(context, expected_outcome)

    def test_get_table_context(self):
        expected_outcome = {
            "test_id": {
                "id": "test_id",
                "headers": ["a", "b", "c", "d", "e"],
            }
        }
        context = get_table_context("test_id", ["a", "b", "c", "d", "e"])
        self.assertEqual(context, expected_outcome)
