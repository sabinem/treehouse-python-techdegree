"""
This file includes custom validators for wt-forms
"""
from wtforms import ValidationError


date_display_fmt = '%B, %d %Y'


def title_exists(modelclass, classname):
    """
    this function checks whether the given title already
    exists for a given model class
    """
    message = '%s with that title already exists.' % (classname)

    def _title_exists(form, field):
        if modelclass.select().\
                where(modelclass.title == field.data)\
                .exists() and form.id.data == '':
            raise ValidationError(message)
    return _title_exists
