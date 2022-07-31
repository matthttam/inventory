from django.test import TestCase

from unittest.mock import MagicMock, Mock, create_autospec, patch

from django.urls import reverse

from inventory.utils import (
    get_history_table_context,
    get_permitted_actions,
    get_reverse_placeholder,
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

    def test_get_reverse_placeholder_with_default_placeholder(self):
        # Default placeholder
        path = get_reverse_placeholder("assignments:detail")
        self.assertEqual(path, "/assignments/__id_placeholder__/")

    def test_get_reverse_placeholder_with_placeholder(self):
        # Modified placeholder
        path = get_reverse_placeholder("assignments:detail", "~placeholder~")
        self.assertEqual(path, "/assignments/~placeholder~/")

    @patch("inventory.utils.get_reverse_placeholder")
    def test_get_permitted_actions_with_default_action_list(
        self, mock_reverse_placeholder
    ):
        expected_result = {
            "view": {"allowed": True, "path": "url1"},
            "change": {"allowed": True, "path": "url2"},
            "delete": {"allowed": True, "path": "url3"},
        }
        # mock_request = Mock(**{"request.user.has_perm.side_effect": [True, True, True]})
        mock_request = Mock()
        mock_request.user.has_perm.return_value = True
        mock_reverse_placeholder.side_effect = ["url1", "url2", "url3"]
        result = get_permitted_actions(mock_request, "app_name", "model_name")
        self.assertEqual(result, expected_result)

    @patch("inventory.utils.get_reverse_placeholder")
    def test_get_permitted_actions_with_default_action_list(
        self, mock_reverse_placeholder
    ):
        expected_result = {
            "jump": {"allowed": True, "path": "url1"},
            "duck": {"allowed": True, "path": "url2"},
        }
        # mock_request = Mock(**{"request.user.has_perm.side_effect": [True, True, True]})
        mock_request = Mock()
        mock_request.user.has_perm.return_value = True
        mock_reverse_placeholder.side_effect = ["url1", "url2", "url3"]
        result = get_permitted_actions(
            mock_request,
            "app_name",
            "model_name",
            [("jump", "detail"), ("duck", "delete")],
        )
        self.assertEqual(result, expected_result)

    @patch("inventory.utils.get_reverse_placeholder")
    def test_get_permitted_actions_with_no_permissions(self, mock_reverse_placeholder):
        expected_result = {
            "view": {"allowed": False, "path": "url1"},
            "change": {"allowed": False, "path": "url2"},
            "delete": {"allowed": False, "path": "url3"},
        }
        # mock_request = Mock(**{"request.user.has_perm.side_effect": [True, True, True]})
        mock_request = Mock()
        mock_request.user.has_perm.return_value = False
        mock_reverse_placeholder.side_effect = ["url1", "url2", "url3"]
        result = get_permitted_actions(
            mock_request,
            "app_name",
            "model_name",
        )
        self.assertEqual(result, expected_result)
