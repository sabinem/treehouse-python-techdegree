"""
Tests for the main dialog
"""
import unittest
from unittest.mock import patch
patch.object = patch.object

from worklogdb.worklog.main_dialog import MainDialog
from worklogdb.worklog.create_dialog import CreateDialog
from worklogdb.worklog.search_dialog import SearchDialog


class TestMainDialog(unittest.TestCase):
    """
    The main dialog is the entry point to the application
    """
    def setUp(self):
        """
        the main dialog is started
        """
        self.dialog = MainDialog()

    def test_main_get_menu(self):
        """
        the menu should know the two option 'b' for back and 'q' for quit
        """
        menu = self.dialog.get_menu()
        self.assertIn('s', menu)
        self.assertIn('q', menu)
        self.assertIn('c', menu)

    @patch.object(SearchDialog, 'main')
    @patch.object(SearchDialog, '__init__')
    def test_main_search(self, mock_dialog_start, mock_dialog_main):
        """
        the search dialog can be called
        """
        mock_dialog_start.return_value = None
        self.dialog.search()
        mock_dialog_start.assert_called_once_with()
        mock_dialog_main.assert_called_once_with()

    @patch.object(CreateDialog, 'main')
    @patch.object(CreateDialog, '__init__')
    def test_main_create(self, mock_dialog_start, mock_dialog_main):
        """
        the create dialog can be called
        when a messages comes back the main dialog will pick it up
        """
        mock_dialog_start.return_value = None
        mock_dialog_main.return_value = "some message"
        self.dialog.create()
        mock_dialog_start.assert_called_once_with()
        mock_dialog_main.assert_called_once_with()
        self.assertEqual(self.dialog.msg, "some message")
