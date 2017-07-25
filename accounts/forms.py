from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

#TODO modelformfactory ausprobieren
from django.forms.models import modelformset_factory
from django.forms.formsets import BaseFormSet

from teambuilder.models import Skill, Project


class UserCreateForm(UserCreationForm):
    """Form to create a new user
    for the custom user model
    that the accounts app employs"""
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'placeholder': 'Email Address'}
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(render_value=True, attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(render_value=True, attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        """uses custom user model"""
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
        widget=forms.PasswordInput(render_value=True, attrs={'placeholder': 'Password'}))

    class Meta:
        """uses custom user model
        """
        fields = ("email", "password")
        model = get_user_model()


class ProfileForm(forms.ModelForm):
    """Form for updating the UserProfile"""
    name = forms.CharField(
            label='First Name',
            required=False,
            widget=forms.TextInput(
                attrs={'placeholder': 'Name',
                       'class': 'circle--input--h1'})
        )
    bio = forms.CharField(
        label='About You',
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Tell us about yourself ...',
                'style': 'resize: both; overflow: auto;',
            }
        )
    )
    avatar = forms.ImageField()

    class Meta:
        """uses custom user model"""
        model = get_user_model()
        fields = ['name', 'bio', 'avatar']
        labels = {
            'avatar':'Your Photo',
        }


class SkillForm(forms.ModelForm):
    """Form for entering skills"""
    skill = forms.ModelChoiceField(
        queryset=Skill.objects.all(),
        required=False)

    class Meta:
        """based on the Skill model"""
        model = Skill
        fields = ['skill']


# a formset is employed for entering skills
SkillsFormSet = forms.formset_factory(
    SkillForm)


class ProjectForm(forms.Form):
    """Project form"""
    title = forms.CharField(
        max_length=255)
    link = forms.URLField(
        widget=forms.URLInput(attrs={
            'placeholder': 'URL',
        }),
        required=False)
    id = forms.IntegerField(required=False)


# a formset is employed for entering projects
ProjectsFormSet = forms.formset_factory(ProjectForm)

# TODO modelformfactory ist noch nicht im Einsatz
ProjectsModelFormSet = forms.modelformset_factory(
    Project, fields=('title', 'link'), form=ProjectForm)