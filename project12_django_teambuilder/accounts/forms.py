"""forms for the accounts app"""
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import (authenticate,
                                 get_user_model)

from teambuilder.models import Skill


class UserCreateForm(UserCreationForm):
    """Form to create a new user
    for the custom user model"""
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'placeholder': 'Email Address'}
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            render_value=True,
            attrs={'placeholder': 'Password'}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            render_value=True,
            attrs={'placeholder': 'Confirm Password'}
        )
    )

    class Meta:
        fields = ("email", "password1", "password2")
        model = get_user_model()


class UserLoginForm(forms.Form):
    """User login form for custom user model"""
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'placeholder': 'Email Address'}
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            render_value=True,
            attrs={'placeholder': 'Password'}
        )
    )

    class Meta:
        fields = ("email", "password")
        model = get_user_model()

    def clean(self):
        cleaned_data = super(UserLoginForm, self).clean()
        user = authenticate(
            email=cleaned_data['email'],
            password=cleaned_data['password']
        )
        if user is None:
            raise forms.ValidationError("Invalid login")


class ProfileForm(forms.ModelForm):
    """Form for updating the UserProfile"""
    name = forms.CharField(
            label='First Name',
            required=True,
            widget=forms.TextInput(
                attrs={'placeholder': 'Name',
                       'class': 'circle--input--h1'})
        )
    bio = forms.CharField(
        label='About You',
        required=True,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Tell us about yourself ...',
                'style': 'resize: both; overflow: auto;',
            }
        )
    )
    avatar = forms.ImageField(
        required=True
    )

    class Meta:
        model = get_user_model()
        fields = ['name', 'bio', 'avatar']
        labels = {
            'avatar': 'Your Photo',
        }


class SkillForm(forms.ModelForm):
    """Form for entering skills"""
    skill = forms.ModelChoiceField(
        queryset=Skill.objects.all(),
        required=False)

    class Meta:
        model = Skill
        fields = ['skill']


# a formset is employed for entering skills
SkillsFormSet = forms.formset_factory(
    form=SkillForm,
    can_delete=True,
    extra=1,
)


class ProjectForm(forms.Form):
    """Project form"""
    title = forms.CharField(
        max_length=255)
    link = forms.URLField(
        widget=forms.URLInput(attrs={
            'placeholder': 'URL',
        }),
        required=False)


# a formset is employed for entering projects
ProjectsFormSet = forms.formset_factory(ProjectForm,
                                        extra=0, can_delete=False)
