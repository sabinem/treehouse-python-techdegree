"""
forms for the minerals app
"""
from django import forms

from . import models


class SearchForm(forms.Form):
    """Searchform: combines 3 kind of searches:
    - fulltext search for a searchterm
    - search for a specific gravity range
    - search for a chemical element to be part
      of the minerals formula
    """
    searchterm = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'size': 100,
                'type': 'text',
                'placeholder': 'searchterm'
            }
        ),
        label="Fulltext Search in Mineral's Attributes"
    )
    gravity_from = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
           attrs={
               'min': 0,
               'max': 14,
               'step': 1,
               'id': 'input-gravity-from',
               'placeholder': 0,
           }
        ),
        label="Specific Gravity Range"
    )
    gravity_to = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                'min': 0,
                'max': 14,
                'step': 1,
                'id': 'input-gravity-to',
                'placeholder': 14,
            })
    )
    chemical_element = forms.ModelChoiceField(
        queryset=models.ChemicalElement.objects.all(),
        required=False,
        label="Formula includes Chemical Element",
    )
