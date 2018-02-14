"""
Tests for the Search Dialog
"""
import datetime

from playhouse.test_utils import test_database
import unittest
from unittest.mock import patch
patch.object = patch.object

from worklogdb.worklog.models import LogEntry, Employee, _get_employee_from_name
from worklogdb.worklog.search_dialog import SearchDialog
from worklogdb.worklog.result_dialog import ResultDialog
from worklogdb.worklog.base_dialog import ChoiceList
from worklogdb.worklog.helpers import SearchParameters, _logentry_to_date
from tests.testdata import TestWithData, test_db


class SearchDialogSetUpTests(TestWithData):
    """
    tests the setup of the dialog and its basic methods
    """
    def setUp(self):
        """
        the search dialog is started
        """
        self.dialog = SearchDialog()

    def test_search_get_menu(self):
        """
        the menu should contain the search options
        """
        menu = self.dialog.get_menu()
        menu = self.dialog.get_menu()
        self.assertIn('w', menu)
        self.assertIn('t', menu)
        self.assertIn('d', menu)
        self.assertIn('e', menu)
        self.assertIn('b', menu)
        self.assertIn('q', menu)

    def test_search_init_new_search(self):
        """
        for a nwe search the search parameters and the result are deleted
        """
        self.dialog.search_parameters = "something"
        self.dialog.logentry_queryset = "some queryset"
        self.dialog.init_new_search()
        self.assertFalse(hasattr(self.dialog, 'search_parameters'))
        self.assertFalse(hasattr(self.dialog, 'logentry_queryset'))

    def test_search_search_by_term(self):
        """
        search by term menu option prepares for that search type
        """
        self.dialog.search_by_term()
        self.assertEqual(self.dialog.activestep.checkinput_func, self.dialog.check_term)

    def test_search_search_by_time_spent(self):
        """
        search by time spent menu option prepares for that search type
        """
        self.dialog.search_by_time_spent()
        self.assertEqual(self.dialog.activestep.checkinput_func, self.dialog.check_time_spent)

    def test_search_search_by_date(self):
        """
        search by date menu option prepares for that search type
        """
        self.dialog.search_by_date()
        self.assertEqual(self.dialog.activestep.checkinput_func, self.dialog.check_date)

    def test_search_search_by_employee(self):
        """
        search by employee menu option prepares for that search type
        """
        self.dialog.search_by_employee()
        self.assertEqual(self.dialog.activestep.checkinput_func, self.dialog.check_employee)


class TestSearchDialogQueries(TestWithData):
    """
    Tests queries of the search dialog
    """

    def run(self, result=None):
        with test_database(test_db, (Employee, LogEntry)):
            super(TestSearchDialogQueries, self).run(result)

    def setUp(self):
        """
        the database is filled with testdata. The logentry
        """
        self.create_test_data()
        self.dialog = SearchDialog()
        self.logentry_queryset = LogEntry.select()

    def test_search_query_by_term(self):
        searchterm = 'hard'
        self.dialog.search_parameters = SearchParameters(searchterm=searchterm)
        self.dialog.query_by_term()
        hits = [logentry for logentry in self.task_list
                if (searchterm in logentry.task or searchterm in logentry.note)]
        self.assertListEqual(list(self.dialog.logentry_queryset), hits)

    def test_search_query_by_employee(self):
        employee = Employee.select().get()
        tasks = LogEntry.select().where(LogEntry.employee_id == employee.id)
        self.dialog.search_parameters = SearchParameters(employee_id=employee.id)
        self.dialog.query_by_employee()
        self.assertEqual(tasks, self.dialog.logentry_queryset)

    def test_search_query_by_date_exact(self):
        self.dialog.search_parameters = SearchParameters(
            date_from=datetime.date(2016, 8, 30),
            date_to=None)
        self.dialog.query_by_date()
        hits = [logentry for logentry in self.task_list
                if logentry.logdate == datetime.date(2016, 8, 30)]
        self.assertSetEqual(set(hits), set(list(self.dialog.logentry_queryset)))

    def test_search_query_by_date_range(self):
        self.dialog.search_parameters = SearchParameters(
            date_from=datetime.date(2016, 8, 29),
            date_to=datetime.date(2016, 8, 30))
        self.dialog.query_by_date()
        hits = [logentry for logentry in self.task_list
                if datetime.date(2016, 8, 29) <= logentry.logdate <= datetime.date(2016, 8, 30)]
        self.assertSetEqual(set(hits), set(list(self.dialog.logentry_queryset)))

    def test_search_query_by_time_exact(self):
        self.dialog.search_parameters = SearchParameters(
            time_from=15,
            time_to=None)
        self.dialog.query_by_time_spent()
        hits = [logentry for logentry in self.task_list
                if (logentry.time_spent == 15)]
        self.assertEqual(hits, list(self.dialog.logentry_queryset))

    def test_search_query_by_time_range(self):
        self.dialog.search_parameters = SearchParameters(
            time_from=10,
            time_to=20)
        self.dialog.query_by_time_spent()
        hits = [logentry for logentry in self.task_list
                if (10 <= logentry.time_spent <= 20)]
        self.assertEqual(hits, list(self.dialog.logentry_queryset))


