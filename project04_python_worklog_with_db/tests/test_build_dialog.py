"""
Tests for the Build Dialog
"""
import unittest

from playhouse.test_utils import test_database

from worklogdb.worklog.models import LogEntry, Employee
from worklogdb.worklog.build_dialog import BuildDialog
from worklogdb.worklog.base_dialog import ChoiceList
from worklogdb.worklog.helpers import _print_logentry_tmp
from tests.testdata import TestWithData, test_db


class TestBuildDialogSetUp(unittest.TestCase):
    """
    Tests of dialog setup
    """
    def setUp(self):
        """
        The dialog is started
        """
        self.dialog = BuildDialog()

    def test_build_init(self):
        """
        a temporary logentry storage has been set up
        """
        self.assertEqual(self.dialog.logentry_tmp, {})

    def test_build_get_first_dialogstep(self):
        """
        next_function is set to get_name
        """
        first_dialogstep = self.dialog.get_first_dialogstep()
        self.assertEqual(first_dialogstep.checkinput_func, self.dialog.get_name)
        self.assertIsNotNone(first_dialogstep.prompt)


    def test_build_prepare_get_task(self):
        """
        next_function is set to get_task
        """
        self.dialog.prepare_get_task()
        self.assertEqual(self.dialog.activestep.checkinput_func, self.dialog.get_task)
        self.assertIsNotNone(self.dialog.activestep.prompt)


    def test_build_prepare_get_time_spent(self):
        """
        next_function is set to get_time_spent
        """
        self.dialog.prepare_get_time_spent()
        self.assertEqual(self.dialog.activestep.checkinput_func, self.dialog.get_time_spent)
        self.assertIsNotNone(self.dialog.activestep.prompt)


    def test_build_prepare_get_note(self):
        """
        next_function is set to get_note
        """
        self.dialog.prepare_get_note()
        self.assertEqual(self.dialog.activestep.checkinput_func, self.dialog.get_note)
        self.assertIsNotNone(self.dialog.activestep.prompt)

    def test_build_prepare_confirm(self):
        """
        next_function is set to confirm
        """
        self.dialog.prepare_confirm()
        self.assertEqual(self.dialog.activestep.checkinput_func, self.dialog.confirm)
        self.assertIsNotNone(self.dialog.activestep.prompt)


class TestBuildDialogGetFields(unittest.TestCase):
    """
    Test of field checks for userinput
    """
    def setUp(self):
        """
        The dialog is started
        """
        self.dialog = BuildDialog()

    def test_build_get_task_valid(self):
        """
        insert userinput as task into the temporary logentry,
        call preparation of next step
        """
        func = self.dialog.get_task("some task")
        self.assertEqual(self.dialog.logentry_tmp['task'], 'some task')
        self.assertEqual(func, self.dialog.prepare_get_time_spent)

    def test_build_get_task_unvalid(self):
        """
        if no task is given, give user a message and prompt him again
        """
        func = self.dialog.get_task("")
        self.assertIsNotNone(self.dialog.msg)
        self.assertFalse(hasattr(self.dialog.logentry_tmp, 'task'))
        self.assertIsNone(func)

    def test_build_get_time_spent_valid(self):
        """
        insert userinput as time spent into the temporary logentry,
        call preparation of next step
        """
        func = self.dialog.get_time_spent('45')
        self.assertEqual(self.dialog.logentry_tmp['time_spent'], 45)
        self.assertEqual(func, self.dialog.prepare_get_note)

    def test_build_get_time_spent_unvalid(self):
        """
        if no task is given, give user a message and prompt him again
        """
        func = self.dialog.get_time_spent("not a number")
        self.assertIsNotNone(self.dialog.msg)
        self.assertFalse(hasattr(self.dialog.logentry_tmp, 'time_spent'))
        self.assertIsNone(func)

    def test_build_get_note(self):
        """
        insert userinput as note into the temporary logentry,
        call preparation of next step
        """
        func = self.dialog.get_note('some note')
        self.assertEqual(self.dialog.logentry_tmp['note'], "some note")
        self.assertEqual(func, self.dialog.prepare_confirm)


    def test_build_confirm_save(self):
        """
        save is confirmed, next function: create
        """
        func = self.dialog.confirm('s')
        self.assertEqual(func, self.dialog.save_logentry)

    def test_build_confirm_discard(self):
        """
        save is confirmed, next function: create
        """
        func = self.dialog.confirm('d')
        self.assertEqual(func, self.dialog.discard_logentry)

    def test_build_confirm_unvalid(self):
        """
        save is confirmed, next function: create
        """
        func = self.dialog.confirm('x')
        self.assertIsNone(func)
        self.assertIsNotNone(self.dialog.msg)

    def test_build_save_logentry(self):
        """
        logentry is saved,
        this method will be overwirtten by the real create or save
        """
        self.dialog.save_logentry()
        self.assertTrue(self.dialog.quit_dialog)
        self.assertIsNotNone(self.dialog.return_msg)

    def test_build_discard_logentry(self):
        """
        logentry is discarded
        """
        self.dialog.discard_logentry()
        self.assertTrue(self.dialog.quit_dialog)
        self.assertIsNotNone(self.dialog.return_msg)


