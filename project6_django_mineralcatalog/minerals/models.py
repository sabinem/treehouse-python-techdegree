"""
This file contains the model for the minerals app
"""
import os
import re
from collections import defaultdict

from django.db import models


GROUP_CHOICES = (
    ('su', 'Sulfates'),
    ('ar', 'Arsenates'),
    ('ca', 'Carbonates'),
    ('sd', 'Sulfides'),
    ('sa', 'Sulfosalts'),
    ('ne', 'Native Elements'),
    ('ph', 'Phosphates'),
    ('om', 'Organic Minerals'),
    ('ot', 'Other'),
    ('si', 'Silicates'),
    ('bo', 'Borates'),
    ('ha', 'Halides'),
    ('ox', 'Oxides'),
)


class Mineral(models.Model):
    """Model for a Mineral, see Readme File for Details on the Data."""
    name = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=255)
    image_caption = models.TextField()
    image_filename = models.CharField(max_length=255, blank=True)
    group = models.CharField(max_length=2, choices=GROUP_CHOICES)
    formula = models.TextField(blank=True)
    strunz_classification = models.CharField(max_length=255, blank=True)
    crystal_system = models.CharField(max_length=255, blank=True)
    mohs_scale_hardness = models.CharField(max_length=255, blank=True)
    luster = models.CharField(max_length=255, blank=True)
    color = models.CharField(max_length=255, blank=True)
    specific_gravity = models.CharField(max_length=255, blank=True)
    cleavage = models.CharField(max_length=255, blank=True)
    diaphaneity = models.CharField(max_length=255, blank=True)
    crystal_habit = models.CharField(max_length=255, blank=True)
    streak = models.CharField(max_length=255, blank=True)
    optical_properties = models.CharField(max_length=255, blank=True)
    refractive_index = models.CharField(max_length=255, blank=True)
    unit_cell = models.CharField(max_length=255, blank=True)
    crystal_symmetry = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['name', ]

    @classmethod
    def attributes_weighted(cls):
        """returns a weigthed list of fields for this module:
        It sorts the field by the number of their occurence
        in the data"""
        occurences = defaultdict(int)
        minerals = Mineral.objects.all()
        exclude_fields = ['id', 'name',  'image_filename',  'image_caption']
        relevant_fields = [
            field
            for field in cls._meta.get_fields()
            if field.name not in exclude_fields
        ]
        for mineral in minerals:
            for field in relevant_fields:
                if getattr(mineral, field.name) != '':
                    occurences[field.name] += 1
        fields_sorted = []
        for key in sorted(occurences, key=occurences.get, reverse=True):
            fields_sorted.append(key)
        return fields_sorted

    @property
    def image_path(self):
        """returns the path for the image. Only the filename is
        stored in the database."""
        if self.image_filename != '':
            return os.path.join('minerals', 'images', self.image_filename)
        else:
            return None

    @property
    def short_name(self):
        """returns a short name of the mineral,
        which is usually the first word in the name."""
        return re.match('^[\w]+', self.name).group(0)

    @property
    def url_name(self):
        """the url_name is the short name in lower case"""
        return self.short_name.lower()

    def __str__(self):
        """the mineral is represented by its short name in outputs"""
        return self.short_name
