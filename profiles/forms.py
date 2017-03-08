import datetime
from django import forms
from django.contrib.auth.models import User
from django.utils.html import escape, strip_tags

from . import models


def check_confirm_email(email, instance):
    if instance.pk is None:
        return True
    elif email != instance.email:
        return True
    return False


class UserForm(forms.ModelForm):
    """
    User Form as part of the Userprofile Form
    - the email confirm field is only shown when
      the user changes the email address
    """
    email_confirm = forms.EmailField(
        required=False,
        help_text="In case you change your email, "
                  "please confirm the email address in the field above",
        label="Please confirm your email address"
    )
    first_name = forms.CharField(
        required=True,
        max_length=30,
        label=("First name"),
    )
    last_name = forms.CharField(
        required=True,
        max_length=30,
        label=("Last name"),
    )
    email = forms.EmailField(
        required=True,
        label="Email"
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean(self):
        """
        the email confirm field is checked if the user changes the email
        or when
        """
        cleaned_data = super(UserForm, self).clean()
        if 'email' in cleaned_data:
            if check_confirm_email(cleaned_data['email'], self.instance):
                if cleaned_data['email_confirm'] == "":
                    raise forms.ValidationError(
                        {"email_confirm":
                            "change of email requires confirmation"}
                    )
                if cleaned_data['email'] != cleaned_data['email_confirm']:
                    raise forms.ValidationError(
                        {"email_confirm":
                            "email changed, but confirmation does not match"}
                    )
        return cleaned_data


class ProfileForm(forms.ModelForm):
    """
    Profile Form
    - the date input format is checked by "input_formats"
    """
    default_error_messages = {
        'required': u'Value required!!!!.',
    }

    class Meta:
        model = models.Profile
        fields = (
            'avatar',
            'date_of_birth',
            'bio',
            'show_birthday',
            'show_email',
        )
        input_formats = {
            'date_of_birth': ['%m.%d.%Y', '%Y-%m-%d', '%m.%d.%y']
        }
        labels = {
            'date_of_birth': "Date of Birth",
            'bio': "Biography",
            'avatar': "Avatar",
            'show_email': "Email visibility",
            'show_birthday': "Birthday visibility",
        }
        help_texts = {
            'date_of_birth':
                "Allowed formats are: YYYY-MM-DD, MM/DD/YYYY or MM/DD/YY",
            'bio': "Please write something about yourself",
            'avatar':
                """<ul><li>You can choose an image from
                your Desktop and uplaod it.</li>
                <li>Later on you can edit your avatar
                and make it look cool.</li></ul>""",
            'show_email': "you can keep your email private or"
                          " show it to other Circle users",
            'show_birthday': "you can keep your birthday private"
                             " or show it to other Circle users",
        }
        error_messages = {
            'date_of_birth': {
                'required': "Please provide your date of birth!",
            },
        }

    def clean_bio(self):
        """
        check the bio form field
        - HTML tags are not allowed
        - it must be at least 10 characters long
        """
        data = self.cleaned_data['bio']
        escaped_data = escape(data)
        stripped_data = strip_tags(data)
        if escaped_data != data or stripped_data != data:
            raise forms.ValidationError("Html-Tags are not allowed here")
        if len(data) < 10:
            raise forms.ValidationError(
                "You must write at least 10 characters.")
        return stripped_data

    def clean_date_of_birth(self):
        """
        check the birthdate
        - it should not be in the future
        """
        data = self.cleaned_data['date_of_birth']
        if data > datetime.date.today():
            corrected_data = data.replace(year=data.year-100)
            return corrected_data
        return data


class AvatarForm(forms.Form):
    """
    Form for transforming the Avatar
    """
    FLIP_LEFT_RIGHT = 'lr'
    FLIP_TOP_BOTTOM = 'tb'
    ROTATE = 'r'
    CROP = 'c'
    WELCOME = 'w'
    ACTION_CHOICES = (
        (ROTATE, "rotate"),
        (FLIP_LEFT_RIGHT, 'flip left right'),
        (FLIP_TOP_BOTTOM, 'flip top bottom'),
        (CROP, 'crop'),
        (WELCOME, 'Welcome to styling your avatar'),
    )
    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        required=False,
        initial=WELCOME,
        label=("Action"),
        widget=forms.Select(),
        help_text="Please chose an action and save when you are done",
    )
    rotate = forms.IntegerField(
        required=False,
        label="",
        widget=forms.NumberInput(attrs={
            'id': "angleInputId",
            'type': 'range',
            'min': 0,
            'max': 360,
            'step': 1,
            'value': 0,
            'oninput': "angleOutputId.value = angleInputId.value"
        })
    )
    crop_left = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput,
        initial=0,
    )
    crop_top = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput,
        initial=0,
    )
    crop_right = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput,
        initial=0,
    )
    crop_bottom = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput,
        initial=0,
    )

    def clean(self):
        """
        the email confirm field is checked if the user changes the email
        """
        cleaned_data = super(AvatarForm, self).clean()
        if cleaned_data['action'] == self.CROP:
            if (cleaned_data['crop_top'] == 0 and
                cleaned_data['crop_bottom'] == 0 and
                cleaned_data['crop_left'] == 0 and
                cleaned_data['crop_right'] == 0):
                raise forms.ValidationError(
                    "You must select an error on your image, "
                    "if you want to crop it!")
        if cleaned_data['action'] == self.ROTATE:
            if cleaned_data['rotate'] == 0:
                raise forms.ValidationError(
                    "You must select an angle, if you want to "
                    "rotate your image!"
                )
        return cleaned_data
