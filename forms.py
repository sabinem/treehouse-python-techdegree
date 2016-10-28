import datetime
from flask_wtf import Form
from wtforms import validators, StringField, \
    TextAreaField, HiddenField, PasswordField
import widgets as customwidgets
import fields as customfields
import models
from wtforms.widgets.html5 import DateInput
date_display_fmt = '%B, %d %Y'


class RegisterForm(Form):
    email = StringField(
        'Email',
        validators=[
            validators.DataRequired(),
            validators.Email(),
        ])
    password = PasswordField(
        'Password',
        validators=[
            validators.DataRequired(),
            validators.Length(min=2),
            validators.EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[validators.DataRequired()]
    )
    blog_owner = StringField(
        'Blog Owner for Copyright',
        validators=[
            validators.DataRequired(),
        ])
    blog_title = StringField(
        'Blog Title',
        validators=[
            validators.DataRequired(),
        ])


class LoginForm(Form):
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', validators=[validators.DataRequired()])


class EntryForm(Form):
    id = HiddenField()
    title = StringField(
        'Title',
        default='',
        validators=[validators.DataRequired(),
                    validators.Length(max=100,
                                      message='The title can only be 100 characters long'),
                    customfields.title_exists],
        filters=[lambda x: x.strip() ],
    )
    date = customfields.DateField(
        'Date',
        default=datetime.datetime.now().date().strftime('%Y-%m-%d'),
        widget=DateInput()
    )
    tags = customfields.ChosenSelectField(
        "Select Tags",
        choices=list(models.Tag.select().select(models.Tag.id, models.Tag.tag).tuples()),
        widget=customwidgets.ChosenSelect(multiple=True))
    time_spent = customfields.TimeField(
        'Enter Time Spent as HH:MM (Hours:Minutes)',
        default='01:00',
        widget=customwidgets.TimeInput()
    )
    learned = TextAreaField(
        'Enter your markdown',
        validators=[validators.DataRequired()],
        widget = customwidgets.MarkupTextArea(cssid='learned')
    )
    resources = customfields.ChosenSelectField(
        "List Resources",
        choices=list(models.Resource.select().select(models.Resource.id, models.Resource.title).tuples()),
        widget=customwidgets.ChosenSelect(multiple=True))


class ResourceForm(Form):
    id = HiddenField()
    title = StringField(
        'Title',
        default='',
        validators=[validators.DataRequired(),
                    validators.Length(max=100,
                                      message='The title can only be 100 characters long'),
                    customfields.title_exists],
        filters=[lambda x: x.strip() ],
    )
    abstract = StringField(
        'Abstract',
        default='',
        validators=[validators.DataRequired(),
                    validators.Length(max=200,
                                      message='The abstract can only be 200 characters long'),
                    customfields.title_exists],
        #filters=[lambda x: x.strip() ],
    )
    links = TextAreaField(
        'Enter description in markdown',
        validators=[validators.DataRequired()],
        widget=customwidgets.MarkupTextArea()
    )


class TagForm(Form):
    id = HiddenField()
    tag = StringField(
        'Enter Tag',
        default='',
        validators=[validators.DataRequired(),
                    validators.Length(max=30,
                                      message='The tag can only be 30 characters long'),
                    customfields.title_exists],
        filters=[lambda x: x.strip()],
    )
    description = TextAreaField(
        'Enter description in markdown',
        validators=[validators.DataRequired()],
        widget=customwidgets.MarkupTextArea()
    )


class ConfirmDeleteForm(Form):
    pass
