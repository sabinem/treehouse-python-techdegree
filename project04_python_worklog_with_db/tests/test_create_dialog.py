"""
Tests for the Create Dialog
"""
import unittest

from playhouse.test_utils import test_database

from worklogdb.worklog.models import LogEntry, Employee
from worklogdb.worklog.create_dialog import CreateDialog
from tests.testdata import TestWithData, test_db


class TestCreateDialogSetUp(unittest.TestCase):
    """
    Tests of the dialogs setup
    """
    def setUp(self):
        self.dialog = CreateDialog()

    def test_create_init(self):
        """
        dialog title is set
        """
        self.assertIsNotNone(self.dialog.title)


class TestCreateDialogCreate(TestWithData):
    """
    Tests after build of temporary logentry
    """
    def run(self, result=None):
        with test_database(test_db, (Employee, LogEntry)):
            super(TestCreateDialogCreate, self).run(result)

    def setUp(self):
        """
        Szenario: temporary logentry has been build.
        the user can now decide what to do with it.
        """
        self.create_test_data()
        self.dialog = CreateDialog()
        employee = Employee.select().get()
        self.dialog.logentry_tmp = {
            'task': "some exotic task",
            'time_spent': 20,
            'note': "some note",
            'employee': employee,
        }

    def test_create_save_logentry(self):
        """
        logentry is saved
        """
        self.dialog.save_logentry()
        self.assertTrue(self.dialog.quit_dialog)
        self.assertIsNotNone(self.dialog.return_msg)
        self.assertTrue(LogEntry.select(LogEntry.task == "some exotic task").exists())
