"""
custom forms for User Authentication
"""
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth import forms as authforms


class UserCreationForm(authforms.UserCreationForm):
    """
    signup form
    - custom error messages and widget settings for user creation form
    - password remains if it is wrong
    - djangos password validation is customized,
      so that the errors in the password
      pick are shown as errors of password1
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(
            render_value=True,
            attrs={
                'pattern':
                    "(?=^.{14,}$)(?=.*\d)(?=.*\W+)"
                    "(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$",
                'title':
                    "expected: uppercase, lowercase, number and "
                    "special character "
                    "and it must be at least 14 characters long"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(render_value=True),
        strip=False,
        help_text=("Enter the same password as before, for verification."),
        error_messages={
            'required': "You must confirm the password"
        }
    )

    def clean_password1(self):
        """validates the new password"""
        password1 = self.cleaned_data.get('password1')
        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(password1, self.instance)
        return password1

    def clean_password2(self):
        """validates the confirmation of the new password"""
        # TODO: Check signup form
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2


class AuthenticationForm(authforms.AuthenticationForm):
    """
    signin form
    - custom error messages and widget settings for user authentication form
    - password remains if it is wrong
    - form focuses on first field
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
            "Please enter a correct %(username)s and password. "
            "Note that both "
            "fields may be case-sensitive."
        ),
    }


class PasswordChangeForm(authforms.PasswordChangeForm):
    """
    A form that lets a user change their password by entering their old
    password.
    - djangos password validation is customized,
      so that the errors in the password
      pick are shown as errors of new_password1
    """
    error_messages = dict(authforms.SetPasswordForm.error_messages, **{
        'password_incorrect':
            ("Your old password was entered incorrectly. "
             "Please enter it again."),
    })
    old_password = forms.CharField(
        label=("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True},
                                   render_value=True),
    )
    new_password1 = forms.CharField(
        label=("New password"),
        widget=forms.PasswordInput(
            render_value=True,
            attrs={
                'pattern':
                    "(?=^.{14,}$)(?=.*\d)(?=.*\W+)"
                    "(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$",
                'title':
                    "expected: uppercase, lowercase, number and "
                    "special character "
                    "and it must be at least 14 characters long"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput,
    )
    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_new_password1(self):
        """validates the new password"""
        password1 = self.cleaned_data.get('new_password1')
        password_validation.validate_password(password1, self.user)
        return password1

    def clean_new_password2(self):
        """validates the confirmation of the new password"""
        # TODO: Check signup form
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2
