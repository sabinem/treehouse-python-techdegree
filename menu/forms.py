"""forms for the menu app"""
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.forms import ValidationError

from . import models


class MenuForm(forms.ModelForm):
    """form to edit or create a menu"""
    expiration_date = forms.DateTimeField(
        widget=SelectDateWidget(years=range(2017, 2030))
    )
    items = forms.ModelMultipleChoiceField(
        queryset=models.Item.objects.all(),
        widget=forms.SelectMultiple()
    )

    class Meta:
        model = models.Menu
        fields = ('season', 'items', 'expiration_date')

    def clean(self):
        """the year appearing in the name of the season
        should not be after the year of the expire date"""
        data = self.cleaned_data
        if 'season' in self.cleaned_data:
            season, year = models.validate_season(self.cleaned_data['season'])
            if year and year.year > self.cleaned_data['expiration_date'].year:
                raise ValidationError(
                    "Year of the Season '%d' cannot be after "
                    "the expiration date '%d'"
                    % (year.year, self.cleaned_data['expiration_date'].year))
        return data
