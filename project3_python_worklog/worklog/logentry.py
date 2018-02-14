"""
This file knows about the structure of the csv file.
"""
import datetime

from .helpers import input_wrapper


class LogEntry():
    """
    A LogEntry instance is the structure of a row in the csv file.
    It can be initiated from scratch or from a given row in the
    csv file.
    """
    fieldnames = ['Log time', 'Task', 'Time spent', 'Note']
    log_time_fmt = '%d.%m.%Y %H:%M'

    def __init__(self, row=None):
        """
        The logentry row is set up either form an existing row, in
        order to update it or as a new row. In any case
        the user is asked whether he wants to overwrite the field values.
        """
        if row:
            print('Update log entry: press enter to accept a field value!\n')
            self.task = row['Task']
            self.time_spent = row['Time spent']
            self.note = row['Note']
            self.logtime = row['Log time']
        else:
            print('Create a new log entry\n')
        self.task = self._get_task()
        self.time_spent = self._get_time_spent()
        self.note = self._get_note()
        if not row:
            self.logtime = self._get_log_time_as_string()

    def _get_task(self):
        """
        Get the value of the 'Task' field form the user
        or from an existing row.
        """
        task = self.task if hasattr(self, 'task') else ''
        userinput = input_wrapper('Task: {} > '.format(task)).strip()
        if hasattr(self, 'task') and userinput == '':
            return self.task
        else:
            return userinput

    def _get_time_spent(self):
        """
        Get the value of the 'Time spent' field form the user
        or from an existing row.
        """
        time_spent = self.time_spent if hasattr(self, 'time_spent') else ''
        while True:
            userinput = input_wrapper(
                'Time spent on the task in minutes: {} > '
                .format(time_spent)).strip()
            if hasattr(self, 'time_spent') and userinput == '':
                return self.time_spent
            else:
                try:
                    minutes = int(userinput)
                    minutes_timedelta = datetime.timedelta(minutes=minutes)
                    if minutes_timedelta.days > 0:
                        print("{} is more then 24 hours. That can't be true"
                              .format(minutes))
                        continue
                except ValueError:
                    print('{} is not a valid entry for time spent.'
                          .format(userinput))
                    continue
                else:
                    return minutes

    def _get_note(self):
        """
        Get the value of the 'Note' field form the user
        or from an existing row.
        """
        note = self.note if hasattr(self, 'note') else ''
        userinput = input_wrapper('Note: {} > '.format(note))
        if hasattr(self, 'note') and userinput == '':
            return self.note
        else:
            return userinput

    def _get_log_time_as_string(self):
        """
        get the logtime as the current time
        """
        now = datetime.datetime.now()
        return datetime.datetime.strftime(now, LogEntry.log_time_fmt)

    def __str__(self):
        """
        format the row for useroutput
        """
        return "{0:3s} {1:20s} {2:20s} {3} min\n{4}\n    {5}".format(
            ' ',
            self.logtime,
            self.task,
            self.time_spent,
            80 * '-',
            self.note,
        )

    def as_csvdict_row(self):
        """
        format as a csv dict row for a csvdictwriter
        """
        return {
            'Task': self.task,
            'Time spent': self.time_spent,
            'Log time': self.logtime,
            'Note': self.note
        }
