"""Tests for the minerals app
The Database is filled with data by the datamigrations,
Therefore testdata is already available and must not be
created.
"""
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.template import Context, Template

from .models import Mineral
from .templatetags import minerals_extras
import re


class MineralViewsTests(TestCase):
    """Tests the Views"""
    def setUp(self):
        """All Minearls and a specific mineral
        are fetched from the database"""
        self.minerals = Mineral.objects.all()
        self.mineral = Mineral.objects.get(pk=12)

    def test_mineral_list_view(self):
        """The list view should show all minerals.
        For each mineral its
        short name is displayed."""
        resp = self.client.get(reverse('minerals:list'))
        self.assertEqual(resp.status_code, 200)
        for mineral in self.minerals:
            self.assertIn(self.mineral, resp.context['minerals'])
            self.assertContains(resp, self.mineral.short_name)
        self.assertTemplateUsed(resp, 'minerals/mineral_list.html')

    def test_mineral_detail_view(self):
        """with the url_name of the mineral
        the detail view can be loaded."""
        resp = self.client.get(reverse(
            'minerals:detail',
            kwargs={'name': self.mineral.url_name}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.mineral, resp.context['mineral'])

    def test_mineral_detail_view_404(self):
        """the 404 error case is tested"""
        resp = self.client.get(reverse(
            'minerals:detail',
            kwargs={'name': 'nothing'}))
        self.assertEqual(resp.status_code, 404)


class MineralModelTests(TestCase):
    """Tests the Model Mineral"""
    def setUp(self):
        self.mineral = Mineral.objects.create(
            name='mineralxy-1',
            category='something',
            image_caption='some caption',
            image_filename='some_filename.jpg',
            group='su',
        )

    def test_attributes_weigthed(self):
        """Attributes are returned in order of
        how often they occur"""
        fields = Mineral.attributes_weighted()
        self.assertListEqual(fields[:-2], [
            'group',
            'formula',
            'category',
            'strunz_classification',
            'crystal_system',
            'mohs_scale_hardness',
            'luster',
            'color',
            'specific_gravity',
            'cleavage',
            'diaphaneity',
            'crystal_habit',
            'streak',
            'optical_properties',
            'refractive_index', ])
        self.assertSetEqual(set(fields[-2:]), {
            'unit_cell',
            'crystal_symmetry',
        })

    def test_image_path(self):
        """the minerals image path is returned"""
        self.assertEqual(
            self.mineral.image_path,
            'minerals/images/some_filename.jpg')

    def test___str__(self):
        """the mineral is represented by its short name"""
        self.assertEqual(
            str(self.mineral),
            'mineralxy')


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
        """all minerals and a special mineral are set up"""
        self.minerals = Mineral.objects.all()
        self.mineral = Mineral.objects.get(pk=12)

    def render_template(self, string, context=None):
        """helper function to render a template.
        This is no test!"""
        context = context or {}
        context = Context(context)
        return Template(string).render(context)

    def test_random_mineral(self):
        """returns a random mineral link"""
        rendered = self.render_template(
            '{% load minerals_extras %}'
            '{% random_mineral %}'
        )
        match = re.search(r'(?<=href="/)\w+', rendered)
        url_name = match.group(0)
        self.assertTrue(
            Mineral.objects.filter(name__startswith=url_name).exists())

    def test_mineral_fields(self):
        """returns attributes of a mineral in a template"""
        rendered = self.render_template(
            '{% load minerals_extras %}'
            '{% mineral_fields mineral=mineral %}',
            context={'mineral': self.mineral}
        )
        fields = Mineral.attributes_weighted()
        fields_capitalized = [minerals_extras.capitalize(' '.join(field.split('_')))
                              for field in fields]
        matches = re.findall(
            '<td class="mineral__category">([\w\s]+)</td>',
            rendered)
        for match in matches:
            self.assertIn(match, fields_capitalized)
