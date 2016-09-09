"""
This file contains the search dialog
"""
from collections import OrderedDict

from worklogdb.worklog.helpers import quit, \
    SearchParameters, _logentry_to_date, \
    get_time_searchparameters_from_userinput, \
    get_date_searchparameters_from_userinput
from worklogdb.worklog.base_dialog import BaseDialog, DialogStep, \
    ChoiceList
from worklogdb.worklog.result_dialog import ResultDialog
from worklogdb.worklog.models import LogEntry, Employee, \
    _get_employee_from_name


class SearchDialog(BaseDialog):
    """
    Search Dialog: the user can search for logentries: first the
    userinput is evaluated and the searchparameters are set,
    second the query is performed.
    """

    def __init__(self):
        """
        the dialog title is set
        """
        super().__init__()
        self.title = "Search for Logentries"

    def get_menu(self):
        """
        the menu is prepared
        """
        return OrderedDict([
            ('w', self.search_by_term),
            ('t', self.search_by_time_spent),
            ('d', self.search_by_date),
            ('e', self.search_by_employee),
            ('b', self.back),
            ('q', quit),
        ])

    def init_new_search(self):
        """
        a new search is initialized: the result and parameters
        of the previous search are deleted
        """
        if hasattr(self, 'search_parameters'):
            del self.search_parameters
            del self.logentry_queryset

    def search_by_term(self):
        """search by term"""
        self.init_new_search()
        self.activestep = DialogStep(
                    checkinput_func=self.check_term,
                    prompt="Please provide a searchterm")

    def search_by_time_spent(self):
        """search by time spent"""
        self.init_new_search()
        self.activestep = DialogStep(
                    checkinput_func=self.check_time_spent,
                    prompt="Please provide a time or time range in minutes"
                           "\nsuch as '30' or '30 - 45")

    def search_by_date(self):
        """search by date"""
        self.init_new_search()
        self.activestep = \
            DialogStep(
                checkinput_func=self.check_date,
                prompt="Please provide a date or range of dates\n"
                       "such as '30.8.2016' or '30.9.2016\n"
                       "or request [l]ist of available logdates")

    def search_by_employee(self):
        """search by employee"""
        self.init_new_search()
        self.activestep = \
            DialogStep(
                checkinput_func=self.check_employee,
                prompt="Please enter the name of an employee")

    def check_term(self, userinput):
        """
        the userinput for search by term is checked
        in case the check was okay:
        the searchparameters are set
        the qury function is returned
        """
        if userinput == "":
            self.msg = "{} is not a valid search term!".format(userinput)
            return
        else:
            header = "Logentries for searchterm: {}" \
                .format(userinput)
            self.search_parameters = SearchParameters(
                searchterm=userinput,
                header=header
            )
            return self.query_by_term

    def check_time_spent(self, userinput):
        """
        the userinput for search by time spent is checked
        in case the check was okay:
        the searchparameters are set
        the qury function is returned
        """
        try:
            search_parameters = \
                get_time_searchparameters_from_userinput(userinput)
        except ValueError as e:
            self.msg = e
            return
        else:
            self.search_parameters = search_parameters
            return self.query_by_time_spent

    def check_employee(self, userinput):
        """
        the userinput for search by employee is checked
        example: "Sab"
        special in this case: form the name input the employee
        is guessed: if the guess was not unique, a list of
        employees is prepared for the user to choose from
        if the name was unique:
        the searchparameters are set
        the qury function is returned
        """
        employee, employee_queryset = _get_employee_from_name(userinput)
        if employee:
            header = ("Logentries for employee: {}"
                      .format(employee))
            self.search_parameters = SearchParameters(
                employee_id=employee.id,
                header=header
            )
            return self.query_by_employee
        elif employee_queryset:
            self.choice = True
            self.choice_list = ChoiceList(
                list=list(employee_queryset),
                fmt_func=str,
                choice_func=self.choice_employee
            )
            return
        else:
            self.msg = "No employee has been found with name {}"\
                       .format(userinput)
            return

    def check_date(self, userinput):
        """
        the userinput for search by date is checked
        example: "29.8.2016" or "29.8.2016 - 30.8.2016"
        if a date or date range is given,
        the searchparameters are set
        the qury function is returned.
        The user can also choose "l" as list, then a list of all
        dates for which logentries exist is prepared
        for the user to choose from
        """
        if userinput == 'l':
            logentries = \
                LogEntry.select(LogEntry.logdate).group_by(LogEntry.logdate)
            self.choice_list = ChoiceList(
                list=list(logentries),
                fmt_func=_logentry_to_date,
                choice_func=self.choice_date
            )
            self.choice = True
            return
        else:
            try:
                search_parameters = \
                    get_date_searchparameters_from_userinput(userinput)
            except ValueError as e:
                self.msg = e
                return
            else:
                self.search_parameters = search_parameters
                return self.query_by_date

    def choice_employee(self):
        """
        the choice of an employee by means of a list
        is processed: the searchparameters are set
        and the query function is returned
        """
        employee = self.choice_list.list[self.active_choice_index]
        self.active_choice_item = None
        self.active_choice_index = None
        header = "Logentries for Employee: {}" \
            .format(employee)
        self.search_parameters = SearchParameters(
            employee_id=employee.id,
            header=header
        )
        return self.query_by_employee

    def choice_date(self):
        """
        the choice of a date by means of a list
        is processed: the searchparameters are set
        and the query function is returned
        """
        logentry = self.choice_list.list[self.active_choice_index]
        self.active_choice_item = None
        self.active_choice_index = None
        header = "Logentries for Logdate: {}" \
            .format(logentry.logdate)
        self.search_parameters = SearchParameters(
            date_from=logentry.logdate,
            header=header
        )
        return self.query_by_date

    def query_by_term(self):
        """
        query for search by term and set up the searchresult list
        """
        searchstring = self.search_parameters.searchterm
        self.logentry_queryset = \
            LogEntry.select()\
                    .where(LogEntry.task.contains(searchstring) |
                           LogEntry.note.contains(searchstring))

    def query_by_time_spent(self):
        """
        query for search by time spent
        and set up the searchresult list
        """
        time_from = self.search_parameters.time_from
        if self.search_parameters.time_to:
            time_to = self.search_parameters.time_to
        else:
            time_to = time_from
        self.logentry_queryset = \
            LogEntry.select()\
                    .where((LogEntry.time_spent <= time_to) &
                           (LogEntry.time_spent >= time_from))

    def query_by_date(self):
        """
        query for search by date and set up the searchresult list
        """
        date_from = self.search_parameters.date_from
        if self.search_parameters.date_to:
            date_to = self.search_parameters.date_to
        else:
            date_to = date_from
        self.logentry_queryset = \
            LogEntry.select()\
                    .where((LogEntry.logdate <= date_to) &
                           (LogEntry.logdate >= date_from))

    def query_by_employee(self):
        """
        query for search by employee and set up the searchresult list
        """
        self.logentry_queryset = \
            LogEntry.select().join(Employee).where(
                (Employee.id == self.search_parameters.employee_id)
            )

    def check_for_dialog_goal(self):
        """
        the dialog goal is reached if the searchresult could be
        established, which means that logentries where found.
        In this case the result dialog is called with the data
        """
        if hasattr(self, 'logentry_queryset'):
            if self.logentry_queryset:
                searchresult = ChoiceList(
                    list=list(self.logentry_queryset),
                    fmt_func=str,
                    name=self.search_parameters.header,
                    fmt_detail_func=repr,
                    choice_func=None)
                data = {'searchresult': searchresult}
                resultdialog = ResultDialog(**data)
                self.msg = resultdialog.main()
            else:
                self.msg = 'No logentries for {} have been found'\
                           .format(self.search_parameters.header)