class TestSearchDialogSearchResultResponse(TestWithData):
    """
    Tests the response after the query has been performed.
    In case of success a change to the result dialog
    takes place.
    """

    def run(self, result=None):
        with test_database(test_db, (Employee, LogEntry)):
            super(TestSearchDialogSearchResultResponse, self).run(result)

    def setUp(self):
        """
        the database is filled with testdata.
        a logentry queryset is prepared as possible search result
        """
        self.create_test_data()
        self.dialog = SearchDialog()
        self.logentry_queryset = LogEntry.select()
        self.logentry_queryset_empty = LogEntry.select().where(LogEntry.employee_id == 100)

    @patch.object(ResultDialog, 'main')
    @patch.object(ResultDialog, '__init__')
    def test_search_check_for_dialog_goal_case_reached(self, mock_dialog_start, mock_main):
        """
        if there is a searchresult the reult dialog should be called with it
        """
        self.dialog.search_parameters = SearchParameters(header="some header")
        self.dialog.logentry_queryset = self.logentry_queryset
        mock_dialog_start.return_value = None
        self.dialog.check_for_dialog_goal()
        searchresult = ChoiceList(
            list=list(self.logentry_queryset), fmt_func=str,
            name="some header", fmt_detail_func=repr, choice_func=None)
        data = {'searchresult': searchresult}
        mock_dialog_start.assert_called_with(**data)
        mock_main.assert_called_with()

    def test_search_check_for_dialog_goal_case_not_reached(self):
        """
        if there is no search result the user receives a message
        """
        self.dialog.logentry_queryset = self.logentry_queryset_empty
        self.dialog.search_parameters = SearchParameters(header="some header")
        self.dialog.check_for_dialog_goal()
        self.assertIsNotNone(self.dialog.msg)

    def test_search_check_for_dialog_goal_case_no_queryset(self):
        """
        if there is no search result yet nothing happens
        """
        self.dialog.check_for_dialog_goal()
        self.assertIsNone(self.dialog.msg)


class TestSearchDialogChoiceEmployee(TestWithData):
    """
    tests the search preparation after the employee as a
    search parameter has been chosen from a list
    """
    def run(self, result=None):
        with test_database(test_db, (Employee, LogEntry)):
            super(TestSearchDialogChoiceEmployee, self).run(result)

    def setUp(self):
        """
        the list is set up
        """
        self.create_test_data()
        self.dialog = SearchDialog()
        self.dialog.active_choice_index = 1
        employee_list = list(Employee.select())
        self.employee = employee_list[1]
        self.dialog.choice_list = ChoiceList(list = employee_list)

    def test_search_choice_employee(self):
        """
        employee is chosen from list, the next step is prepared
        """
        func = self.dialog.choice_employee()
        self.assertEqual(self.dialog.search_parameters.employee_id, self.employee.id)
        self.assertIsNotNone(self.dialog.search_parameters.header)
        self.assertIsNone(self.dialog.active_choice_index)
        self.assertIsNone(self.dialog.active_choice_item)
        self.assertEqual(func, self.dialog.query_by_employee)


