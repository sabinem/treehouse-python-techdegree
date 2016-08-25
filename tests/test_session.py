"""
#from .context import worklog_peewee


from peewee import *

db = SqliteDatabase('test.db')
from peewee import *

class Employee(Model):
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)

    class Meta:
        database = db

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)



def initialize():
    db.connect()
    db.create_tables([Employee], safe=True)

    @patch('worklog_peewee.worklog_session.session.Session.get_first_name', return_value='Sabine')
    def test_get_first_name_valid(self, input):
        self.assertEqual(self.session.get_first_name(), 'Sabine')


    @patch('worklog_peewee.worklog_session.session.Session.get_first_name', return_value='Sabine x1')
    def test_get_first_name_unvalid(self, input):
        self.assertEqual(self.session.get_first_name(), self.session.get_first_name)
"""
import unittest


#from unittest.mock import patch
from worklogdb.worklog.session import Session, RC_RETURN
#from worklogdb.worklog.models import initialize

from playhouse.test_utils import test_database
from peewee import *

db = SqliteDatabase(':memory:')
from worklogdb.worklog.models import Employee, initialize


class SessionTests(unittest.TestCase):
    def create_test_data(self):
        # ... create a bunch of users and tweets
        Employee.create(first_name='Hans', last_name='Muller')
        Employee.create(first_name='Hans', last_name='Hoffman')
        Employee.create(first_name='Susan', last_name='Sunday')

    def setUp(self):
        self.session = Session()
        initialize()
        self.create_test_data()

    def test_session_register(self):
        """User choses register and should be served with a prompt.
        The system should know where to go next."""
        rc = self.session.register()
        self.assertEqual(rc[0], (self.session.check_fullname_input_and_create_employee))
        self.assertIsNotNone(rc[1])

    def test_session_check_fullname_input_and_create_employee(self):
        kwargs = {'userinput': 'Peter Pan'}
        rc = self.session.check_fullname_input_and_create_employee(**kwargs)
        self.assertEquals(rc[0], RC_RETURN)
        self.assertIsNotNone(rc[1])
        employee = Employee.get(Employee.first_name == 'Peter')
        self.assertIsNotNone(employee)
        self.assertEquals(employee.first_name, 'Peter')
        self.assertEquals(employee.last_name, 'Pan')

if __name__ == '__main__':
    unittest.main()