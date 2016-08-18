"""
This file contains the session class. The session controls
the dialog, when the user interacts with the workfile.
"""
from .worklog import WorkLog
from .logentry import LogEntry
from .helpers import input_wrapper


class Session:
    """
    The Session instance is a session of a user with his worklog.
    """
    ACTION_QUIT = {'code': 'q', 'menu': '[q]uit'}
    ACTION_SEARCH = {'code': 's', 'menu': '[s]earch worklog'}
    ACTION_CREATE = {'code': 'c', 'menu': '[c]reate logentry'}
    BASIC_OPTIONS = [ACTION_QUIT]
    ADVANCED_OPTIONS = [ACTION_QUIT, ACTION_CREATE, ACTION_SEARCH]
    STATE_CREATE = 'Search Worklog'
    STATE_SEARCH = 'Create Logentry'
    STATE_FETCH = 'Fetch Worklog'
    STATE_LIST = 'Search Result'
    STATE_BASE = 'Your worklog is ready for you!'
    STATE_DETAIL = 'Logentry detail view'
    UPDATE_LOG = 'u'
    DELETE_LOG = 'd'
    NEXT_LOG = 'n'
    PREVIOUS_LOG = 'p'
    LIST = 'l'

    def __init__(self):
        """
        When the session starts, the worklog of a user must be identified
        by his user name.
        Afterwards a dialogue loop runs to keep the session alive.
        'next_state' is the most important control attribut here:
        it always knows what dialog state comes next.
        """
        self.worklog = None
        self.next_state = self.setup_worklog
        self.active_screen_header = 'Welcome to the WorkLog Application'
        self.active_menu_options = Session.BASIC_OPTIONS
        self.active_state = None
        self.active_logentry = None
        self.active_row_nr = None
        self.searchoption = None
        self.search_term = None
        self.result = None
        self.msg = None
        self.repeat_search = False
        while True:
            self.next_state()

    def setup_worklog(self):
        """
        Fetch the worklog and set the screen header with the name of the file.
        This is the first step in the dialog.
        """
        self.active_state = Session.STATE_FETCH
        self._print_page()
        self.worklog = WorkLog()
        self.msg = ('Your worklog {} has been prepared.'
                    .format(self.worklog.filename))
        self.active_screen_header = (
            'Worklog: {} for User {}'
            .format(self.worklog.filename, self.worklog.user))
        self.next_state = self.base_state

    def base_state(self):
        """
        Start the default dialog.
        """
        self.active_state = Session.STATE_BASE
        self.active_menu_options = Session.ADVANCED_OPTIONS
        self._print_page()
        if self.active_logentry:
            print(self.active_logentry)
            self.active_logentry = None
        self.next_state = None
        while not self.next_state:
            userinput = (input_wrapper(
                'Choose from the menu above, what you want to do \n> ')
                .strip().lower())
            if self._check_menu_option(userinput):
                break
            else:
                print("{} is not a valid action code. "
                      "See the menu above for your options"
                      .format(userinput))

    def create_logentry(self):
        """
        Create a new Logentry
        """
        self.active_state = Session.STATE_CREATE
        self.active_menu_options = Session.BASIC_OPTIONS
        self._print_page()
        logentry = LogEntry()
        self.worklog.add_logentry(logentry)
        self.msg = "\nThe logentry has been added:\n"
        self.active_logentry = logentry
        self.next_state = self.base_state

    def logentry_result_detail(self):
        """
        Detail view of the search result: you can scroll
        in the records or go back to the list view.
        You can also choose to update or delete, but then
        the dialog with the search results ends since the file
        is rewritten in this case. you get back to the base dialog
        in this case after the update or delete is performed.
        """
        self.active_state = Session.STATE_DETAIL
        self.active_menu_options = Session.ADVANCED_OPTIONS
        self._print_page()
        self.worklog.print_list_header()
        print("\n{}".format(self.worklog.format_detail_row(
            self.data[self.active_row_nr],
            self.active_row_nr)))
        print("\nYou can view the [n]ext or [p]revious "
              "logentry in the search results.\n"
              "or return to the list with [l]ist\n"
              "\nYou can [u]update or [d]elete this logentry "
              "and leave the search result\n")
        while True:
            userinput = input_wrapper("What do you want to do? > ")
            if self._check_menu_option(userinput):
                break
            if userinput == Session.NEXT_LOG:
                if (self.result_row_nrs.index(self.active_row_nr)
                        < len(self.result_row_nrs) - 1):
                    result_index_active_row_nr = \
                        self.result_row_nrs.index(self.active_row_nr)
                    self.active_row_nr = \
                        self.result_row_nrs[result_index_active_row_nr + 1]
                    self.next_state = self.logentry_result_detail
                    break
                else:
                    print('you have reached the end of the search result')
                    continue
            elif userinput == Session.PREVIOUS_LOG:
                if self.result_row_nrs.index(self.active_row_nr) > 0:
                    result_index_active_row_nr = \
                        self.result_row_nrs.index(self.active_row_nr)
                    self.active_row_nr = \
                        self.result_row_nrs[result_index_active_row_nr - 1]
                    self.next_state = self.logentry_result_detail
                    break
                else:
                    print('you have reached the start of the search result')
                    continue
            elif userinput == Session.LIST:
                self.next_state = self.list_search_result
                break
            elif userinput == Session.UPDATE_LOG:
                self.active_logentry = LogEntry(self.data[self.active_row_nr])
                self.worklog.logentry_rewrite_worklog(
                    self.active_row_nr, self.active_logentry)
                self.msg = 'The logentry has been updated'
                self.next_state = self.base_state
                self.repeat_search = True
                break
            elif userinput == Session.DELETE_LOG:
                self.worklog.logentry_rewrite_worklog(self.active_row_nr)
                self.msg = 'The logentry has been deleted'
                self.next_state = self.base_state
                self.repeat_search = True
                break
            else:
                print("{} is not a valid action code. "
                      "See the above for your options"
                      .format(userinput))
                continue

    def search_worklog(self):
        """
        Ask the user for a searchoption and searchterm and perform the search.
        The search parameters are returned for further use.
        """
        self.result = None
        self.searchoption = None
        self.searchterm = None
        self.active_menu_options = Session.BASIC_OPTIONS
        self.active_state = Session.STATE_SEARCH
        self._print_page()
        (self.searchoption,
         self.searchterm,
         self.data,
         self.result,
         self.result_row_nrs) = self.worklog.search_worklog()
        if self.result:
            self.msg = (
                "This is the result of your search with '{} {}':"
                .format(self.searchterm, self.searchoption['text']))
            self.next_state = self.list_search_result
        else:
            self.msg = (
                "No entries where found"
                " for this search with '{} {}'.\n"
                .format(self.searchterm, self.searchoption['text']))
            self.next_state = self.base_state

    def list_search_result(self):
        """
        List the search results and ask the user to choose a logentry
        for the detail view by row number.
        """
        self.active_state = Session.STATE_LIST
        self.active_menu_options = Session.ADVANCED_OPTIONS
        self._print_page()
        self.worklog.print_list_header()
        for row in self.result:
            print(self.worklog.format_list_row(row))
        self.next_state = self.logentry_result_detail
        self.active_row_nr = self._list_search_result_select_row_nr()

    def _list_search_result_select_row_nr(self):
        """
        Get the userinput for the row_nr in order to choose a record
        from the search result list for a detail view.
        """
        while True:
            userinput = input_wrapper("\nYou can select a log "
                                      "entry by typing it's row nr:\n> ")
            if self._check_menu_option(userinput):
                break
            try:
                requested_row_nr = int(userinput) - 1
            except ValueError:
                print("{} is not a number".format(userinput))
                continue
            else:
                if requested_row_nr in self.result_row_nrs:
                    return requested_row_nr
                else:
                    continue

    def _print_page(self):
        """
        Print a freh page. This helper function is
        used by all dialog steps.
        """
        print("\033c", end="")
        print(self.active_screen_header)
        print('-' * 80)
        menu = ' | '\
               .join(action['menu'] for action in self.active_menu_options)
        text = "Step: {}".format(self.active_state)
        print('Menu: {}\n{}\n{}\n{}'.format(menu, '-' * 80, text, '=' * 80))
        if hasattr(self, 'msg') and self.msg:
            print(self.msg)
            del self.msg

    def _check_menu_option(self, userinput):
        """
        Check if the user has chosen an option from the menu, such as
        quit, search or create.
        """
        if userinput == Session.ACTION_CREATE['code']:
            self.next_state = self.create_logentry
            return True
        elif userinput == Session.ACTION_SEARCH['code']:
            self.next_state = self.search_worklog
            return True
        else:
            return False