class TestSearchDialogChoiceDates(TestWithData):
    """
    tests the search preparation after the date as a
    search parameter has been chosen from a list
    """
    def run(self, result=None):
        with test_database(test_db, (Employee, LogEntry)):
            super(TestSearchDialogChoiceDates, self).run(result)

    def setUp(self):
        """
        the date list is set up
        """
        self.create_test_data()
        self.dialog = SearchDialog()
        self.dialog.active_choice_index = 0
        date_list = list(LogEntry.select(LogEntry.logdate).group_by(LogEntry.logdate))
        self.dialog.choice_list = ChoiceList(list=date_list)

    def test_search_choice_date(self):
        """
        the search is prepared with the chosen date as search parameter
        """
        func = self.dialog.choice_date()
        self.assertEqual(self.dialog.search_parameters.date_from, datetime.date(2015,8,29))
        self.assertIsNone(self.dialog.search_parameters.date_to)
        self.assertIsNotNone(self.dialog.search_parameters.header)
        self.assertIsNone(self.dialog.active_choice_index)
        self.assertIsNone(self.dialog.active_choice_item)
        self.assertEqual(func, self.dialog.query_by_date)


class TestSearchDialogInputChecks(unittest.TestCase):
    """
    tests the input checks of the search dialog
    """
    def setUp(self):
        """
        the dialog is started
        """
        self.dialog = SearchDialog()

    def test_search_check_term_no_input(self):
        """
        empty searchterm is not accepted: a message is send to the user
        """
        func = self.dialog.check_term('')
        self.assertIsNone(func)
        self.assertIsNotNone(self.dialog.msg)

    def test_search_check_term_valid_input(self):
        """
        a not empty searchterm is accepted: the searchparameters are prepared for
        actual the search
        """
        func = self.dialog.check_term('Some Term')
        self.assertEqual(func, self.dialog.query_by_term)
        self.assertEqual(self.dialog.search_parameters.searchterm, 'Some Term')
        self.assertIsNotNone(self.dialog.search_parameters.header)


    def test_search_check_time_spent_unvalid_input(self):
        """
        unvalid time input is not accepted: a message is send to the user
        """
        func = self.dialog.check_time_spent('x')
        self.assertIsNone(func)
        self.assertIsNotNone(self.dialog.msg)


    def test_search_check_time_spent_valid_exact_time(self):
        """
        a valid time input is number for the minutes:
        the searchparameters are prepared with time_to set to None
        """
        func = self.dialog.check_time_spent('30')
        self.assertEqual(func, self.dialog.query_by_time_spent)
        self.assertEqual(self.dialog.search_parameters.time_from, 30)
        self.assertIsNotNone(self.dialog.search_parameters.header)
        self.assertIsNone(self.dialog.search_parameters.time_to)

    def test_search_check_time_spent_valid_time_range(self):
        """
        the userinput is a time range, then time_from and time_to
        should be in the searchparameters
        """
        userinput = '30 - 40'
        func = self.dialog.check_time_spent('30 - 40')
        self.assertEqual(func, self.dialog.query_by_time_spent)
        self.assertEqual(self.dialog.search_parameters.time_from, 30)
        self.assertIsNotNone(self.dialog.search_parameters.header)
        self.assertEqual(self.dialog.search_parameters.time_to, 40)

    def test_search_check_date_valid_exact_time(self):
        """
        a valid time input is number for the minutes:
        the searchparameters are prepared with time_to set to None
        """
        func = self.dialog.check_date('29.8.2016')
        self.assertEqual(func, self.dialog.query_by_date)
        self.assertEqual(self.dialog.search_parameters.date_from, datetime.date(2016, 8, 29))
        self.assertIsNotNone(self.dialog.search_parameters.header)
        self.assertIsNone(self.dialog.search_parameters.time_to)

    def test_search_check_date_valid_time_range(self):
        """
        the userinput is a time range, then time_from and time_to
        should be in the searchparameters
        """
        func = self.dialog.check_date('29.8.2016 - 30.8.2016')
        self.assertEqual(func, self.dialog.query_by_date)
        self.assertEqual(self.dialog.search_parameters.date_from, datetime.date(2016, 8, 29))
        self.assertIsNotNone(self.dialog.search_parameters.header)
        self.assertEqual(self.dialog.search_parameters.date_to, datetime.date(2016, 8, 30))

    def test_search_check_date_unvalid(self):
        """
        the userinput is a time range, then time_from and time_to
        should be in the searchparameters
        """
        func = self.dialog.check_date('x')
        self.assertIsNotNone(self.dialog.msg)


