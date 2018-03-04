"""
This file contains the Build Dialog Class
Create and Update Dialog inherit from that class
"""
import sys

from worklogdb.worklog.helpers import _check_for_valid_time_format,\
    _print_logentry_tmp
from worklogdb.worklog.base_dialog import BaseDialog, DialogStep, \
    ChoiceList
from worklogdb.worklog.models import _get_employee_from_name


class BuildDialog(BaseDialog):
    """
    Class for Dialogs that build logentries
    """
    def __init__(self):
        """
        A temporary logentry is established
        """
        super().__init__()
        self.title = "Build Logentry"
        self.logentry_tmp = {}

    def get_first_dialogstep(self):
        """
        the first dialogstep is fetched: entering the name
        """
        return DialogStep(
            checkinput_func=self.get_name,
            prompt="Please enter your name"
        )

    def prepare_get_task(self):
        """
        dialogstep getting the task is prepared
        """
        self.activestep = DialogStep(
            checkinput_func=self.get_task,
            prompt="Please enter your task"
        )

    def prepare_get_time_spent(self):
        """
        dialogstep getting time spent is prepared
        """
        self.activestep = DialogStep(
            checkinput_func=self.get_time_spent,
            prompt="Please enter the time you spent in minutes"
        )

    def prepare_get_note(self):
        """
        dialogstep getting the note is prepared
        """
        self.activestep = DialogStep(
            checkinput_func=self.get_note,
            prompt="Please enter a note and exit with Ctrl D,"
                   "when you are finished.",
            input_method=sys.stdin.read
        )

    def prepare_confirm(self):
        """
        dialogstep confirmation of the data is prepared
        """
        self.activestep = DialogStep(
            checkinput_func=self.confirm,
            prompt="Please confirm with [s]ave or discard with [d]iscard"
        )

    def get_name(self, userinput):
        """
        checks the name input and initiates a choice list, so that
        the user can choose a name from the list
        """
        employee, employee_queryset = _get_employee_from_name(userinput)
        if employee_queryset:
            self.choice = True
            self.choice_list = ChoiceList(
                list=list(employee_queryset),
                fmt_func=str,
                choice_func=self.choice_employee
            )
        else:
            self.msg = ("No employee has been found with name {}"
                        .format(userinput))

    def choice_employee(self):
        """
        the employee choice is processed, next: prepare get task
        """
        employee = self.choice_list.list[self.active_choice_index]
        self.logentry_tmp['employee'] = employee
        self.active_choice_item = None
        self.active_choice_index = None
        return self.prepare_get_task

    def get_task(self, userinput):
        """
        the task input is checked
        """
        if userinput != "":
            self.logentry_tmp['task'] = userinput
            return self.prepare_get_time_spent
        else:
            self.msg = "{} is not a valid task name".format(userinput)

    def get_time_spent(self, userinput):
        """
        the time spent input is checked
        """
        try:
            time_spent = _check_for_valid_time_format(userinput)
        except ValueError as e:
            self.msg = e
        else:
            self.logentry_tmp['time_spent'] = time_spent
            return self.prepare_get_note

    def get_note(self, userinput):
        """
        the note input is checked
        """
        self.logentry_tmp['note'] = userinput
        return self.prepare_confirm

    def confirm(self, userinput):
        """
        the user is asked to confirm or discard
        """
        if userinput in 's':
            return self.save_logentry
        elif userinput == 'd':
            return self.discard_logentry
        else:
            self.msg = "{} is not a valid choice".format(userinput)

    def save_logentry(self):
        """
        the save process is performed: this method is overwritten
        by the Create or Update Dialog to really save the data,
        finish the dialog.
        """
        self.quit_dialog = True
        self.return_msg = "The logentry has been saved."

    def discard_logentry(self):
        """
        the build is discarded, finish the dialog
        :return:
        """
        self.quit_dialog = True
        self.return_msg = "Your logentry has been discarded"

    def add_to_print_stack(self, print_stack):
        """
        print the data
        """
        if not self.choice:
            print_stack.append(_print_logentry_tmp(self.logentry_tmp))
            print_stack.append(60 * '-')
