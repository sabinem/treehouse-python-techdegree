"""
Tests for the minerals app's template filters and tags
---------------------------------------------------------
- The Database is filled with data by the datamigrations,
Therefore testdata is already available and must not be
created.
"""
import re
import string

from django.test import TestCase
from django.template import Context, Template
from django.utils.text import slugify

from minerals.models import Mineral
from minerals.templatetags import minerals_extras


class MineralFilterTests(TestCase):
    """Tests the Template Filters"""
    def test_capitalize(self):
        """returns all words capitalized"""
        self.assertEqual(
            minerals_extras.capitalize('mohs scale hardness'),
            'Mohs Scale Hardness')


class MineralTemplateTagTests(TestCase):
    """Tests the Template Tags."""
    def setUp(self):
        """set up some example mineral"""
        self.mineral = Mineral.minerals.first()

    def render_template(self, string, context=None):
        """helper function to render a template.
        This is no test!"""
        context = context or {}
        context = Context(context)
        return Template(string).render(context)

    def test_random_mineral(self):
        """renders link to a  random mineral"""
        rendered = self.render_template(
            '{% load minerals_extras %}'
            '{% random_mineral %}'
        )
        pattern = r'href="[\w/]*/(?P<mineral>\w+)'
        match = re.search(pattern, rendered)
        url = match.group('mineral')
        self.assertEquals(
            Mineral.minerals.filter(mineral_slug=url).count(), 1)

    def test_mineral_fields(self):
        """renders attributes of a mineral in a template"""
        mineral = self.mineral
        rendered = self.render_template(
            '{% load minerals_extras %}'
            '{% mineral_fields mineral=mineral %}',
            context={'mineral': mineral}
        )
        fields = Mineral.attributes_weighted()
        fields_capitalized = \
            [minerals_extras.capitalize(' '.join(field.split('_')))
             for field in fields]
        matches = re.findall(
            '<td class="mineral__category">([\w\s]+)</td>',
            rendered)
        for match in matches:
            self.assertIn(match, fields_capitalized)

    def test_search_letter(self):
        """renders links for
        letters of the alphabet"""
        letters = string.ascii_lowercase
        search_letter = 'a'
        rendered = self.render_template(
            '{% load minerals_extras %}'
            '{% search_letter %}',
            context={'search_letter': search_letter}
        )
        for letter in letters:
            html = 'href="/' + letter + '"'
            self.assertIn(html, rendered)

    def test_search_group(self):
        """renders group links in
        the mineral group navigation"""
        groups = Mineral.minerals.get_ordered_groups()
        rendered = self.render_template(
            '{% load minerals_extras %}'
            '{% search_group %}',
        )
        for group in groups:
            html = 'href="/group/' + slugify(group) + '"'
            self.assertIn(html, rendered)

    def test_search_form(self):
        """renders search form"""
        rendered = self.render_template(
            '{% load minerals_extras %}'
            '{% search_form %}',
        )
        html = '<form'
        self.assertIn(html, rendered)
