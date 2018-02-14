"""
This file contains the model for the minerals app
"""
import os
import re
import random
from collections import defaultdict

from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.text import slugify


class MineralManager(models.Manager):
    """querysets for Minerals"""
    def get_minerals_by_group(self, group):
        """get queryset of minerals that belog to
         a group"""
        return self.filter(group=group)

    def get_minerals_for_letter(self, letter):
        """return queryset of minerals
        that have a name that starts with a
        letter: note that the slug is evaluated instead of the
        mineral name since some minerals start with a special
        letter"""
        return self.filter(mineral_slug__startswith=letter)

    def get_mineral_from_slug(self, mineral_slug):
        """get mineral from its slug"""
        return get_object_or_404(self, mineral_slug=mineral_slug)

    def get_random_mineral(self):
        """return a random mineral"""
        mineral_ids = self.values_list('id', flat=True)
        random_pk = random.choice(mineral_ids)
        return self.get(pk=random_pk)

    def get_ordered_groups(self):
        """return a sorted list of all groups where
        the 'Other' group comes last"""
        group_nav = list(
            self.exclude(group="Other")
                .order_by('group')
                .values_list('group', flat=True)
                .distinct()
        )
        group_nav.append("Other")
        return group_nav

    def filter_minerals_by_chem_element(self, chem_element_code):
        """return queryset of minerals, where the formula
        contains a chemical element code """
        chem_pattern = chem_element_code + "[^a-z]"
        qs = self.filter(formula__contains=chem_element_code)
        exclude = [m.id for m in qs if not re.search(chem_pattern, m.formula)]
        return qs.exclude(id__in=exclude)

    def filter_minerals_by_searchterm(self, searchterm):
        """return a queryset of minerals derived by a fulltext
        search in its attributes"""
        return self.filter(
            models.Q(name__icontains=searchterm) |
            models.Q(category__icontains=searchterm) |
            models.Q(image_caption__icontains=searchterm) |
            models.Q(group__icontains=searchterm) |
            models.Q(formula__icontains=searchterm) |
            models.Q(strunz_classification__icontains=searchterm) |
            models.Q(crystal_system__icontains=searchterm) |
            models.Q(mohs_scale_hardness__icontains=searchterm) |
            models.Q(luster__icontains=searchterm) |
            models.Q(color__icontains=searchterm) |
            models.Q(specific_gravity__icontains=searchterm) |
            models.Q(cleavage__icontains=searchterm) |
            models.Q(diaphaneity__icontains=searchterm) |
            models.Q(crystal_habit__icontains=searchterm) |
            models.Q(streak__icontains=searchterm) |
            models.Q(optical_properties__icontains=searchterm) |
            models.Q(refractive_index__icontains=searchterm) |
            models.Q(unit_cell__icontains=searchterm) |
            models.Q(crystal_symmetry__icontains=searchterm)
        )

    def filter_minerals_by_specific_gravity(self, gravity_bounds):
        """read gravity bounds from the field 'special gravity' of
        minerals: this is a class method in order to avoid hitting
        the database each time the method is called"""
        gravity_from, gravity_to = gravity_bounds

        gravity_values = self.all().exclude(specific_gravity="") \
                             .values_list('id', 'specific_gravity')
        id_list = []
        for value_pair in gravity_values:
            id, specific_gravity = value_pair
            lower, upper = \
                Mineral.get_gravity_bounds(specific_gravity)
            if lower and upper:
                if gravity_from <= upper and lower <= gravity_to:
                    id_list.append(id)
        return self.filter_minerals_by_id_list(id_list)

    def filter_minerals_by_id_list(self, id_list):
        """returns queryset of minerals
        with ids in a given list"""
        return self.filter(id__in=id_list)

    def get_minerals_from_search_params(self, search_params):
        """combines querysets of minerals according to
        seacrh parameters"""
        minerals_c = minerals_s = minerals_g = self.all()
        if search_params.chem_element_code:
            minerals_c = \
                self.filter_minerals_by_chem_element(
                    search_params.chem_element_code
                )
        if search_params.searchterm:
            minerals_s = \
                self.filter_minerals_by_searchterm(
                    search_params.searchterm
                )
        if search_params.gravity_bounds:
            minerals_g = \
                self.filter_minerals_by_specific_gravity(
                    search_params.gravity_bounds
                )
        return minerals_s & minerals_c & minerals_g


class Mineral(models.Model):
    """Model for a Mineral, see Readme File for Details on the Data.
    - the data is loaded by a migration
    - the only additional field is a slug
      derived from the mineral name
    """
    name = models.CharField(max_length=255, unique=True)
    mineral_slug = models.SlugField(max_length=255, unique=True)
    category = models.CharField(max_length=255)
    image_caption = models.TextField()
    image_filename = models.CharField(max_length=255, blank=True)
    group = models.CharField(max_length=255)
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
    MAX_SPECIFIC_GRAVITY = 14
    MIN_SPECIFIC_GRAVITY = 0

    minerals = MineralManager()

    class Meta:
        ordering = ['name', ]

    @classmethod
    def attributes_weighted(cls):
        """returns a weigthed list of fields for this module:
        It sorts the field by the number of their occurence
        in the data"""
        occurences = defaultdict(int)
        minerals = cls.minerals.all()
        exclude_fields = ['id', 'name',  'image_filename',
                          'image_caption', 'mineral_slug']
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

    def __str__(self):
        """the mineral is represented by its short name in outputs"""
        return self.name

    @classmethod
    def get_gravity_bounds(cls, specific_gravity):
        """gets back gravity bounds for a specific_gravity"""
        if specific_gravity == "":
            return None, None
        else:
            integer_or_float = r'\d*\.?\d+'
            match = re.findall(integer_or_float, specific_gravity)
            bound_lower, bound_upper = None, None
            bounds = [float(x) for x in match if (float(x) < 14.0)]
            if len(bounds) > 0:
                bound_lower, bound_upper = bounds[0], bounds[0]
                if len(bounds) > 1:
                    bound_upper = max(bounds)
            return bound_lower, bound_upper

    @classmethod
    def get_group_slug(cls, group):
        """gets a slug from the group"""
        return slugify(group)

    @classmethod
    def get_group_from_slug(cls, slug):
        """get group from slug"""
        return ' '.join([word.capitalize() for word in slug.split('-')])

    @classmethod
    def get_search_letter(cls, letter=None):
        """get search_letter: return letter or provide default"""
        return letter if letter else settings.MINERALS_DEFAULT_LIST_LETTER


class ChemicalElement(models.Model):
    """Model for a Mineral, see Readme File for Details on the Data."""
    code = models.CharField(max_length=2, unique=True, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        """the mineral is represented by its short name in outputs"""
        return self.code + " - " + self.name