class TestSearchDialogInputCheckEmployee(TestWithData):
    """
    tests the input check for the employee name: if the
    name identifies the employee, the query is returned and the search parameters
    are set. If more than one employee exist with that name, a list
    to choose from is presented.
    """
    def run(self, result=None):
        with test_database(test_db, (Employee, LogEntry)):
            super(TestSearchDialogInputCheckEmployee, self).run(result)

    def setUp(self):
        """
        sets up seacrh results for the 3 cases: one employee was found with a name,
        more than one employee found, no employee found.
        this set up relies on the knowledge of the testdata that is created
        """
        self.create_test_data()
        self.dialog = SearchDialog()
        self.logentry_queryset = LogEntry.select()
        self.employee1, self.employee_queryset1 = _get_employee_from_name('Love')
        self.employee2, self.employee_queryset2 = _get_employee_from_name('Sabine')
        self.employee3, self.employee_queryset3 = _get_employee_from_name('Nobody')
        self.logentries_dates = list(LogEntry.select(LogEntry.logdate).group_by(LogEntry.logdate))

    def test_search_check_employee_case_name_unique(self):
        """
        the name identifies the employee: the employee is taken
        for the query
        """
        func = self.dialog.check_employee('Love')
        self.assertEqual(func, self.dialog.query_by_employee)
        self.assertEqual(self.dialog.search_parameters.employee_id, self.employee1.id)
        self.assertIsNotNone(self.dialog.search_parameters.header)

    def test_search_check_employee_case_name_not_unique(self):
        """
        there are more than one employees with that name: a choice list
         is prepared
        """
        func = self.dialog.check_employee('Sabine')
        self.assertListEqual(self.dialog.choice_list.list, list(self.employee_queryset2))
        self.assertEqual(self.dialog.choice_list.fmt_func, str)
        self.assertEqual(self.dialog.choice_list.choice_func, self.dialog.choice_employee)
        self.assertTrue(self.dialog.choice)
        self.assertIsNone(func)

    def test_search_check_employee_case_name_not_found(self):
        """
        no employee was found for that name: the user is informed by a message
        """
        func = self.dialog.check_employee('Nobody')
        self.assertFalse(self.dialog.choice)
        self.assertIsNone(func)
        self.assertIsNotNone(self.dialog.msg)


class TestSearchDialogChooseDate(TestWithData):
    """
    tests the input check for the employee name: if the
    name identifies the employee, the query is returned and the search parameters
    are set. If more than one employee exist with that name, a list
    to choose from is presented.
    """

    def run(self, result=None):
        with test_database(test_db, (Employee, LogEntry)):
            super(TestSearchDialogChooseDate, self).run(result)

    def setUp(self):
        """
        the dialog is started and test data are created
        the date_list of logentries is established, in order to be compared
        with the dialogs result
        """
        self.create_test_data()
        self.dialog = SearchDialog()
        self.logentries_dates = [datetime.date(2015, 8, 29),
                                 datetime.date(2015, 9, 29),
                                 datetime.date(2016, 8, 29),
                                 datetime.date(2016, 8, 30),
                                 datetime.date(2016, 9, 29)]

    def test_search_check_date_list(self):
        """
        the user has taken option 'l' list dates for the search by
        date: a list of dates is prepared for the user to choose from
        """
        func = self.dialog.check_date('l')
        self.assertListEqual(
            [logentry.logdate for logentry in self.dialog.choice_list.list],
             self.logentries_dates)
        self.assertEqual(self.dialog.choice_list.fmt_func, _logentry_to_date)
        self.assertEqual(self.dialog.choice_list.choice_func, self.dialog.choice_date)
        self.assertTrue(self.dialog.choice)
        self.assertIsNone(func)