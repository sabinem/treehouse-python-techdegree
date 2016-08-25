import sys
from peewee import *

from worklogdb.worklog.models import initialize
from worklogdb.worklog.session import Session


if __name__ == '__main__':
    initialize()
    session = Session()
    session.login_dialog()
