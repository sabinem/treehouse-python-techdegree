import unittest
import datetime
import re

from playhouse.test_utils import test_database

from worklogdb.worklog.helpers import _format_date, _logentry_to_date, \
    date_fmt, _check_for_valid_date_format, _check_for_valid_time_format, \
    get_date_searchparameters_from_userinput,\
    get_time_searchparameters_from_userinput, _print_logentry_tmp
from worklogdb.worklog.models import LogEntry, Employee
from tests.testdata import TestWithData, test_db


class TestHelpers(TestWithData):

    def setUp(self):
        pass

    def test_helpers__format_date(self):
        """
        valid transformation of datetime.date in a format of '%d.%m.%Y'
        """
        test_date = datetime.date(2016, 9, 2)
        self.assertEqual(_format_date(test_date), '02.09.2016')

    def test_helpers__logentry_to_date(self):
        """
        get formated date out of logentry in format of '%d.%m.%Y'
        """
        with test_database(test_db, (Employee, LogEntry)):
            self.create_test_data()
            logentry = LogEntry.select().get()
            datestring = _logentry_to_date(logentry)
            date_from_datestring = datetime.datetime.strptime(datestring, date_fmt).date()
            self.assertEqual(logentry.logdate, date_from_datestring)

    def test_helpers__check_for_valid_date_format_case_valid(self):
        """
        for valid date_string, such as 12.3.2015 get valid datetime.date back
        """
        datestring='24.2.2017'
        valid_date = _check_for_valid_date_format(datestring)
        self.assertEqual(valid_date, datetime.date(2017, 2, 24))

    def test_helpers__check_for_valid_date_format_case_unvalid(self):
        """
        for unvalid date_string, such as 32.3.2015 raise ValueError
        """
        datestring = '32.3.2015'
        with self.assertRaises(ValueError):
            _check_for_valid_date_format(datestring)

    def test_helpers__check_for_valid_time_format_case_valid(self):
        """
        for valid timeinput in minutes, such as '30'
        get time as integer
        """
        timestring = '120'
        valid_time = _check_for_valid_time_format(timestring)
        self.assertEqual(valid_time, 120)

    def test_helpers__check_for_valid_time_format_case_unvalid(self):
        """
        for unvalid timeinput in minutes such as 'a'
        raise ValuError
        """
        timestring = 'a'
        with self.assertRaises(ValueError):
            _check_for_valid_time_format(timestring)

    def test_helpers_get_date_searchparameters_from_userinput_exact_date(self):
        """
        from user input build searchparameters: for exact date such as '24.2.2017'
        set date_from as datetime.date from input and date_to as None.
        """
        userinput = '24.2.2017'
        search_parameters = get_date_searchparameters_from_userinput(userinput)
        self.assertIsNone(search_parameters.date_to)
        self.assertEqual(search_parameters.date_from, datetime.date(2017, 2, 24))

    def test_helpers_get_date_searchparameters_from_userinput_date_range(self):
        """
        from user input build searchparameters: for date range
        such as '24.2.2017 - 25.3.2017'
        set date_from and date_to as datetime.date from input.
        """
        userinput = '24.2.2017 - 25.3.2017'
        search_parameters = get_date_searchparameters_from_userinput(userinput)
        self.assertEqual(search_parameters.date_from, datetime.date(2017, 2, 24))
        self.assertEqual(search_parameters.date_to, datetime.date(2017, 3, 25))

    def test_helpers_get_date_searchparameters_from_userinput_pattern_unvalid(self):
        """
        raise ValueError for unvalid pattern as userinput
        """
        userinput = 'What is this'
        with self.assertRaises(ValueError):
            get_date_searchparameters_from_userinput(userinput)

    def test_helpers_get_date_searchparameters_from_userinput_date_from_unvalid(self):
        """
        raise ValueError for unvalid date_from as userinput
        """
        userinput = '24.300.2017 - 25.3.2017'
        with self.assertRaises(ValueError):
            get_date_searchparameters_from_userinput(userinput)

    def test_helpers_get_date_searchparameters_from_userinput_date_to_unvalid(self):
        """
        raise ValueError for unvalid date_to as userinput
        """
        userinput = '24.2.2017 - 34.55.56'
        with self.assertRaises(ValueError):
            get_date_searchparameters_from_userinput(userinput)

    def test_helpers_get_time_searchparameters_from_userinput_exact_time(self):
        """
        from user input build searchparameters: for exact time such as '23'
        set time_from as int from input and time_to as None.
        """
        userinput = '35'
        search_parameters = get_time_searchparameters_from_userinput(userinput)
        self.assertIsNone(search_parameters.time_to)
        self.assertEqual(search_parameters.time_from, 35)

    def test_helpers_get_time_searchparameters_from_userinput_time_range(self):
        """
        from user input build searchparameters: for date range
        such as '24 - 35'
        set time_from and time_to as int from input.
        """
        userinput = '24 - 35'
        search_parameters = get_time_searchparameters_from_userinput(userinput)
        self.assertEqual(search_parameters.time_from, 24)
        self.assertEqual(search_parameters.time_to, 35)


    def test_helpers_get_time_searchparameters_from_userinput_pattern_unvalid(self):
        """
        raise ValueError for unvalid pattern as userinput
        """
        userinput = 'What is this'
        with self.assertRaises(ValueError):
            get_time_searchparameters_from_userinput(userinput)


    def test_helpers_get_time_searchparameters_from_userinput_time_from_unvalid(self):
        """
        raise ValueError for unvalid time_from as userinput
        """
        userinput = '4r - 30'
        with self.assertRaises(ValueError):
            get_time_searchparameters_from_userinput(userinput)


    def test_helpers_get_time_searchparameters_from_userinput_time_to_unvalid(self):
        """
        raise ValueError for unvalid time_to as userinput
        """
        userinput = '23 - hallo'
        with self.assertRaises(ValueError):
            get_time_searchparameters_from_userinput(userinput)

    def test_helpers__print_logentry_tmp_empty(self):
        """
        print in case of create the empty form
        """
        printstring = _print_logentry_tmp({}, logentry=None)
        self.assertEqual(printstring, (("{0:<20s} {1}\n{2:<20s} {3}\n"
             "{4:<20s} {5} min\n{6}\n{7}").
            format('Employee:',
                   '_' * 30,
                   'Task:',
                   '_' * 30,
                   'Time spent:',
                   '_' * 30,
                   'Note:',
                   '_' * 30 )))

    def test_helpers__print_logentry_tmp_filled(self):
        """
        print in case of create the filled out form
        """
        with test_database(test_db, (Employee, LogEntry)):
            self.create_test_data()
            employee = Employee.select().get()
            logentry_tmp = {
                'employee': employee,
                'task': 'some task',
                'time_spent': 30,
                'note': 'some note',
            }
            printstring = _print_logentry_tmp(logentry_tmp=logentry_tmp, logentry=None)
            self.assertEqual(printstring, (("{0:<20s} {1}\n{2:<20s} {3}\n"
                                            "{4:<20s} {5} min\n{6}\n{7}").
                                           format('Employee:',
                                                  employee,
                                                  'Task:',
                                                  'some task',
                                                  'Time spent:',
                                                  30,
                                                  'Note:',
                                                  'some note')))


    def test_helpers__print_logentry_tmp_for_update(self):
        """
        print in case of update: fields are taken from tmps and if they are
        not filled, from the database record
        """
        with test_database(test_db, (Employee, LogEntry)):
            self.create_test_data()
            employee = Employee.select().get()
            logentry = LogEntry.select().get()
            logentry_tmp = {
                'employee': employee,
                'time_spent': 45,
            }
            printstring = _print_logentry_tmp(logentry_tmp=logentry_tmp, logentry=logentry)
            self.assertEqual(printstring, (("{0:<20s} {1}\n{2:<20s} {3}\n"
                                            "{4:<20s} {5} min\n{6}\n{7}").
                                           format('Employee:',
                                                  employee,
                                                  'Task:',
                                                  logentry.task,
                                                  'Time spent:',
                                                  45,
                                                  'Note:',
                                                  logentry.note)))