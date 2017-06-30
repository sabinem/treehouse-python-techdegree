from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

#TODO modelformfactory ausprobieren
from django.forms.models import modelformset_factory
from django.forms.formsets import BaseFormSet

from teambuilder.models import Skill, Project


class UserCreateForm(UserCreationForm):
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
        fields = ("email", "password1", "password2")
        model = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'placeholder': 'Email Address'}
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(render_value=True, attrs={'placeholder': 'Password'}))

    class Meta:
        fields = ("email", "password")
        model = get_user_model()


class ProfileForm(forms.ModelForm):
    """Update UserProfile model information."""
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
        model = get_user_model()
        fields = ['name', 'bio', 'avatar']
        labels = {
            'avatar':'Your Photo',
        }


class SkillForm(forms.ModelForm):
    skill = forms.ModelChoiceField(
        queryset=Skill.objects.all(),
        required=False)

    class Meta:
        model = Skill
        fields = ['skill']


SkillsFormSet = forms.formset_factory(
    SkillForm)


class ProjectForm(forms.Form):
    title = forms.CharField(
        max_length=255)
    link = forms.URLField(
        widget=forms.URLInput(attrs={
            'placeholder': 'URL',
        }),
        required=False)
    id = forms.IntegerField(required=False)


ProjectsFormSet = forms.formset_factory(ProjectForm)

# TODO modelformfactory ist noch nicht im Einsatz
ProjectsModelFormSet = forms.modelformset_factory(
    Project, fields=('title', 'link'), form=ProjectForm)