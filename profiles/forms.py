import urllib.request
import datetime
from PIL import Image
import glob, os


import io
from django.core.files.uploadedfile import InMemoryUploadedFile

from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.utils.html import escape, strip_tags
from django.forms import PasswordInput
from django.contrib.auth import password_validation
from django.contrib.auth import forms as authforms


from .models import Profile

class UserForm(forms.ModelForm):
    email_confirm = forms.EmailField(
        required=False,
        help_text="In case you change your email, please confirm the email address in the field above",
        label = "Please confirm your email address"
    )
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'email_confirm': "please confirm your email",
            'last_name': "Last name",
            'first_name': "First name",
        }
        help_texts = {
            'email_confirm': "Please repeat your email",
            'last_name': "What is your last name?",
        }

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        if self.instance.pk is not None:
            if self.instance.email != cleaned_data['email']:
                if cleaned_data['email_confirm'] == "":
                    raise forms.ValidationError(
                        {"email_confirm": "change of email requires confirmation"}
                    )
                if cleaned_data['email'] != cleaned_data['email_confirm']:
                    raise forms.ValidationError(
                        {"email_confirm": "email changed, but confirmation does not match"}
                    )
        return cleaned_data


class ProfileForm(forms.ModelForm):
    default_error_messages = {
        'required': u'Value required!!!!.',
    }
    class Meta:
        model = Profile
        fields = ('show_email', 'github_account', 'avatar', 'date_of_birth', 'show_birthday' ,'bio')
        labels = {
            'date_of_birth' : "Date of Birth",
            'bio': "Biography",
            'avatar': "Avatar",
            'show_email': "Email visibility",
            'show_birthday': "Birthday visibility",
            'github_account': "Github username",
        }
        help_texts = {
            'date_of_birth': "Allowed formats are: YYYY-MM-DD, MM/DD/YYYY or MM/DD/YY",
            'bio': "Please write something about yourself",
            'avatar': """<ul><li>You can choose an image from your Desktop and uplaod it.</li>
                      <li>Later on you can edit your avatar and make it look cool.</li></ul>""",
            'show_email': "you can keep your email private or show it to other Circle users",
            'show_birthday': "you can keep your birthday private or show it to other Circle users",
            'github_account': "Enter your github username to provide a link to your github account"
        }
        error_messages = {
            'date_of_birth': {
                'required': "Please provide your date of birth!",
            },
        }
        widget = {
            'email' : forms.widgets.EmailInput(attrs={'id': "email_input"}),
            'date_of_birth': forms.widgets.DateInput(
                format=['%m.%d.%Y', '%Y-%m-%d', '%m.%d.%y']
            )
        }


    def clean_bio(self):
        data = self.cleaned_data['bio']
        escaped_data = escape(data)
        stripped_data = strip_tags(data)
        if escaped_data != data or stripped_data != data:
            raise forms.ValidationError("Html-Tags are not allowed here")
        if len(data) < 10:
            raise forms.ValidationError("You must write at least 10 characters.")
        return stripped_data

    def clean_github_account(self):
        data = self.cleaned_data['github_account']
        if (self.instance.pk is None or
           self.instance.github_account != data):
            github_url = '/'.join(["https://github.com/", data])
            try:
                response = urllib.request.urlopen(github_url)
            except urllib.request.HTTPError:
                raise forms.ValidationError("This is not a valid Github account")
            except urllib.request.URLError:
                raise forms.ValidationError("The Internet Connection is not working. Please try again later")
        return data

    def clean_date_of_birth(self):
        data = self.cleaned_data['date_of_birth']
        if data > datetime.date.today():
            corrected_data = data.replace(year=data.year-100)
            return corrected_data
        return data

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        infile = avatar.file
        im = Image.open(infile)
        new_im = im.rotate(90).resize((128,128))
        new_im.show()
        import io
        new_im_io = io.BytesIO()
        new_im.save(new_im_io, format='JPEG')
        temp_name = avatar.name
        avatar.delete(save=False)
        from django.core.files.base import ContentFile
        avatar.save(
            temp_name,
            content=ContentFile(new_im_io.getvalue()),
            save=False
        )
        return avatar


class PasswordChangeForm(authforms.PasswordChangeForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = dict(authforms.SetPasswordForm.error_messages, **{
        'password_incorrect': ("Your old password was entered incorrectly. Please enter it again."),
    })
    old_password = forms.CharField(
        label=("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True}, render_value=True),
    )
    new_password1 = forms.CharField(
        label=("New password"),
        widget=forms.PasswordInput(
            render_value=True,
            attrs={'pattern': "(?=^.{14,}$)(?=.*\d)(?=.*\W+)(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$",
                   'title': "expected: uppercase, lowercase, number and special character "
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
        password1 = self.cleaned_data.get('new_password1')
        password_validation.validate_password(password1, self.user)
        return password1

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2