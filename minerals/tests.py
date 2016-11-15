from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone
from django.template import Context, Template

from .models import Mineral, GROUP_CHOICES
from .templatetags import minerals_extras
import re


class MineralViewsTests(TestCase):
    def setUp(self):
        self.minerals = Mineral.objects.all()
        self.mineral = Mineral.objects.get(pk=12)

    def test_mineral_list_view(self):
        resp = self.client.get(reverse('minerals:list'))
        self.assertEqual(resp.status_code, 200)
        for mineral in self.minerals:
            self.assertIn(self.mineral, resp.context['minerals'])
            self.assertContains(resp, self.mineral.name.split('-')[0])
        self.assertTemplateUsed(resp, 'minerals/mineral_list.html')

    def test_mineral_detail_view(self):
        resp = self.client.get(reverse('minerals:detail',
                                       kwargs={'pk': self.mineral.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.mineral, resp.context['mineral'])

    def test_mineral_detail_view_404(self):
        resp = self.client.get(reverse('minerals:detail',
                                       kwargs={'pk': 5000}))
        self.assertEqual(resp.status_code, 404)


class MineralModelTests(TestCase):
    def setUp(self):
        self.mineral = Mineral.objects.create(
            name = 'mineral1',
            category = 'something',
            image_caption = 'some caption',
            image_filename = 'some_filename.jpg',
            group = 'su',
        )

    def test_attributes_weigthed(self):
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
            'refractive_index',])
        self.assertSetEqual(set(fields[-2:]), {
            'unit_cell',
            'crystal_symmetry',
        })

    def test_image_path(self):
        self.assertEqual(self.mineral.image_path(), 'minerals/images/some_filename.jpg')

    def test___str__(self):
        self.assertEqual(str(self.mineral), self.mineral.name)

    def test_file_exists(self):
        self.assertTrue(self.mineral.image_path())

class MineralFilterTests(TestCase):

    def test_truncate_mineral_name(self):
        self.assertEqual(minerals_extras.truncate_mineral_name('Mineral1-(Y3) Mineral1-(X)'), 'Mineral1')

    def test_capitalize(self):
        self.assertEqual(minerals_extras.capitalize('mohs scale hardness'), 'Mohs Scale Hardness')

class MineralTemplateTagTests(TestCase):

    def setUp(self):
        self.minerals = Mineral.objects.all()
        self.mineral = Mineral.objects.get(pk=12)

    def render_template(self, string, context=None):
        context = context or {}
        context = Context(context)
        return Template(string).render(context)

    def test_random_mineral(self):
        rendered = self.render_template(
            '{% load minerals_extras %}'
            '{% random_mineral %}'
        )
        pk = int(re.search(r'([\d]+)', rendered).group(0))
        self.assertTrue(Mineral.objects.filter(pk=pk).exists())

    def test_mineral_fields(self):
        rendered = self.render_template(
            '{% load minerals_extras %}'
            '{% mineral_fields mineral=mineral %}',
            context = {'mineral': self.mineral}
        )
        fields = Mineral.attributes_weighted()
        print(fields)
        matches = re.findall('<td class="mineral__category">([\w\s]+)</td>', rendered)
        print(rendered)
        print(matches)

