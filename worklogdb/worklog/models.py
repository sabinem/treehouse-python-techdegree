from peewee import *
import datetime

from worklogdb.worklog.helpers import _format_date


db = SqliteDatabase('worklog.db')


class BaseModel(Model):
    class Meta:
        database = db


class Employee(BaseModel):
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)

    def __str__(self):
        return self.first_name + " " + self.last_name


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

task_sets = {1: task_set_l, 2: task_set_k, 3: task_set_m}


def add_data():
    count = 0
    for employee_record in employees:
        try:
            employee, created = Employee.get_or_create(
                first_name=employee_record['first_name'],
                last_name=employee_record['last_name']
            )
            count += 1
            for task in task_sets[count]:
                LogEntry.get_or_create(
                    task=task['task'],
                    time_spent=task['time_spent'],
                    note=task['note'],
                    employee=employee.id,
                    logdate=task['logdate'],
                )
        except IntegrityError as e:
            print(e)


class LogEntry(BaseModel):
    employee = ForeignKeyField(Employee)
    task = CharField(max_length=100)
    time_spent = IntegerField()
    note = TextField()
    logdate = DateField(default=datetime.datetime.now().date())

    def __str__(self):
        employee_name = "{}".format(self.employee)
        logdate_fmt = _format_date(self.logdate)
        return ("{0:<20s} {1} {2:<20s} {3:>5d} min".
                format(employee_name, logdate_fmt, self.task, self.time_spent))

    def __repr__(self):
        logdate_fmt = _format_date(self.logdate)
        return (("\n{0:<20s} {1}\n{2:<20s} {3}\n"
                "{4:<20s} {5}\n{6:<20s} {7} min\n{8}\n{9}").
                format('Employee:',
                       self.employee,
                       'Logdate:',
                       logdate_fmt,
                       'Task:',
                       self.task,
                       'Time spent:',
                       self.time_spent,
                       'Note:',
                       self.note))


def initialize():
    db.connect()
    db.create_tables([Employee, LogEntry], safe=True)


def _get_employee_from_name(name):
    employee_queryset = Employee.select() \
        .where(Employee.first_name
               .concat(" ")
               .concat(Employee.last_name)
               .contains(name)
               )
    employee_list = list(employee_queryset)
    if len(employee_list) == 1:
        employee = employee_queryset.get()
        return employee, employee_queryset
    elif len(employee_list) > 1:
        return None, employee_queryset
    else:
        return None, None
