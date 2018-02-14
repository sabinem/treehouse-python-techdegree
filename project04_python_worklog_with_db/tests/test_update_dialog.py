"""
Tests for the Update Dialog
"""
import sys
import unittest

from playhouse.test_utils import test_database

from worklogdb.worklog.models import LogEntry, Employee
from worklogdb.worklog.update_dialog import UpdateDialog
from worklogdb.worklog.helpers import _print_logentry_tmp
from tests.testdata import TestWithData, test_db


class TestUpdateDialogSetUp(unittest.TestCase):
    """
    Tests of dialog setup
    """
    def setUp(self):
        """
        a logentry is fetch from the parameters
        """
        self.logentry = "some logentry"
        data = {'logentry': self.logentry}
        self.dialog = UpdateDialog(**data)

    def test_update_init(self):
        """
        the title is set and the logentry is found
        """
        self.assertIsNotNone(self.dialog.title)
        self.assertEqual(self.dialog.logentry, self.logentry)

    def test_update_get_first_dialogstep(self):
        """
        prepares dialog for get name
        """
        first_dialogstep = self.dialog.get_first_dialogstep()
        self.assertEqual(first_dialogstep.checkinput_func, self.dialog.get_name)
        self.assertIsNotNone(first_dialogstep.prompt)

    def test_update_prepare_get_task(self):
        """
        prepares dialog for get task
        """
        self.dialog.prepare_get_task()
        self.assertEqual(self.dialog.activestep.checkinput_func, self.dialog.get_task)
        self.assertIsNotNone(self.dialog.activestep.prompt)

    def test_update_prepare_get_time_spent(self):
        """
        prepares dialog for get time spent
        """
        self.dialog.prepare_get_time_spent()
        self.assertEqual(self.dialog.activestep.checkinput_func, self.dialog.get_time_spent)
        self.assertIsNotNone(self.dialog.activestep.prompt)

    def test_update_prepare_get_note(self):
        """
        prepares dialog for get note
        """
        self.dialog.prepare_get_note()
        self.assertEqual(self.dialog.activestep.checkinput_func, self.dialog.ask_for_note_update)
        self.assertIsNotNone(self.dialog.activestep.prompt)

    def test_update_prepare_note_change(self):
        """
        prepares dialog for get note
        """
        self.dialog.prepare_note_change()
        self.assertEqual(self.dialog.activestep.checkinput_func, self.dialog.get_note)
        self.assertEqual(self.dialog.activestep.input_method, sys.stdin.read)
        self.assertIsNotNone(self.dialog.activestep.prompt)


class TestUpdateDialogUpdate(TestWithData):
    """
    Tests after build of temporary logentry
    """
    def run(self, result=None):
        with test_database(test_db, (Employee, LogEntry)):
            super(TestUpdateDialogUpdate, self).run(result)

    def setUp(self):
        """
        Szenario: temporary logentry has been build.
        the user can now decide what to do with it.
        """
        self.create_test_data()
        self.logentry = LogEntry.select().get()
        data = {'logentry': self.logentry}
        self.dialog = UpdateDialog(**data)
        self.employee = Employee.select().get()
        self.dialog.logentry_tmp = {
            'task': "some exotic task",
            'time_spent': 20,
            'note': "some note",
            'employee': self.employee,
        }
        self.print_stack = ['some item']
        self.print_logentries = _print_logentry_tmp(self.dialog.logentry_tmp, self.logentry)

    def test_update_save_logentry(self):
        """
        logentry is saved with the updated values
        """
        self.dialog.save_logentry()
        updated_logentry = LogEntry.get(LogEntry.id == self.logentry.id)
        self.assertEqual(updated_logentry.employee, self.employee)
        self.assertEqual(updated_logentry.task, "some exotic task")
        self.assertEqual(updated_logentry.time_spent, 20)
        self.assertEqual(updated_logentry.note, "some note")
        self.assertEqual(updated_logentry.logdate, self.logentry.logdate)

    def test_update_get_name_accept(self):
        """
        if the user accepts the given name, the old value is taken
        """
        func = self.dialog.get_name("a")
        self.assertEqual(self.dialog.logentry_tmp['employee'], self.logentry.employee)
        self.assertEqual(func, self.dialog.prepare_get_task)

    def test_update_get_name_change(self):
        """
        if the user enters a new name, he receives a list of employees with that name
        to chose from
        """
        func = self.dialog.get_name("sabine")
        self.assertTrue(self.dialog.choice)
        self.assertIsNotNone(self.dialog.choice_list)

    def test_update_get_task_accept(self):
        """
        if the user accepts the given task, the old value is taken
        """
        func = self.dialog.get_task("a")
        self.assertEqual(self.dialog.logentry_tmp['task'], self.logentry.task)
        self.assertEqual(func, self.dialog.prepare_get_time_spent)

    def test_update_get_task_change(self):
        """
        if the user enters a new value, the new value is taken
        """
        func = self.dialog.get_task("some task")
        self.assertEqual(self.dialog.logentry_tmp['task'], "some task")
        self.assertEqual(func, self.dialog.prepare_get_time_spent)

    def test_update_get_time_spent_accept(self):
        """
        if the user accepts the given task, the old value is taken
        """
        func = self.dialog.get_time_spent("a")
        self.assertEqual(self.dialog.logentry_tmp['time_spent'], self.logentry.time_spent)
        self.assertEqual(func, self.dialog.prepare_get_note)

    def test_update_get_time_spent_change(self):
        """
        if the user enters a new value, the new value is taken
        """
        func = self.dialog.get_time_spent("45")
        self.assertEqual(self.dialog.logentry_tmp['time_spent'], 45)
        self.assertEqual(func, self.dialog.prepare_get_note)

    def test_update_ask_for_note_update_accept(self):
        """
        if the user accepts the given note, the old value is taken
        """
        func = self.dialog.ask_for_note_update("a")
        self.assertEqual(self.dialog.logentry_tmp['note'], self.logentry.note)
        self.assertEqual(func, self.dialog.prepare_confirm)

    def test_update_ask_for_note_update_change(self):
        """
        if the user wants to change the note, his edit is prepared
        """
        func = self.dialog.ask_for_note_update("c")
        self.assertEqual(func, self.dialog.prepare_note_change)

    def test_update_ask_for_note_update_unvalid(self):
        """
        if the user wants to change the note, his edit is prepared
        """
        func = self.dialog.ask_for_note_update("x")
        self.assertIsNone(func)
        self.assertIsNotNone(self.dialog.msg)

    def test_update_add_to_print_stack_case_no_choice(self):
        """
        logentry_tmp is added to the stack for print out
        """
        self.dialog.choice = False
        self.dialog.add_to_print_stack(self.print_stack)
        self.assertEqual(self.print_stack[1], self.print_logentries)
        self.assertEqual(self.print_stack[0], 'some item')

    def test_update_add_to_print_stack_case_choice(self):
        """
        logentry_tmp is added to the stack for print out
        """
        self.dialog.choice = True
        self.dialog.add_to_print_stack(self.print_stack)
        self.assertListEqual(self.print_stack, self.print_stack)
