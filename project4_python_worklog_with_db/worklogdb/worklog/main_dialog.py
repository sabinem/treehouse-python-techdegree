"""
This file contains the main dialog
"""
from collections import OrderedDict

from worklogdb.worklog.helpers import quit
from worklogdb.worklog.base_dialog import BaseDialog
from worklogdb.worklog.search_dialog import SearchDialog
from worklogdb.worklog.create_dialog import CreateDialog


class MainDialog(BaseDialog):
    """
    main dialog which is the start dialog
    from here you can chose to go into the update
    or search dialog
    """
    def __init__(self):
        """
        the title is set for display
        """
        super().__init__()
        self.title = "Main Dialog"

    def search(self):
        """search logentries"""
        searchdialog = SearchDialog()
        searchdialog.main()

    def create(self):
        """create logentry"""
        createdialog = CreateDialog()
        self.msg = createdialog.main()

    def get_menu(self):
        """
        get the menu
        """
        return OrderedDict([
            ('s', self.search),
            ('c', self.create),
            ('q', quit),
        ])

if __name__ == '__main__':
    MainDialog()
