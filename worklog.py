"""
Script to start the Worklogdb Application
"""
from worklogdb.worklog.models import initialize
from worklogdb.worklog.main_dialog import MainDialog


if __name__ == '__main__':
    initialize()
    m = MainDialog()
    m.main()
