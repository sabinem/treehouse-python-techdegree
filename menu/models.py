"""models for the menu app"""
from datetime import datetime

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


SEASON_AUTMN = "Autumn"
SEASON_FALL = "Fall"
SEASON_HOT = "Hot"
SEASON_COOL = "Cool"
SEASON_SUMMER = "Summer"
SEASON_SPRING = "Spring"
SEASON_WINTER = "Winter"
SEASON_ALLYEAR = "Allyear"
SEASON_CHOICES = [
    SEASON_AUTMN,
    SEASON_SPRING,
    SEASON_SUMMER,
    SEASON_WINTER,
    SEASON_FALL,
    SEASON_COOL,
    SEASON_HOT,
    SEASON_ALLYEAR
]


def get_season_from_date(date):
    """the season is determined from a given date
    this is just needed to have a default for
    correcting the data in the database at migration"""
    if date.month in range(3, 6):
        season = SEASON_SPRING
    elif date.month in range(6, 9):
        season = SEASON_SUMMER
    elif date.month in range(9, 12):
        season = SEASON_AUTMN
    else:
        season = SEASON_WINTER
    return season + " " + str(date.year)


def validate_season(value):
    """the season should contain a year and a season"""
    parts = value.split(" ")
    year = None
    season = parts[0]
    if season not in SEASON_CHOICES:
        raise ValidationError(
            ('Expected "Spring 2017": %s is not a season' % parts[0]),
        )
    if len(parts) > 1:
        try:
            year = datetime.strptime(parts[1], '%Y')
        except ValueError:
            raise ValidationError(
                ('Expected "Spring 2017": %s is not a year' % parts[1]),
            )
    return season, year


class Menu(models.Model):
    """ a menu consists of items"""
    season = models.CharField(
        'Season',
        max_length=20,
        help_text="please provide a season and a year:"
                  " possible seasons are ''Autumn', 'Fall'"
                  " 'Hot, 'Cool, 'Summer', 'Spring' 'Winter', 'Allyear'",
        validators=[validate_season])
    items = models.ManyToManyField(
        'Item',
        related_name='items',
        help_text="please chose some items")
    created_date = models.DateField(
        auto_now_add=True)
    expiration_date = models.DateField(
        'Expiration Date',
        blank=True,
        null=True,
        help_text="when will this menu expire?")

    class Meta:
        ordering = ['expiration_date']

    def __str__(self):
        """a menu is represented by its season"""
        return self.season


class Item(models.Model):
    """a menu item has ingredients
    and a chef
    """
    name = models.CharField(max_length=200)
    description = models.TextField()
    chef = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateField(
        auto_now_add=True)
    standard = models.BooleanField(default=False)
    ingredients = models.ManyToManyField('Ingredient')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """ingredients for menu items"""
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
