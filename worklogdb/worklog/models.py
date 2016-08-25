from peewee import *

from worklogdb.worklog.settings import db


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
