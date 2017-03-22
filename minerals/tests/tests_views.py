"""
Tests for the minerals app's detail view
---------------------------------------------------------
- The Database is filled with data by the datamigrations,
Therefore testdata is already available and must not be
created.
"""
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.text import slugify

from minerals.models import Mineral, ChemicalElement
from minerals.views import SearchParams, get_search_params_from_request


class MineralDetailViewTests(TestCase):
    """Tests the Mineral DetailView"""
    def setUp(self):
        """set up some example mineral"""
        self.mineral = Mineral.minerals.first()

    def test_mineral_detail_view(self):
        """the detail view should be displayed for a mineral, when it
        is called with its slug
        """
        mineral = self.mineral
        resp = self.client.get(reverse(
            'minerals:detail',
            kwargs={'mineral_slug': mineral.mineral_slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, mineral.name)

    def test_mineral_detail_view_404(self):
        """the detail view returns a 404 error no mineral was not found"""
        resp = self.client.get(reverse(
            'minerals:detail',
            kwargs={'mineral_slug': 'nothing'}))
        self.assertEqual(resp.status_code, 404)


class MineralLetterListViewTests(TestCase):
    """Tests the Views"""
    def setUp(self):
        """The minerals found are assumed to be correct for the views test
        The retrieval of the minerals is done in models.py and tested
        with the models test.
        """
        self.search_letter = "b"
        self.default_letter = "a"
        self.no_result_letter = "y"
        self.minerals_for_letter_a \
            = Mineral.minerals.get_minerals_for_letter("a")
        self.minerals_for_letter_b \
            = Mineral.minerals.get_minerals_for_letter("b")
        self.minerals_for_letter_y \
            = Mineral.minerals.get_minerals_for_letter("y")

    def test_minerals_letter_listview_with_letter(self):
        test_url = reverse('minerals:filter_by_letter',
                           kwargs={'search_letter': self.search_letter})
        resp = self.client.get(test_url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'minerals/mineral_list.html')
        self.assertEqual(self.search_letter, resp.context['search_letter'])
        self.assertEqual(
            len(resp.context['minerals']),
            self.minerals_for_letter_b.count()
        )

    def test_minerals_letter_listview_default(self):
        test_url = reverse('minerals:filter_by_letter')
        resp = self.client.get(test_url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'minerals/mineral_list.html')
        self.assertEqual(self.default_letter, resp.context['search_letter'])
        self.assertEqual(
            len(resp.context['minerals']),
            self.minerals_for_letter_a.count()
        )

    def test_minerals_letter_listview_no_result(self):
        test_url = reverse('minerals:filter_by_letter',
                           kwargs={'search_letter': self.no_result_letter})
        resp = self.client.get(test_url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'minerals/mineral_list.html')
        self.assertEqual(self.no_result_letter, resp.context['search_letter'])
        self.assertEqual(
            len(resp.context['minerals']),
            self.minerals_for_letter_y.count()
        )


class MineralGroupListViewTests(TestCase):
    """Tests the Views"""
    def setUp(self):
        """The minerals found are assumed to be correct for the views test
        The retrieval of the minerals is done in models.py and tested
        with the models test.
        """
        self.group = Mineral.minerals.first().group
        self.minerals_for_group = Mineral.minerals.get_minerals_by_group(self.group)

    def test_minerals_group_listview_group(self):
        test_url = reverse('minerals:filter_by_group',
                           kwargs={'group_slug': slugify(self.group)})
        resp = self.client.get(test_url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'minerals/mineral_list.html')
        self.assertEqual(self.group, resp.context['search_group'])
        self.assertEqual(
            len(resp.context['minerals']),
            self.minerals_for_group.count()
        )


class MineralSearchHelpersTests(TestCase):
    def test_get_search_params_from_request(self):
        self.assertEqual(
            get_search_params_from_request(
                {
                    'chemical_element': "",
                    'searchterm': "",
                    'gravity_from': 3,
                    'gravity_to': 5,
                }
            ),
            SearchParams(None, None, (3,5))
        )


def test_get_search_params_from_request_gravity_both(self):
    self.assertEqual(
        get_search_params_from_request(
            {
                'chemical_element': "",
                'searchterm': "",
                'gravity_from': 3,
                'gravity_to': 5,
            }
        ),
        SearchParams(None, None, (3, 5))
    )
    def test_get_search_params_from_request_gravity_lower(self):
        self.assertEqual(
            get_search_params_from_request(
                {
                    'chemical_element': "",
                    'searchterm': "",
                    'gravity_from': 3,
                    'gravity_to': "",
                }
            ),
            SearchParams(None, None, (3,Mineral.MAX_SPECIFIC_GRAVITY))
        )
    def test_get_search_params_from_request_gravity_upper(self):
        self.assertEqual(
            get_search_params_from_request(
                {
                    'chemical_element': "",
                    'searchterm': "",
                    'gravity_from': "",
                    'gravity_to': 5,
                }
            ),
            SearchParams(None, None, (Mineral.MIN_SPECIFIC_GRAVITY,5))
        )

    def test_get_search_params_from_request_chemical_element(self):
        self.assertEqual(
            get_search_params_from_request(
                {
                    'chemical_element': "Fe",
                    'searchterm': "",
                    'gravity_from': "",
                    'gravity_to': "",
                }
            ),
            SearchParams("Fe", None, None)
        )

    def test_get_search_params_from_request_searchterm(self):
        self.assertEqual(
            get_search_params_from_request(
                {
                    'chemical_element': "",
                    'searchterm': "Ab",
                    'gravity_from': "",
                    'gravity_to': "",
                }
            ),
            SearchParams(None, "Ab", None)
        )

    def test_get_search_params_from_request_combination(self):
        self.assertEqual(
            get_search_params_from_request(
                {
                    'chemical_element': "Fe",
                    'searchterm': "Ab",
                    'gravity_from': 3,
                    'gravity_to': 5,
                }
            ),
            SearchParams("Fe", "Ab", (3,5))
        )


class MineralsSearchByFormViewTests(TestCase):
    """Tests Search by Form"""
    def setUp(self):
        """The minerals found are assumed to be correct for the views test
        The retrieval of the minerals is done in models.py and tested
        with the models test.
        """
        self.chemical_element = ChemicalElement.objects.first()

    def test_minerals_search_view_chem_element(self):
        context = {
            'chemical_element': self.chemical_element.code,
            'searchterm': "",
            'gravity_from': "",
            'gravity_to': "",
        }
        expected_minerals =\
            Mineral.minerals.filter_minerals_by_chem_element(
                self.chemical_element.code
            )
        test_url = reverse('minerals:filter_by_form')
        resp = self.client.get(test_url, context)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'minerals/mineral_list.html')
        self.assertEqual(
            len(resp.context['minerals']),
            expected_minerals.count()
        )

    def test_minerals_search_view_term(self):
        context = {
            'chemical_element': "",
            'searchterm': "Ab",
            'gravity_from': "",
            'gravity_to': "",
        }
        expected_minerals =\
            Mineral.minerals.filter_minerals_by_searchterm(
                "Ab"
            )
        test_url = reverse('minerals:filter_by_form')
        resp = self.client.get(test_url, context)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'minerals/mineral_list.html')
        self.assertEqual(
            len(resp.context['minerals']),
            expected_minerals.count()
        )

    def test_minerals_search_view_gravitybounds_both(self):
        context = {
            'chemical_element': "",
            'searchterm': "",
            'gravity_from': 3,
            'gravity_to': 5,
        }
        expected_minerals =\
            Mineral.minerals.filter_minerals_by_specific_gravity(
                (3, 5)
            )
        test_url = reverse('minerals:filter_by_form')
        resp = self.client.get(test_url, context)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'minerals/mineral_list.html')
        self.assertEqual(
            len(resp.context['minerals']),
            expected_minerals.count()
        )

    def test_minerals_search_view_gravitybounds_lower(self):
        context = {
            'chemical_element': "",
            'searchterm': "",
            'gravity_from': 3,
            'gravity_to': "",
        }
        expected_minerals = \
            Mineral.minerals.filter_minerals_by_specific_gravity(
                (3,Mineral.MAX_SPECIFIC_GRAVITY)
            )
        test_url = reverse('minerals:filter_by_form')
        resp = self.client.get(test_url, context)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'minerals/mineral_list.html')
        self.assertEqual(
            len(resp.context['minerals']),
            expected_minerals.count()
        )

    def test_minerals_search_view_gravitybounds_upper(self):
        context = {
            'chemical_element': "",
            'searchterm': "",
            'gravity_from': "",
            'gravity_to': 5,
        }
        expected_minerals = \
            Mineral.minerals.filter_minerals_by_specific_gravity(
                (Mineral.MIN_SPECIFIC_GRAVITY,5)
            )
        test_url = reverse('minerals:filter_by_form')
        resp = self.client.get(test_url, context)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'minerals/mineral_list.html')
        self.assertEqual(
            len(resp.context['minerals']),
            expected_minerals.count()
        )


    def test_minerals_search_view_combination(self):
        context = {
            'chemical_element': "Fe",
            'searchterm': "Ab",
            'gravity_from': "7",
            'gravity_to': 12,
        }
        expected_minerals = \
            Mineral.minerals.get_minerals_from_search_params(
                get_search_params_from_request(context)
            )
        test_url = reverse('minerals:filter_by_form')
        resp = self.client.get(test_url, context)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'minerals/mineral_list.html')
        self.assertEqual(
            len(resp.context['minerals']),
            expected_minerals.count()
        )
