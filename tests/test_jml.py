import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from unittest.mock import patch
import pytest
from joiner import handle_joiner
from leaver import handle_leaver

FAKE_TOKEN = "fake-token"
FAKE_ID = "12345678-0000-0000-0000-000000000000"
DEPT_MAP = {"HR": ["grp-hr-001"], "Engineering": ["grp-eng-001"]}

class TestJoiner:
    @patch("joiner.add_to_group")
    @patch("joiner.create_user")
    def test_creates_user_and_assigns_group(self, mock_create, mock_add):
        mock_create.return_value = {"id": FAKE_ID}
        row = {"name": "Alice", "upn": "alice@demo.com", "department": "HR", "title": "Analyst"}
        result = handle_joiner(FAKE_TOKEN, row, DEPT_MAP)
        assert result == FAKE_ID
        assert mock_add.call_count == 1

class TestLeaver:
    @patch("leaver.remove_all_groups")
    @patch("leaver.revoke_sign_in_sessions")
    @patch("leaver.update_user")
    @patch("leaver.get_user_by_upn")
    def test_full_offboarding(self, mock_get, mock_update, mock_revoke, mock_remove):
        mock_get.return_value = {"id": FAKE_ID, "displayName": "Carol"}
        mock_remove.return_value = 1
        handle_leaver(FAKE_TOKEN, {"upn": "carol@demo.com"})
        mock_update.assert_called_once_with(FAKE_TOKEN, FAKE_ID, {"accountEnabled": False})
        mock_revoke.assert_called_once()
        mock_remove.assert_called_once()
