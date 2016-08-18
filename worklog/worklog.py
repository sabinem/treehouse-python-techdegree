"""
This file contains the worklog class. It administers the worklog.
It writes and reads the csv file.
"""
import csv
import datetime
import os
import re

from .helpers import input_wrapper
from .logentry import LogEntry


log_time_fmt = '%d.%m.%Y %H:%M'
log_date_fmt = '%d.%m.%Y'
date_fmt = '%d.%m.%Y'
date_range_pattern = \
    r'(?P<date_from>[\d]{2}.[\d]{2}.[\d]{4})([\s]*-[\s]*(?P<date_to>[\d]{2}.[\d]{2}.[\d]{4}))?'
log_date_pattern = r'(?P<date>[\d]{2}.[\d]{2}.[\d]{4})\s[\d]{2}:[\d]{2}'
username_pattern = '[a-z]*'
time_range_pattern = r'(?P<time_from>[\d]+)(\s*-\s*(?P<time_to>[\d]+))?'


class WorkLog():
    """
    The Worklog instance is a worklog file, which is treated as a csv file.
    """
    SEARCH_EXACT = {'code': '1', 'text': 'in content'}
    SEARCH_BY_DATE = {'code': '2', 'text': 'by log date'}
    SEARCH_BY_TIME_SPENT = {'code': '3', 'text': 'by time spent'}
    SEARCH_BY_PATTERN = {'code': '4', 'text': 'as searchpattern'}
    OPTION_AVAILABLE_DATES = 'a'
    DELIMITER = ';'

    def __init__(self):
        """
        The file is searched with the username. If on file is found a
        filename is chosen. The file is not opened yet.
        """
        self.user, self.filename = self._worklog_get_file_name()

    def add_logentry(self, logentry):
        """
        Add a new logentry at the end of the file.
        """
        with open(self.filename, 'a+') as csvfile:
            logwriter = csv.DictWriter(csvfile,
                                       delimiter=WorkLog.DELIMITER,
                                       fieldnames=LogEntry.fieldnames)
            if os.path.getsize(self.filename) == 0:
                logwriter.writeheader()
            logwriter.writerow(logentry.as_csvdict_row())
        msg = ('--> Your log entry was written to the logfile {}'
               .format(self.filename))
        return msg

    def logentry_rewrite_worklog(self, row_nr, logentry=None):
        """
        The worklog file is rewritten in case
        a logentry is requested for update or delete.
        """
        with open(self.filename, newline='\n') as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter=WorkLog.DELIMITER)
            csv_updated_rows = []
            for row in csvreader:
                if csvreader.line_num != self._line_num_for_row_nr(row_nr):
                    csv_updated_rows.append(row)
                else:
                    if logentry:
                        csv_updated_rows.append(logentry.as_csvdict_row())
        with open(self.filename, 'w') as csvfile:
            csvwriter = csv.DictWriter(csvfile,
                                       delimiter=WorkLog.DELIMITER,
                                       fieldnames=LogEntry.fieldnames)
            csvwriter.writeheader()
            for row in csv_updated_rows:
                csvwriter.writerow(row)

    def search_worklog(self, searchoption=None, searchterm=None):
        """
        Search in the worklog with searchoption and searchterm
        Get the searchoption for the user and the also the
        searchterm. In principle a search can be repeated,
        but this feature is not used so far.
        """
        if not searchoption:
            searchoption = self._search_get_search_option()
            if searchoption['code'] == WorkLog.SEARCH_EXACT['code']:
                searchterm = self._get_searchterm_exact()
            elif searchoption['code'] == WorkLog.SEARCH_BY_PATTERN['code']:
                searchterm = self._get_searchterm_pattern()
            elif searchoption['code'] is WorkLog.SEARCH_BY_DATE['code']:
                searchterm = self._get_searchterm_by_date()
            elif searchoption['code'] is WorkLog.SEARCH_BY_TIME_SPENT['code']:
                searchterm = self._get_term_search_by_time_spent()
        data = self._worklog_read_data()
        if searchoption['code'] == WorkLog.SEARCH_BY_DATE['code']:
            datetime_from, datetime_to = \
                self._search_get_date_range(searchterm)
            result = [
                (row, data.index(row),) for row in data
                if (datetime_from <=
                    datetime.datetime.strptime(row['Log time'], log_time_fmt)
                    < datetime_to)]
        elif searchoption['code'] == WorkLog.SEARCH_BY_TIME_SPENT['code']:
            minutes_from, minutes_to = \
                self._search_get_minutes_range(searchterm)
            result = [(row, data.index(row),) for row in data
                      if (minutes_from <=
                          int(row['Time spent'])
                          <= minutes_to)]
        else:
            result = [(row, data.index(row)) for row in data
                      if (re.search(searchterm, row['Note'])
                          or re.search(searchterm, row['Task']))]
        result_row_nrs = [tuple[1] for tuple in result]
        return searchoption, searchterm, data, result, result_row_nrs

    def _search_get_search_option(self):
        """
        Get the searchoption from the user.
        """
        print("You can search the worklog by four options:\n"
              "1: by an exact phrase 'cooking'\n"
              "2: by date mm.dd.yyyy or date range: "
              "dd.mm.yyyy-dd.mm.yyyy\n"
              "3: by time spent as minutes or as range: 30 or 30-40\n"
              "4: by a regular expression\n")
        while True:
            msg = ("Please state the option by which you want to search\n"
                   "> ")
            userinput = input_wrapper(msg).strip()
            if userinput == WorkLog.SEARCH_EXACT['code']:
                return WorkLog.SEARCH_EXACT
            elif userinput == WorkLog.SEARCH_BY_DATE['code']:
                return WorkLog.SEARCH_BY_DATE
            elif userinput == WorkLog.SEARCH_BY_TIME_SPENT['code']:
                return WorkLog.SEARCH_BY_TIME_SPENT
            elif userinput == WorkLog.SEARCH_BY_PATTERN['code']:
                return WorkLog.SEARCH_BY_PATTERN
            else:
                print("{} is not a valid search option".format(userinput))
                continue

    def _worklog_read_data(self):
        """
        Read the Worklog and return its data as a list of rows.
        """
        with open('sabine-worklog.csv', newline='\n') as f:
            reader = csv.DictReader(f, delimiter=WorkLog.DELIMITER)
            return list(reader)

    def _get_searchterm_exact(self):
        """
        Get the searchterm for an exact search from the user, if he has
        choosen to search by an exact term.
        """
        userinput = input_wrapper("Please provide a search term\n> ")
        return userinput

    def _get_searchterm_pattern(self):
        """
        Get a regex pattern from the user, if he has choosen to search by
        a regular expression.
        """
        while True:
            userinput = input_wrapper("Please provide a search regex\n> ")\
                        .strip()
            try:
                re.compile(userinput)
            except re.error:
                print("{} is not a valid regular expression"
                      .format(userinput))
            else:
                return userinput

    def _get_searchterm_by_date(self):
        """
        Get the date range form the user, if he has choosen to
        search by date. The user may request to see a list of the
        dates on files first.
        """
        while True:
            userinput = input_wrapper(
                "Please provide a date or date range as "
                "'dd.mm.yyyy - dd.mm.yyyy\n"
                "or choose [a]vailable to see the available log dates> ")
            if userinput == self.OPTION_AVAILABLE_DATES:
                data = self._worklog_read_data()
                matches = set([re.match(log_date_pattern, row['Log time'])
                               for row in data])
                available_dates = \
                    set([match.group('date') for match in matches])
                print("Dates in the log:\n{}".format('-' * 15))
                for date in available_dates:
                    print("{}".format(date))
                print('-' * 15)
            else:
                try:
                    self._search_get_date_range(userinput)
                except ValueError as e:
                    print(e)
                    continue
                return userinput

    def _get_term_search_by_time_spent(self):
        """
        Get the searchpattern for 'Time spent' from the user.
        This can be a minutes value or a from and to value,
        such as '30-40'.
        """
        while True:
            userinput = input_wrapper(
                "Please provide a time or time range "
                "for time spent in minutes:\n"
                "Example '20 - 30'\n> ")
            try:
                self._search_get_minutes_range(userinput)
            except ValueError as e:
                print(e)
                continue
            return userinput

    def _search_get_date_range(self, userinput):
        """
        Prepare search by date:
        Get the range of dates as datetime values, in order to compare
        during the search in the file: datetime_from is set to the
        beginning of the day and fatetime_to is set to the beginning
        of the next day.
        """
        match = re.search(date_range_pattern, userinput)
        if not match:
            raise ValueError("{} is not a valid input "
                             "for this search".format(userinput))
        date_from = match.group('date_from')
        date_to = match.group('date_to')
        try:
            datetime_from = datetime.datetime.strptime(date_from, date_fmt)
        except ValueError:
            raise ValueError("{} is not a valid date".format(date_from))
        if date_to:
            try:
                datetime_to = datetime.datetime.strptime(date_to, date_fmt)
            except ValueError:
                raise ValueError("{} is not a valid date".format(date_to))
        else:
            datetime_to = datetime_from
        limit_datetime_to = datetime_to + datetime.timedelta(days=1)
        return datetime_from, limit_datetime_to

    def _search_get_minutes_range(self, userinput):
        """
        Prepare search by time spent:
        Get the range of minutes as intenger values, in order to compare
        during the search in the file.
        """
        match = re.search(time_range_pattern, userinput)
        if not match:
            raise ValueError("{} is not a valid input for this search."
                             .format(userinput))
        time_from = match.group('time_from')
        time_to = match.group('time_to')
        try:
            minutes_from = int(time_from)
        except ValueError:
            raise ValueError("{} is not a valid time".format(time_from))
        if time_to:
            try:
                minutes_to = int(time_to)
            except ValueError:
                raise ValueError("{} is not a valid time".format(time_to))
        else:
            minutes_to = minutes_from
        return minutes_from, minutes_to

    def _worklog_get_file_name(self):
        """
        Ask the user for his username and set the worklog file accordingly.
        """
        print("I am getting your work log!")
        while True:
            userinput = input_wrapper("Please type your username : > ")
            if len(userinput) < 6:
                print('The username should be at least 6 characters long')
                continue
            elif not re.match(username_pattern, userinput):
                print('{} is not a valid username. '
                      'It should only contain letters.')
                continue
            user = userinput
            worklogname = '-'.join([user, 'worklog'])
            filename = '.'.join([worklogname, 'csv'])
            return user, filename

    def print_list_header(self):
        """
        Print the list header of the search result list.
        """
        print("{0:3s} {1:20s} {2:20s} {3}".
              format('Nr ', 'Log time', 'Task', 'Time spent'))

    def format_list_row(self, row):
        """
        Format a row for output in the search result list.
        """
        return "{0:3d} {1:20s} {2:20s} {3} min".format(
            self._row_nr_for_print(row[1]),
            row[0]['Log time'],
            row[0]['Task'],
            row[0]['Time spent'],
        )

    def format_detail_row(self, row, active_row_nr):
        """
        Format a row of the search result for output in the detail
        view.
        """
        return "{0:3d} {1:20s} {2:20s} {3} min\n{4}\n{5}".format(
            self._row_nr_for_print(active_row_nr),
            row['Log time'],
            row['Task'],
            row['Time spent'],
            80 * '-',
            row['Note'],
        )

    def _row_nr_for_print(self, row_nr):
        """
        The print row number starts at 1 differing from the
        actual row_nr that starts at 0.
        """
        return row_nr + 1

    def _line_num_for_row_nr(self, row_nr):
        """
        The line_number in the csv file starts at 2, since the
        first line is the header.
        """
        return row_nr + 2