class TestBuildDialogChoiceEmployee(unittest.TestCase):
    """
    In the build process the employee is chosen from a list of employees
    """
    def setUp(self):
        """
        The dialog is started. A list of employees is set up, the user
        has chosen an employee by row number in the list
        """
        self.dialog = BuildDialog()
        self.dialog.active_choice_index = 1
        self.dialog.choice_list = ChoiceList(list = ['anna', 'peter', 'tom'])

    def test_build_choice_employee(self):
        """
        the employee has been transfered into the temporary storage,
        the next function is set: the dialogstep where the task is fetched.
        """
        func = self.dialog.choice_employee()
        self.assertEqual(self.dialog.logentry_tmp['employee'], 'peter')
        self.assertIsNone(self.dialog.active_choice_index)
        self.assertIsNone(self.dialog.active_choice_item)
        self.assertEqual(func, self.dialog.prepare_get_task)


class TestBuildDialogChooseEmployee(TestWithData):
    """
    Tests choosing the employee from a list fafter entering the name
    with real data. The testcases realte to the testdata.
    """
    def run(self, result=None):
        with test_database(test_db, (Employee, LogEntry)):
            super(TestBuildDialogChooseEmployee, self).run(result)

    def setUp(self):
        """
        the dialog has started, testdata is created
        """
        self.create_test_data()
        self.dialog = BuildDialog()

    def test_build_get_name_exists(self):
        """
        employee could be chosen from list
        """
        self.dialog.get_name('sabine')
        self.assertTrue(self.dialog.choice)
        self.assertIsNotNone(self.dialog.choice_list)
        self.assertIsNotNone(self.dialog.choice_list.list)
        self.assertEqual(self.dialog.choice_list.choice_func, self.dialog.choice_employee)
        self.assertEqual(self.dialog.choice_list.fmt_func, str)

    def test_build_get_name_does_not_exist(self):
        """
        no employee for that name esists
        """
        self.dialog.get_name('markus')
        self.assertFalse(self.dialog.choice)
        self.assertIsNotNone(self.dialog.msg)


class TestBuildDialogPrint(unittest.TestCase):
    """
    tests the print of the temporary logentry
    """
    def setUp(self):
        """
        The dialog is started
        """
        self.dialog = BuildDialog()
        self.dialog.menu = self.dialog.get_menu()
        self.logentry_tmp = {'task': 'some task'}
        self.dialog.logentry_tmp = self.logentry_tmp
        self.print_stack = ['some item']
        self.print_logentry_tmp = _print_logentry_tmp(self.logentry_tmp)

    def test_build_add_to_print_stack_case_no_choice(self):
        """
        logentry_tmp is added to the stack for print out
        """
        self.dialog.choice = False
        self.dialog.add_to_print_stack(self.print_stack)
        self.assertEqual(self.print_stack[1], self.print_logentry_tmp)
        self.assertEqual(self.print_stack[0], 'some item')

    def test_build_add_to_print_stack_case_choice(self):
        """
        logentry_tmp is added to the stack for print out
        """
        self.dialog.choice = True
        self.dialog.add_to_print_stack(self.print_stack)
        self.assertListEqual(self.print_stack, self.print_stack)
