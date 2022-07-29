from django.test import TestCase

from unittest.mock import MagicMock, Mock, create_autospec, patch

from django.urls import reverse

from inventory.utils import (
    get_history_table_context,
    get_permitted_actions,
    get_table_context,
)


class TestGetHistoryTableContext(TestCase):
    def test_call(self):
        expected_outcome = {
            "test_id": {
                "id": "test_id",
                "headers": ["Date", "Actor", "Field", "From", "To"],
            }
        }
        context = get_history_table_context("test_id")
        self.assertEqual(context, expected_outcome)


class TestGetTableContext(TestCase):
    def test_call(self):
        expected_outcome = {
            "test_id": {
                "id": "test_id",
                "headers": ["a", "b", "c", "d", "e"],
            }
        }
        context = get_table_context("test_id", ["a", "b", "c", "d", "e"])
        self.assertEqual(context, expected_outcome)


# @patch.object(django.core.urlresolvers.reverse, "reverse")
# @patch("django.urls.reverse", Mock)


class TestGetPermittedActions(TestCase):
    @patch("inventory.utils.reverse")
    def test_call_default_action_list(self, mock_reverse):
        expected_result = {
            "view": {"allowed": True, "path": "url1"},
            "change": {"allowed": True, "path": "url2"},
            "delete": {"allowed": True, "path": "url13"},
        }
        # mock_request = Mock(**{"request.user.has_perm.side_effect": [True, True, True]})
        mock_request = Mock()
        mock_request.user.has_perm.return_value = True
        mock_reverse.side_effect = ["url_1", "url_2", "url_3"]
        result = get_permitted_actions(mock_request, "app_name", "model_name")
        self.assertEqual(result, expected_result)
