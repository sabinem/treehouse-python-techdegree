"""
This file collects custom fields for wt-forms
"""
import datetime
from dateutil.parser import parse

from wtforms import validators, Field, SelectMultipleField


date_display_fmt = '%B, %d %Y'


def time_valid(value):
    """
    test the value and tests for a valid time
    it returns an Error or a valid time-delta
    """
    try:
        time_values = value.strip().split(':')
        timedelta = datetime.timedelta(hours=int(time_values[0]),
                                       minutes=int(time_values[1]))
    except ValueError:
        raise ValueError('This is not a valid time value')
    else:
        if timedelta == datetime.timedelta(minutes=0):
            raise ValueError('Time cannot be 0')
        else:
            return timedelta


class TimeField(Field):
    """
    Time-Field that gets a time value of hours and minutes
    it derives from a WT-Forms Field
    """
    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        else:
            return validators.text_type(self.data) \
                if self.data is not None else ''

    def process_data(self, value):
        self.data = value

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = valuelist[0]
            except ValueError:
                self.data = None

    def pre_validate(self, form):
        if self.raw_data[0] != '':
            try:
                time_valid(self.raw_data[0])
            except ValueError:
                raise validators.StopValidation(
                    "'{}' is not a valid time spent value"
                    .format(self.raw_data[0])
                )


class DateField(Field):
    """
    Date-Field that gets a date value
    it derives from a WT-Forms Field
    """
    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        else:
            return validators.text_type(self.data) \
                if self.data is not None else ''

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                datetime_valid = parse(valuelist[0].strip())
            except ValueError:
                self.data = None
                raise ValueError("This is not a valid date.")
            else:
                self.data = datetime_valid

    def process_data(self, value):
        self.data = value


class ChosenSelectField(SelectMultipleField):
    """
    Chosen Select Field that uses chosen.js from harvesthq:
    https://harvesthq.github.io/chosen/
    The field is derived from WT-Forms Field
    """
    def __init__(self, *args, choice_func=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.choice_func = choice_func

    def iter_choices(self):
        print('in iter_choices', self.choice_func)
        self.choices = self.choices or self.choice_func()
        for value, label in self.choices:
            if self.data is not None and not self.data == self.raw_data:
                from ast import literal_eval as make_tuple
                valueslist = \
                    [str(make_tuple(a)[0]) for a in self.data]
                selected = \
                    self.data is not None and self.coerce(value) in valueslist
            elif self.data is not None:
                selected = self.coerce(value) in self.data
            else:
                selected = False
            yield (value, label, selected)

    def pre_validate(self, form):
        print('in pre_validate', self.choice_func)
        self.choices = self.choices or self.choice_func()
        if self.data:
            values = list(str(c[0]) for c in self.choices)
            for d in self.data:
                if d not in values:
                    msg = ("'%(value)s' is not a valid choice for this field"
                           % dict(value=d))
                    raise ValueError(msg)
