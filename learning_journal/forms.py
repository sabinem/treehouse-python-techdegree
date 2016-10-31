"""
This file includes the Form, deriving from WT-Forms
"""
import datetime

from wtforms import validators, StringField, \
    TextAreaField, HiddenField, PasswordField
from wtforms.widgets.html5 import DateInput
from flask_wtf import Form

from learning_journal import fields as customfields
from learning_journal import models
from learning_journal import validators as customvalidators
from learning_journal import widgets as customwidgets


date_display_fmt = '%B, %d %Y'


class RegisterForm(Form):
    """
    Registration Form
    """
    email = StringField(
        'Email',
        validators=[
            validators.DataRequired(),
            validators.Email(),
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            validators.DataRequired(),
            validators.Length(min=2),
            validators.EqualTo(
                'password2',
                message='Passwords must match'
            )
        ]
    )
    password2 = PasswordField(
        'Confirm',
        validators=[validators.DataRequired()]
    )
    blog_title = StringField(
        'Give your Learning Journal a Title. Do not include your name in it!',
        validators=[
            validators.DataRequired(),
        ]
    )
    blog_owner = StringField(
        'Now we need your Name for the Copyright Statement',
        validators=[
            validators.DataRequired(),
        ]
    )


class LoginForm(Form):
    """
    Login Form
    """
    email = StringField(
        'Email',
        validators=[
            validators.DataRequired(),
            validators.Email()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            validators.DataRequired()
        ]
    )


class EntryForm(Form):
    """
    Form for adding or updating entries
    """
    id = HiddenField()
    title = StringField(
        'Title',
        default='',
        validators=[
            validators.DataRequired(),
            validators.Length(
                max=100,
                message='The title can only be 100 characters long'),
            customvalidators.title_exists(models.Entry, 'Entry')
        ],
        filters=[lambda x: x.strip()],
    )
    date = customfields.DateField(
        'Date',
        default=datetime.datetime.now().date().strftime('%Y-%m-%d'),
        widget=DateInput()
    )
    tags = customfields.ChosenSelectField(
        "Select Tags",
        choice_func=models.get_tag_choices,
        widget=customwidgets.ChosenSelect(multiple=True))
    time_spent = customfields.TimeField(
        'Enter Time Spent as HH:MM (Hours:Minutes)',
        default='01:00',
        widget=customwidgets.TimeInput()
    )
    learned = TextAreaField(
        'Enter your markdown',
        validators=[validators.DataRequired()],
        widget=customwidgets.MarkupTextArea(cssid='learned')
    )
    resources = customfields.ChosenSelectField(
        "List Resources",
        choice_func=models.get_resource_choices,
        widget=customwidgets.ChosenSelect(multiple=True))


class ResourceForm(Form):
    """
    Form for adding or updating Resources
    """
    id = HiddenField()
    title = StringField(
        'Title',
        default='',
        validators=[
            validators.DataRequired(),
            validators.Length(
                max=100,
                message='The title can only be 100 characters long'),
            customvalidators.title_exists(models.Resource, 'Resource')
        ],
        filters=[lambda x: x.strip()],
    )
    abstract = StringField(
        'Abstract',
        default='',
        validators=[
            validators.DataRequired(),
            validators.Length(
                max=200,
                message='The abstract can only be 200 characters long'
            )
        ],
    )
    links = TextAreaField(
        'Enter description in markdown',
        validators=[
            validators.DataRequired()
        ],
        widget=customwidgets.MarkupTextArea()
    )


class TagForm(Form):
    """
    Form for adding or updating Tags
    """
    id = HiddenField()
    title = StringField(
        'Enter Tag',
        default='',
        validators=[
            validators.DataRequired(),
            validators.Length(
                max=30,
                message='The tag can only be 30 characters long'),
            customvalidators.title_exists(models.Tag, 'Tag')
        ],
        filters=[lambda x: x.strip()],
    )
    description = TextAreaField(
        'Enter description in markdown',
        validators=[
            validators.DataRequired()
        ],
        widget=customwidgets.MarkupTextArea()
    )


class ConfirmDeleteForm(Form):
    """
    Form without fields to confirm deletion of Database records
    """
    pass
