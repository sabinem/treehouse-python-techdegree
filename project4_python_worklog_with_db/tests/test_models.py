"""
Test for the functions that work with models
"""
from playhouse.test_utils import test_database

from worklogdb.worklog.models import LogEntry, Employee, _get_employee_from_name
from tests.testdata import TestWithData, test_db


class TestModels(TestWithData):
    """
    tests the string output for employees and
    also how to guess the employee from a name
    """
    def run(self, result=None):
        with test_database(test_db, (Employee, LogEntry)):
            super(TestModels, self).run(result)

    def setUp(self):
        """
        testdata is created
        and an employee is set up for the first test
        """
        self.create_test_data()
        self.employee = Employee.select().get()

    def test_models_employee___str__(self):
        """
        valid transformation of datetime.date in a format of '%d.%m.%Y'
        """
        self.assertEqual(str(self.employee),
                         self.employee.first_name + " " + self.employee.last_name)

    def test_models__get_employee_from_name_case_not_found(self):
        """
        None is returned, when the name was not found
        """
        name = "Markus"
        employee, employee_queryset = _get_employee_from_name(name)
        self.assertIsNone(employee)
        self.assertIsNone(employee_queryset)

    def test_models__get_employee_from_name_more_records_found(self):
        """
        A queryset is returned, when more employees with that name where found"""
        name = "Sabine"
        employee, employee_queryset = _get_employee_from_name(name)
        self.assertIsNone(employee)
        self.assertIsNotNone(employee_queryset)

    def test_models__get_employee_from_name_one_record_found(self):
        """
        the employee and a queryset are returned, when the name
        identified a unique employee
        """
        name = "Love"
        employee, employee_queryset = _get_employee_from_name(name)
        self.assertIsNotNone(employee)
        self.assertIsNotNone(employee_queryset)