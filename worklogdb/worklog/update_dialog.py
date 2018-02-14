"""
This file contains the Update Dialog class to update logentries
"""
import sys

from worklogdb.worklog.helpers import _print_logentry_tmp
from worklogdb.worklog.base_dialog import DialogStep
from worklogdb.worklog.build_dialog import BuildDialog


class UpdateDialog(BuildDialog):
    """
    Update Dialog for updating logentries
    """
    def __init__(self, **data):
        """
        the logentry choden for update is passed to the dialog
        """
        super().__init__()
        self.logentry = data.pop('logentry', None)
        self.title = "Update Logentry"

    def get_first_dialogstep(self):
        """
        the get name step is prepared
        """
        return DialogStep(
            checkinput_func=self.get_name,
            prompt="Name: [a] for accept as is\n"
                   "or enter your name:"
        )

    def prepare_get_task(self):
        """
        the get task step is prepared
        """
        self.activestep = DialogStep(
            checkinput_func=self.get_task,
            prompt="Task: [a] for accept as is\n"
                   "or enter your task:"
        )

    def prepare_get_time_spent(self):
        """
        the get time spent step is prepared
        """
        self.activestep = DialogStep(
            checkinput_func=self.get_time_spent,
            prompt="Time spent: [a] for accept as is\n"
                   "or enter the time you spent in minutes"
        )

    def prepare_get_note(self):
        """
        the get note step is prepared
        """
        self.activestep = DialogStep(
            checkinput_func=self.ask_for_note_update,
            prompt="Note: [a] for accept as is\n"
                   "or enter [c] to change."
        )

    def prepare_note_change(self):
        """
        the not change step is prepared
        """
        self.activestep = DialogStep(
            checkinput_func=self.get_note,
            prompt="Note: Please enter a note and exit with Ctrl D,"
                   "when you are finished.",
            input_method=sys.stdin.read
        )

    def get_name(self, userinput):
        """
        the name can be entered or the user can type 'a'
        to except the value of the logentry as it is
        """
        if userinput.lower() == 'a':
            self.logentry_tmp['employee'] = self.logentry.employee
            return self.prepare_get_task
        return super().get_name(userinput)

    def get_task(self, userinput):
        """
        the task can be entered or the user can type 'a'
        to except the value of the logentry as it is
        """
        if userinput.lower() == "a":
            self.logentry_tmp['task'] = self.logentry.task
            return self.prepare_get_time_spent
        return super().get_task(userinput)

    def get_time_spent(self, userinput):
        """
        the time spent can be entered or the user can type 'a'
        to except the value of the logentry as it is
        """
        if userinput.lower() == "a":
            self.logentry_tmp['time_spent'] = self.logentry.time_spent
            return self.prepare_get_note
        return super().get_time_spent(userinput)

    def ask_for_note_update(self, userinput):
        """
        the user is asked whether he wants to change the note:
        'c' means change and 'a' means accept
        """
        if userinput.lower() == "a":
            self.logentry_tmp['note'] = self.logentry.note
            return self.prepare_confirm
        elif userinput.lower() == "c":
            return self.prepare_note_change
        else:
            self.msg = "{} is not a valid choice".format(userinput)

    def save_logentry(self):
        """
        the logentry is saved to the database
        """
        self.logentry.task = self.logentry_tmp['task']
        self.logentry.time_spent = self.logentry_tmp['time_spent']
        self.logentry.note = self.logentry_tmp['note']
        self.logentry.employee_id = self.logentry_tmp['employee'].id
        self.logentry.save()
        super().save_logentry()

    def add_to_print_stack(self, print_stack):
        """
        the updated logentry is printed below the original record
        """
        super().add_to_print_stack(print_stack)
        if not self.choice:
            print_stack.append(
                _print_logentry_tmp(self.logentry_tmp, self.logentry))
            print_stack.append(60 * '-')
