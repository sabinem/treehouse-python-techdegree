"""
This file contains basic helper-functionality
"""
import collections
import os
import sys
import re
from dateutil.parser import parse


SearchParameters = collections.namedtuple(
    'SearchParameters',
    ['time_from', 'time_to',
     'date_from', 'date_to',
     'searchterm', 'name', 'employee_id',
     'header',
     'query_func'])
SearchParameters.__new__.__defaults__ = \
    (None, None, None, None, None, None, None, '', None)
date_fmt = '%d.%m.%Y'
name_pattern = ''


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def quit(**kwargs):
    """quit"""
    sys.exit()


def _check_for_valid_date_format(datestring):
    """
    check date input that comes as string and
    return as datetime.date if it is valid.
    """
    try:
        datetime_valid = parse(datestring)
    except ValueError:
        raise ValueError("{} is not a valid date".format(datestring))
    else:
        return datetime_valid.date()


def _check_for_valid_time_format(timestring):
    """
    check time input that comes as string and return as int if it is valid.
    """
    try:
        time_valid = int(timestring)
    except ValueError:
        raise ValueError("{} is not a valid time".format(timestring))
    else:
        return time_valid


def get_date_searchparameters_from_userinput(userinput):
    """
    return searchparameters from a date or range of dates, that where
    given as stringinput such as '2.3.2016- 8.3.2016'
    the parameters date_from and date_to are set as datetime.date
    if the range part: '- 8.3.2016' is missing, the date_to is set to None
    """
    date_range_pattern = \
        r'(?P<date_from>[\d./-]+)([\s]*-[\s]*(?P<date_to>[\d./-]+))?$'
    match = re.search(date_range_pattern, userinput)
    if not match:
        raise ValueError("{} is not a valid input "
                         "for this search".format(userinput))
    date_from = match.group('date_from')
    date_to = match.group('date_to')
    try:
        date_from_clean = _check_for_valid_date_format(date_from)
    except ValueError:
        raise
    else:
        if date_to:
            try:
                date_to_clean = _check_for_valid_date_format(date_to)
            except ValueError:
                raise
            else:
                header = "Logentries with logdate: {} - {}" \
                    .format(date_from, date_to)
        else:
            header = ("Logentries with logdate: {}"
                      .format(date_from))
            date_to_clean = None
    return SearchParameters(date_from=date_from_clean, date_to=date_to_clean,
                            header=header)


def get_time_searchparameters_from_userinput(userinput):
    """
    return searchparameters from a time or range of time, that where
    given as stringinput such as '23 - 45'
    the parameters time_from and time_to are set as int
    if the range part: '- 45' is missing, the time_to is set to None
    """
    time_range_pattern = r'^(?P<time_from>[\d]+)(\s*-\s*(?P<time_to>[\d]+))?$'
    match = re.search(time_range_pattern, userinput)
    if not match:
        raise ValueError("{} is not a valid input for this search."
                         .format(userinput))
    time_from = match.group('time_from')
    time_to = match.group('time_to')
    time_from_clean = _check_for_valid_time_format(time_from)
    if time_to:
        time_to_clean = _check_for_valid_time_format(time_to)
        header = "Search for time spent: {} - {} minutes"\
                 .format(time_from, time_to)
    else:
        header = "Logentries with time spent: {} minutes" \
            .format(time_from)
        time_to_clean = None
    return SearchParameters(time_from=time_from_clean, time_to=time_to_clean,
                            header=header)


def _format_date(logdate):
    """
    return a formatted datestring from datetime.date
    """
    date_fmt = '%d.%m.%Y'
    return logdate.strftime(date_fmt)


def _logentry_to_date(logentry):
    """
    return a formatted datestring from a logentry
    """
    date_fmt = '%d.%m.%Y'
    return logentry.logdate.strftime(date_fmt)


def _print_logentry_tmp(logentry_tmp, logentry=None):
    """
    prepares a temporary logentry for print as a form
    that has been filled in parts
    """
    logentry_print = {}
    for field in ['employee', 'task', 'time_spent', 'note']:
        if field in logentry_tmp.keys():
            logentry_print[field] = logentry_tmp[field]
        elif logentry:
            logentry_print[field] = getattr(logentry, field)
        else:
            logentry_print[field] = '_' * 30
    return (("{0:<20s} {1}\n{2:<20s} {3}\n"
             "{4:<20s} {5} min\n{6}\n{7}").
            format('Employee:',
                   logentry_print['employee'],
                   'Task:',
                   logentry_print['task'],
                   'Time spent:',
                   logentry_print['time_spent'],
                   'Note:',
                   logentry_print['note'], ))
