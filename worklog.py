"""
Script to start the Worklogdb Application
"""
from worklogdb.worklog.models import initialize, add_data
from worklogdb.worklog.main_dialog import MainDialog


if __name__ == '__main__':
    initialize()
    add_data()
    main = MainDialog()
    main.main()
