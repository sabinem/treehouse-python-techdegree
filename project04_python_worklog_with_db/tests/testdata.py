import unittest
import datetime
from peewee import *

from worklogdb.worklog.models import Employee, LogEntry


test_db = SqliteDatabase(':memory:')


class TestWithData(unittest.TestCase):
    def create_test_data(self):
        """ ... create a bunch of employees"""
        employees = [
            {'first_name': 'Kenneth',
             'last_name': 'Love'},
            {'first_name': 'Sabine',
             'last_name': 'Maennel'},
            {'first_name': 'Sabine',
             'last_name': 'Konecny'},
        ]

        task_set_m = [
            {'task': 'Cleaning',
             'time_spent': 15,
             'note': 'fun',
             'logdate': datetime.date(2016, 8, 29),
             },
            {'task': 'Baking',
             'time_spent': 23,
             'note': 'hard',
             'logdate': datetime.date(2015, 8, 29),
             },
            {'task': 'Cooking',
             'time_spent': 45,
             'note': 'my best dinner ever',
             'logdate': datetime.date(2016, 8, 30),
             },
        ]

        task_set_l = [
            {'task': 'Testing',
             'time_spent': 15,
             'note': 'hard stuff',
             'logdate': datetime.date(2016, 8, 29),
             },
            {'task': 'Programming Python',
             'time_spent': 30,
             'note': 'was fun',
             'logdate': datetime.date(2015, 9, 29),
             },
            {'task': 'Learning Javascript',
             'time_spent': 30,
             'note': 'difficult',
             'logdate': datetime.date(2016, 9, 29),
             },
        ]

        task_set_k = [
            {'task': 'Gardening',
             'time_spent': 15,
             'note': 'the rain is helping',
             'logdate': datetime.date(2016, 8, 30),
             },
            {'task': 'Building a chincilla cage',
             'time_spent': 200,
             'note': 'need more wood',
             'logdate': datetime.date(2015, 8, 29),
             },

            {'task': 'Jogging',
             'time_spent': 15,
             'note': 'my usual round',
             'logdate': datetime.date(2016, 8, 29),
             },
        ]

        task_sets = {'Maennel': task_set_m, 'Konecny': task_set_k, 'Love': task_set_l}

        self.employee_list = []
        self.task_list = []

        for employee_record in employees:
            employee, created = Employee.get_or_create(
                first_name=employee_record['first_name'],
                last_name=employee_record['last_name']
            )
            self.employee_list.append(employee)
            for task in task_sets[employee.last_name]:
                logentry, created = LogEntry.get_or_create(
                    task=task['task'],
                    time_spent=task['time_spent'],
                    note=task['note'],
                    employee=employee.id,
                    logdate=task['logdate']
                )
                self.task_list.append(logentry)