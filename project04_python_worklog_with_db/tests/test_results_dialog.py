"""
Tests for the Result Dialog
"""
from unittest.mock import patch
patch.object = patch.object

from playhouse.test_utils import test_database

from worklogdb.worklog.models import LogEntry, Employee
from worklogdb.worklog.result_dialog import ResultDialog
from worklogdb.worklog.update_dialog import UpdateDialog
from worklogdb.worklog.base_dialog import ChoiceList
from tests.testdata import TestWithData, test_db


class TestResultDialogBasic(TestWithData):
    """
    Simple tests for the result dialog, where the result could be any list
    """
    def setUp(self):
        """
        The dialog is called with the results in a list
        """
        searchresult = ChoiceList(list=['a', 'b', 'c', 'd', 'e', 'f'],
                                  name="abc")
        data = {"searchresult": searchresult}
        self.dialog = ResultDialog(**data)

    def test_result___init__(self):
        """
        the menus should be there_ one for list and one for details
        """
        self.assertIsNotNone(self.dialog.list_menu)
        self.assertIsNotNone(self.dialog.detail_menu)

    def test_result_show_list(self):
        """
        the list view is prepared correctly
        """
        self.dialog.show_list()
        self.assertTrue(self.dialog.choice)
        self.assertIsNone(self.dialog.active_choice_item)
        self.assertIsNone(self.dialog.active_choice_index)

    def test_result_show_previous_valid(self):
        """
        in the detail view: the previous record in the list is fetched
        """
        self.dialog.choice = False
        self.dialog.active_choice_index = 3
        self.dialog.show_previous()
        self.assertEqual(self.dialog.active_choice_index, 2)
        self.assertEqual(self.dialog.active_choice_item, 'c')

    def test_result_show_previous_start_of_list(self):
        """
        at the start of the list: previous is not possible any more
        """
        self.dialog.choice = False
        self.dialog.active_choice_index = 0
        self.dialog.show_previous()
        self.assertEqual(self.dialog.active_choice_index, 0)
        self.assertIsNotNone(self.dialog.msg)

    def test_result_show_next_valid(self):
        """
        in the detail view: the next record in the list is fetched
        """
        self.dialog.choice = False
        self.dialog.active_choice_index = 3
        self.dialog.show_next()
        self.assertEqual(self.dialog.active_choice_index, 4)
        self.assertEqual(self.dialog.active_choice_item, 'e')

    def test_result_show_next_end_of_list(self):
        """
        at the end of the list: next is not possible any more
        """
        self.dialog.choice = False
        self.dialog.active_choice_index = 5
        self.dialog.show_next()
        self.assertEqual(self.dialog.active_choice_index, 5)
        self.assertIsNotNone(self.dialog.msg)

    def test_result_get_menu(self):
        """
        the dialog starts with the list menu
        """
        menu = self.dialog.get_menu()
        self.assertEqual(menu, self.dialog.list_menu)

    def test_result_update_menu_case_choice_is_true(self):
        """
        when the list view is activated, the list menu is fetched
        """
        self.dialog.choice = True
        self.dialog.menu = self.dialog.detail_menu
        menu = self.dialog.update_menu()
        self.assertEqual(menu, self.dialog.list_menu)

    def test_result_update_menu_case_choice_is_false(self):
        """
        when the list view is deactivated, the detail menu is fetched
        """
        self.dialog.choice = False
        self.dialog.menu = self.dialog.list_menu
        menu = self.dialog.update_menu()
        self.assertEqual(menu, self.dialog.detail_menu)

    def test_result_prepare_delete(self):
        """
        delete is prepared, by setting the next step to call the
        delete confirm function
        """
        self.dialog.prepare_delete()
        self.assertEqual(self.dialog.activestep.checkinput_func, self.dialog.confirm_delete)


class TestResultDialogData(TestWithData):
    """
    Tests for the result dialog, that rely on database records:
    The update and delete method assume that the result list consists
    of logentries from the database
    """

    def run(self, result=None):
        with test_database(test_db, (Employee, LogEntry)):
            super(TestResultDialogData, self).run(result)

    def setUp(self):
        """
        a logentry has been chosen from the list, so the
        dialog is in detail view
        the list of the dialog consists of logentries
        """
        self.create_test_data()
        self.logentry_queryset = LogEntry.select()
        self.logentry_list = list(self.logentry_queryset)
        searchresult = ChoiceList(list=self.logentry_list,
                                  name="logentries")
        data = {"searchresult": searchresult}
        self.dialog = ResultDialog(**data)
        self.logentry = self.logentry_queryset.get()
        self.dialog.active_choice_item = self.logentry
        self.dialog.active_choice_index = self.dialog.choice_list.list.index(self.logentry)
        self.dialog.prepare_delete()

    def test_result___init__(self):
        """
        the result dialogs list should now be the list of logentried
        """
        self.assertEqual(self.dialog.choice_list.list, self.logentry_list)

    def test_result_confirm_delete_confirmed(self):
        """
        when the user confirms the delete, the record should disappear from
        both the result list and the database, the list view should be activated
        """
        func = self.dialog.confirm_delete("y")
        self.assertEqual(func, self.dialog.delete)

    def test_result_confirm_delete_rejected(self):
        """
        when the delete is rejected everything stays as is
        """
        func = self.dialog.confirm_delete("f")
        self.assertEqual(func, self.dialog.discard_delete)

    def test_result_confirm_delete_unvalid_choice(self):
        """
        when no valid chice is made, the user receives a message
        """
        func = self.dialog.confirm_delete("x")
        self.assertIsNotNone(self.dialog.msg)
        self.assertIsNone(func)

    def test_result_discard_delete(self):
        """
        when the delete is rejected everything stays as is
        """
        self.dialog.discard_delete()
        self.assertIsNone(self.dialog.activestep)
        self.assertIsNotNone(self.dialog.msg)
        self.assertTrue(LogEntry.select().where(LogEntry.id == self.logentry.id).exists())

    def test_result_delete(self):
        """
        when the delete is rejected everything stays as is
        """
        self.dialog.delete()
        self.assertTrue(self.dialog.choice)
        self.assertNotIn(self.logentry, self.dialog.choice_list.list)
        self.assertIsNotNone(self.dialog.msg)
        self.assertFalse(LogEntry.select().where(LogEntry.id == self.logentry.id).exists())
        self.assertIsNone(self.dialog.activestep)

    @patch.object(UpdateDialog, 'main')
    @patch.object(UpdateDialog, '__init__')
    def test_result_update(self, mock_init, mock_update):
        """
        the update dialog is called in case an update was requested
        """
        mock_init.return_value = None
        mock_update.return_value = "some message"
        data = {'logentry': self.logentry}
        self.dialog.update()
        mock_init.assert_called_once_with(**data)
        mock_update.assert_called_once_with()
        self.assertEqual(self.dialog.msg, "some message")
