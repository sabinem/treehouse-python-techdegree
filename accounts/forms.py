import unicodedata

from django import forms
from django.contrib.auth import password_validation, get_user_model, authenticate
from django.contrib.auth.models import User
from django.contrib.auth import forms as authforms
from django.utils.text import capfirst


class UserCreationForm(authforms.UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(
            render_value=True,
            attrs={'pattern': "(?=^.{14,}$)(?=.*\d)(?=.*\W+)(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$",
                   'title': "expected: uppercase, lowercase, number and special character "
                            "and it must be at least 14 characters long"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=("Enter the same password as before, for verification."),
    )



class AuthenticationForm(authforms.AuthenticationForm):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = authforms.UsernameField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True}),
    )
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(render_value=True),
    )

    error_messages = {
        'invalid_login': (
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
    }































