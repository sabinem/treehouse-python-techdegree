"""forms for the teambuilder app"""
from django import forms
from django.forms.models import inlineformset_factory

from . import models


class ProjectForm(forms.ModelForm):
    """Project Form"""

    class Meta:
        model = models.Project
        fields = ['title', 'description',
                  'project_timeline', 'applicant_requirements']
        labels = {
            'avatar': 'Your Photo',
        }
        widgets = {
            'applicant_requirements': forms.Textarea(
                attrs={
                    'placeholder': 'Applicant requirements',
                    'style': 'resize: both; overflow: auto;'}),
            'project_timeline': forms.Textarea(
                attrs={
                    'placeholder': 'Project Timeline',
                    'style': 'resize: both; overflow: auto;'}),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Project description...',
                    'style': 'resize: both; overflow: auto;'}),
            'title': forms.TextInput(
                attrs={'placeholder': 'Name',
                       'class': 'circle--input--h1'})
        }


class PositionForm(forms.ModelForm):
    class Meta:
        model = models.Position
        fields = ['skill', 'description']


class NewPositionForm(forms.ModelForm):
    class Meta:
        model = models.Position
        fields = ['skill', 'description']


class ProjectSearchForm(forms.Form):
    searchterm = forms.CharField(max_length=250)


# Form for Project Positions
ProjectWithPositionsFormSet = inlineformset_factory(
    models.Project,
    models.Position,
    fields=('skill', 'description'),
    labels={
        'skill': "",
        'description': ""
    },
    widgets={
        'description': forms.Textarea(
            attrs={
                'placeholder': 'Position description...',
                'style': 'resize: both; overflow: auto;'}),
    },
    can_delete=True,
    extra=1
)

NewPositionsFormset = forms.formset_factory(
    NewPositionForm)
