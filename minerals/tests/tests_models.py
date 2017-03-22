"""
Tests for the minerals app's models
---------------------------------------------------------
- The Database is filled with data by the datamigrations,
Therefore testdata is already available and must not be
created.
"""
import os
import re

from django.test import TestCase
from django.conf import settings
from django.utils.text import slugify

from ..models import Mineral, ChemicalElement
from minerals.views import SearchParams


class MineralModelTests(TestCase):
    """Tests the Model Mineral"""
    def setUp(self):
        """a mineral is set up"""
        self.mineral = Mineral.minerals.first()

    def test_attributes_weigthed(self):
        """returns attributes in order of
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
        imgfile = os.path.join(settings.MINERALS_STATIC_DIR, self.mineral.image_path)
        self.assertTrue(
            os.path.isfile(imgfile)
        )

    def test___str__(self):
        """the mineral is represented by its name"""
        self.assertEqual(
            str(self.mineral),
            self.mineral.name)

    def test_get_gravity_bounds(self):
        """
        extracts specific gravity bounds correctly from the input data
        for specific gravity
        """
        self.assertEqual(
            Mineral.get_gravity_bounds('5.8–6.2 (meas.); 6.37 (calc.)'),
            (5.8, 6.37)
        )
        self.assertEqual(
            Mineral.get_gravity_bounds('1 - 2.6'),
            (1.0, 2.6)
        )
        self.assertEqual(
            Mineral.get_gravity_bounds('1.993'),
            (1.993, 1.993)
        )
        self.assertEqual(
            Mineral.get_gravity_bounds( '3.564 (Fo100); 3.691 (Fo90); 4.845 (Fa100)'),
            (3.564, 4.845)
        )
        self.assertEqual(
            Mineral.get_gravity_bounds('7000352000000000000♠3.52±0.01',),
            (3.52, 3.52)
        )
        self.assertEqual(
            Mineral.get_gravity_bounds('Whiteite-(CaFeMg) 2.58Whiteite-(MnFeMg)2.67Whiteite-(CaMnMg)2.63'),
            (2.58, 2.67)
        )
        self.assertEqual(
            Mineral.get_gravity_bounds('3'),
            (3,3)
        )
        self.assertEqual(
            Mineral.get_gravity_bounds('3.41\xa0g/cm3'),
            (3.41, 3.41)
        )

    def test_get_gravity_bounds_for_blank_input(self):
        """
        sets the bound to None, if the mineral has no specific gravity attribute
        """
        self.assertTupleEqual(
            Mineral.get_gravity_bounds(''), (None, None)
        )

    def test_group_slug(self):
        """for all groups a slug is derived from the group
        it should be possible to recover the group from that slug"""
        groups = Mineral.minerals.order_by('group')\
            .values_list('group', flat=True).distinct()
        for group in groups:
            slug = Mineral.get_group_slug(group)
            group_from_slug = Mineral.get_group_from_slug(slug)
            self.assertEquals(
                group, group_from_slug
            )

    def test_get_search_letter_letter(self):
        """a normal search letter is returned as is"""
        self.assertEqual(
            Mineral.get_search_letter("c"), "c"
        )

    def test_get_search_letter_default(self):
        """when no search letter is given 'a' is returned"""
        self.assertEqual(
            Mineral.get_search_letter(), settings.MINERALS_DEFAULT_LIST_LETTER
        )


class MineralManagerTests(TestCase):
    """tests the minerals querysets"""
    def setUp(self):
        """one minerals and all minerals are set up"""
        self.all_minerals = Mineral.minerals.all()
        self.one_mineral = Mineral.minerals.first()

    def test_get_minerals_by_group(self):
        """the minerals for a group are determined correctly"""
        group = self.one_mineral.group
        test_qs = Mineral.minerals.get_minerals_by_group(group)
        self.assertListEqual(
            list(test_qs),
            [m for m in self.all_minerals if m.group == group]
        )

    def test_get_minerals_for_letter(self):
        """the minerals for a letter are determined correctly"""
        letter = "b"
        test_qs = Mineral.minerals.get_minerals_for_letter(letter)
        self.assertListEqual(
            list(test_qs),
            [m for m in self.all_minerals if slugify(m.name[0]) == letter]
        )

    def test_get_mineral_from_slug_exists(self):
        """the mineral can be derived from its slug"""
        mineral = self.one_mineral
        test_mineral_get = Mineral.minerals.get_mineral_from_slug(mineral.mineral_slug)
        self.assertEqual(
            mineral, test_mineral_get
        )

    def test_filter_minerals_by_id_list(self):
        """minerals can be found form an id_list"""
        id_list = [m.id for m in self.all_minerals[0:10]]
        test_qs = Mineral.minerals.filter_minerals_by_id_list(id_list)
        self.assertSetEqual(
            set([m.id for m in test_qs]), set(id_list)
        )

    def test_filter_minerals_by_chem_element_one_letter(self):
        """minerals for a one letter chemical element are determined correctly"""
        test_qs = Mineral.minerals.filter_minerals_by_chem_element("F")
        self.assertSetEqual(
            set([(m.name, m.formula) for m in self.all_minerals if re.search(r'F[^a-z]', m.formula)]),
            set([(m.name, m.formula) for m in test_qs])
        )

    def test_filter_minerals_by_chem_element_two_letter(self):
        """minerals for a two letter chemical element are determined correctly"""
        test_qs = Mineral.minerals.filter_minerals_by_chem_element("Fe")
        self.assertSetEqual(
            set([(m.name, m.formula) for m in self.all_minerals if re.search(r'Fe[^a-z]', m.formula)]),
            set([(m.name, m.formula) for m in test_qs])
        )

    def test_get_random_mineral(self):
        """a random mineral is returned"""
        test_mineral_get = Mineral.minerals.get_random_mineral()
        self.assertIn(test_mineral_get.id, [m.id for m in self.all_minerals])

    def test_get_ordered_groups(self):
        """the groups are returned with 'Other'
        at the last position"""
        test_list = Mineral.minerals.get_ordered_groups()
        groups = {m.group for m in self.all_minerals}
        self.assertEqual(len(test_list),len(groups))
        self.assertEqual(test_list[-1], "Other" )

    def test_filter_minerals_by_searchterm(self):
        """the fulltext search in the mineral attributes returns
        a record correctly, if the searchterm appears in one of its
        fields"""
        mineral = self.one_mineral
        for field in mineral._meta.fields:
            if hasattr(mineral, field.name):
                if field.name not in ['id', 'image_filename']:
                    term = str(getattr(mineral, field.name))[3:12]
                    test_qs = Mineral.minerals.filter_minerals_by_searchterm(term)
                    self.assertIn(
                        mineral.id,
                        [m.id for m in test_qs]
                    )

    def test_filter_minerals_by_specific_gravity_exact(self):
        """the mineral is found if search for its excact specific
        gravity range"""
        mineral = Mineral.minerals.exclude(specific_gravity="").first()
        gravity_bounds = Mineral.get_gravity_bounds(mineral.specific_gravity)
        test_qs = Mineral.minerals.filter_minerals_by_specific_gravity(gravity_bounds)
        self.assertIn(
            mineral.id,
            [m.id for m in test_qs]
        )

    def test_filter_minerals_by_specific_gravity_example(self):
        """minerals are determined correctly for a specific gravity range"""
        gravity_bounds = (6,8)
        test_qs = Mineral.minerals.filter_minerals_by_specific_gravity(gravity_bounds)
        expected_mineral_ids = \
            [m.id for m in Mineral.minerals.exclude(specific_gravity="")
             if (float(Mineral.get_gravity_bounds(m.specific_gravity)[0]) <= 8 and
                 float(Mineral.get_gravity_bounds(m.specific_gravity)[1]) >= 6)]
        mineral = Mineral.minerals.exclude(specific_gravity="").first()
        self.assertEqual(
            set(expected_mineral_ids),
            {m.id for m in test_qs}
        )

    def test_get_minerals_from_search_params_term(self):
        """minerals are determined correctly from the searchparameters
        in case of just a search term"""
        search_params = SearchParams("Ab", None, None)
        qs_test = Mineral.minerals.get_minerals_from_search_params(
            search_params
        )
        expected_qs = Mineral.minerals.filter_minerals_by_searchterm(search_params.searchterm)
        self.assertSetEqual(
            {m.id for m in qs_test},
            {m.id for m in expected_qs}
        )

    def test_get_minerals_from_search_params_chem_element(self):
        """minerals are determined correctly from the searchparameters
        in case of just a chemical element"""
        search_params = SearchParams(None, "Na", None)
        qs_test = Mineral.minerals.get_minerals_from_search_params(
            search_params
        )
        expected_qs = Mineral.minerals.filter_minerals_by_chem_element("Na")
        self.assertSetEqual(
            {m.id for m in qs_test},
            {m.id for m in expected_qs}
        )

    def test_get_minerals_from_search_params_gravity_bound(self):
        """minerals are determined correctly from the searchparameters
        in case of just a specific gravity bound"""
        search_params = SearchParams(None, None, (7,9))
        qs_test = Mineral.minerals.get_minerals_from_search_params(
            search_params
        )
        expected_qs = Mineral.minerals.filter_minerals_by_specific_gravity((7,9))
        self.assertSetEqual(
            {m.id for m in qs_test},
            {m.id for m in expected_qs}
        )

    def test_get_minerals_from_search_params_combination(self):
        """minerals are determined correctly from the searchparameters
        in case of a combined search"""
        search_params = SearchParams("Ab", "Fe", (2,7))
        qs_test = Mineral.minerals.get_minerals_from_search_params(
            search_params
        )
        expected_qs1 = Mineral.minerals.filter_minerals_by_searchterm("Ab")
        expected_qs2 = Mineral.minerals.filter_minerals_by_specific_gravity((2, 9))
        expected_qs3 = Mineral.minerals.filter_minerals_by_chem_element("Fe")
        self.assertSetEqual(
            {m.id for m in qs_test},
            {m.id for m in expected_qs1
             if (m in expected_qs2 and m in expected_qs3)}
        )


