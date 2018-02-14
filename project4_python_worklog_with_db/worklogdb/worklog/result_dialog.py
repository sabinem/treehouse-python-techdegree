"""
This file contains the Result Dialog, which displays
the search result.
"""
from collections import OrderedDict

from worklogdb.worklog.helpers import quit
from worklogdb.worklog.base_dialog import BaseDialog, DialogStep
from worklogdb.worklog.update_dialog import UpdateDialog


class ResultDialog(BaseDialog):
    """
    Dialog to list results:
    - User can switch between list and detail view
    - Records can be deleted or updated
    - it is possible to scroll in the result
    """
    def __init__(self, **data):
        """
        get result list from parameters, start with list view
        """
        super().__init__()
        self.choice_list = data.pop('searchresult', None)
        self.title = "Logentries Search Result for {}"\
                     .format(self.choice_list.name)
        self.choice = True
        self.list_menu = OrderedDict([
                ('b', self.back),
                ('q', quit),
            ])
        self.detail_menu = OrderedDict([
            ('p', self.show_previous),
            ('n', self.show_next),
            ('u', self.update),
            ('d', self.prepare_delete),
            ('l', self.show_list),
            ('b', self.back),
            ('q', quit),
        ])

    def get_menu(self):
        """
        start with menu for list view
        """
        return self.list_menu

    def update_menu(self):
        """
        adjust menu to list or detail view
        """
        if self.choice:
            return self.list_menu
        else:
            return self.detail_menu

    def show_list(self):
        """list"""
        self.choice = True
        self.active_choice_item = None
        self.active_choice_index = None

    def show_next(self):
        """next"""
        if self.active_choice_index < len(self.choice_list.list) - 1:
            self.active_choice_index += 1
            self.active_choice_item = \
                self.choice_list.list[self.active_choice_index]
        else:
            self.msg = "You have reached the start of the search results"

    def show_previous(self):
        """previous"""
        if self.active_choice_index > 0:
            self.active_choice_index -= 1
            self.active_choice_item = \
                self.choice_list.list[self.active_choice_index]
        else:
            self.msg = "You have reached the end of the search results"

    def update(self):
        """update"""
        data = {'logentry': self.active_choice_item}
        updatedialog = UpdateDialog(**data)
        self.msg = updatedialog.main()

    def prepare_delete(self):
        """delete"""
        self.activestep = \
            DialogStep(
                checkinput_func=self.confirm_delete,
                prompt="[y]es to confirm delete, "
                       "[f]orget to disregard delete request"
            )

    def confirm_delete(self, userinput):
        """
        confirm delete
        """
        userinput = userinput.lower()
        if userinput == 'y':
            return self.delete
        elif userinput == 'f':
            return self.discard_delete
        else:
            self.msg = "{} is not a valid choice".format(userinput)

    def delete(self):
        """
        delete the logentry
        """
        self.active_choice_item.delete_instance()
        self.msg = "The logentry has been deleted."
        self.choice_list.list.pop(self.active_choice_index)
        self.activestep = None
        self.show_list()

    def discard_delete(self):
        """
        reject the delete: the delete request is ignored
        """
        self.msg = "You delete request was ignored."
        self.activestep = None
