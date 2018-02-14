"""
This file contains the CreateDialog where logentries
can be created.
"""

from worklogdb.worklog.build_dialog import BuildDialog
from worklogdb.worklog.models import LogEntry


class CreateDialog(BuildDialog):
    """
    The create dialog allows to create logentries
    """
    def __init__(self):
        """
        the title of the dialog is set
        """
        super().__init__()
        self.title = "Create Logentry"

    def save_logentry(self):
        """
        the logentry is saved to the database after it has been build
        """
        LogEntry.create(
            task=self.logentry_tmp['task'],
            time_spent=self.logentry_tmp['time_spent'],
            note=self.logentry_tmp['note'],
            employee=self.logentry_tmp['employee']
        )
        super().save_logentry()
