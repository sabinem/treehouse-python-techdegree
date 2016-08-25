import unittest
from playhouse.test_utils import test_database
from peewee import *

from worklogdb.worklog.session import Session, RC_RETURN, DialogError
from worklogdb.worklog.models import Employee


test_db = SqliteDatabase(':memory:')


class SessionTests(unittest.TestCase):
    def create_test_data(self):
        """ ... create a bunch of employees"""
        self.hans1 = Employee.create(first_name='Hans', last_name='Muller')
        self.hans2 = Employee.create(first_name='Hans', last_name='Hoffman')
        Employee.create(first_name='Susan', last_name='Sunday')

    def setUp(self):
        """start the session"""
        self.session = Session()

    def test_session_register_ok(self):
        """user choice: register,
        response:
        next step: create employee,
        msg to the user"""
        rc = self.session.register()
        self.assertEqual(rc[0], (self.session.create_employee))
        self.assertIsNotNone(rc[1])

    def test_create_employee_ok(self):
        """user input: full name: ok,
        response:
        next step: return signal to return to caller,
        msg to the user,
        employee_instance with given name
        employee should be in database now."""
        with test_database(test_db, (Employee,)):
            self.create_test_data()
            kwargs = {'userinput': 'Peter Pan'}
            rc = self.session.create_employee(**kwargs)
            self.assertEqual(rc[0], RC_RETURN)
            self.assertIsNotNone(rc[1])
            employee = Employee.get(Employee.first_name == 'Peter')
            self.assertIsNotNone(employee)
            self.assertEqual(employee.first_name, 'Peter')
            self.assertEqual(employee.last_name, 'Pan')

    def test_login(self):
        """user Choice: login,
        response:
        next step: get employee list,
        msg to the user"""
        rc = self.session.login()
        self.assertEqual(rc[0], (self.session.get_employee_list))
        self.assertIsNotNone(rc[1])

    def test_get_employee_list_ok(self):
        """user input: first name: ok
        response:
        next step: login from list,
        msg to the user,
        list of employees with that first name"""
        with test_database(test_db, (Employee,)):
            self.create_test_data()
            kwargs = {'userinput': 'Hans'}
            rc = self.session.get_employee_list(**kwargs)
            self.assertEquals(rc[0], self.session.login_from_list)
            self.assertIsNotNone(rc[1])
            employee_list = [self.hans1, self.hans2]
            x = rc[2]
            self.assertSetEqual(set(rc[2]), set(employee_list))

    def test_get_employee_list_empty(self):
        """user input: first name: does not exist,
        response:
        next step: get employee list,
        msg to the user,
        None"""
        with test_database(test_db, (Employee,)):
            self.create_test_data()
            kwargs = {'userinput': 'Maike'}
            rc = self.session.get_employee_list(**kwargs)
            self.assertEquals(rc[0], self.session.get_employee_list)
            self.assertIsNotNone(rc[1])
            self.assertIsNone(rc[2])

    def test_get_employee_list_first_name_wrong_format(self):
        """user input: first name: wrong format,
        response:
        raise DialogError"""
        with test_database(test_db, (Employee,)):
            self.create_test_data()
            with self.assertRaises(DialogError):
                kwargs = {'userinput': 'Ma 4 ike'}
                self.session.get_employee_list(**kwargs)


if __name__ == '__main__':
    unittest.main()