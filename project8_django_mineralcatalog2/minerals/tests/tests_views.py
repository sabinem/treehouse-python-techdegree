"""
Tests for the minerals app's detail view
---------------------------------------------------------
- The Database is filled with data by the datamigrations,
Therefore testdata is already available and must not be
created.
- The querysets selecting the minerals are part of models.py
and are tested in test_model.py
"""
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.text import slugify

from minerals.models import Mineral, ChemicalElement
from minerals.views import SearchParams, get_search_params_from_request


class MineralDetailViewTests(TestCase):
    """Tests the Mineral DetailView"""
    def setUp(self):
        """set up an example mineral"""
        self.mineral = Mineral.minerals.first()

    def test_mineral_detail_view(self):
        """the detail view should be displayed for a mineral, when it
        is called by its slug"""
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
    """Tests the Mineral List Views"""
    def test_minerals_letter_listview_with_letter(self):
        """minerals for a letter are displayed. the """
        test_url = reverse('minerals:filter_by_letter',
                           kwargs={'search_letter': "b"})
        expected_minerals\
            = Mineral.minerals.get_minerals_for_letter("b")
        resp = self.client.get(test_url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'minerals/mineral_list.html')
        self.assertEqual("b", resp.context['search_letter'])
        self.assertEqual(
            len(resp.context['minerals']),
            expected_minerals.count()
        )

    def test_minerals_letter_listview_default(self):
        """minerals for a default letter are displayed, if no
        letter was provided"""
        test_url = reverse('minerals:filter_by_letter')
        expected_minerals\
            = Mineral.minerals.get_minerals_for_letter("a")
        resp = self.client.get(test_url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'minerals/mineral_list.html')
        self.assertEqual("a", resp.context['search_letter'])
        self.assertEqual(
            len(resp.context['minerals']),
            expected_minerals.count()
        )

    def test_minerals_letter_listview_no_result(self):
        """a message that no result was found is displayed
        if there are no minerals for a letter"""
        test_url = reverse('minerals:filter_by_letter',
                           kwargs={'search_letter': "y"})
        expected_minerals\
            = Mineral.minerals.get_minerals_for_letter("y")
        resp = self.client.get(test_url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'minerals/mineral_list.html')
        self.assertEqual("y", resp.context['search_letter'])
        self.assertEqual(
            len(resp.context['minerals']),
            expected_minerals.count()
        )
        self.assertContains(resp, "no minerals were found")

    def test_minerals_group_listview_group(self):
        """minerals for a group are displayed"""
        group = Mineral.minerals.first().group
        expected_minerals = \
            Mineral.minerals.get_minerals_by_group(group)
        test_url = reverse('minerals:filter_by_group',
                           kwargs={'group_slug': slugify(group)})
        resp = self.client.get(test_url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'minerals/mineral_list.html')
        self.assertEqual(group, resp.context['search_group'])
        self.assertEqual(
            len(resp.context['minerals']),
            expected_minerals.count()
        )


class MineralSearchHelpersTests(TestCase):
    """test the transformation of the request context into
    search parameters: blanks are transformed to None,
    the range is completed if values are missing"""
    def test_get_search_params_from_request_gravity_both(self):
        """search for a specific gravity range with a complete
        range: the range is passed on"""
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
        """search for a specific gravity range with a lower
        bound only: the range is completed with the max upper
        bound"""
        self.assertEqual(
            get_search_params_from_request(
                {
                    'chemical_element': "",
                    'searchterm': "",
                    'gravity_from': 3,
                    'gravity_to': "",
                }
            ),
            SearchParams(None, None, (3, Mineral.MAX_SPECIFIC_GRAVITY))
        )

    def test_get_search_params_from_request_gravity_upper(self):
        """search for a specific gravity range with a upper
        bound only: the range is completed with the min lower
        bound"""
        self.assertEqual(
            get_search_params_from_request(
                {
                    'chemical_element': "",
                    'searchterm': "",
                    'gravity_from': "",
                    'gravity_to': 5,
                }
            ),
            SearchParams(None, None, (Mineral.MIN_SPECIFIC_GRAVITY, 5))
        )

    def test_get_search_params_from_request_chemical_element(self):
        """search for a chemical element only:
        the element is passed on"""
        self.assertEqual(
            get_search_params_from_request(
                {
                    'chemical_element': "Fe",
                    'searchterm': "",
                    'gravity_from': "",
                    'gravity_to': "",
                }
            ),
            SearchParams(None, "Fe", None)
        )

    def test_get_search_params_from_request_searchterm(self):
        """search for a search term only:
        the term is passed on"""
        self.assertEqual(
            get_search_params_from_request(
                {
                    'chemical_element': "",
                    'searchterm': "Ab",
                    'gravity_from': "",
                    'gravity_to': "",
                }
            ),
            SearchParams("Ab", None, None)
        )

    def test_get_search_params_from_request_combination(self):
        """search for a combination:
        the combination is passed on"""
        self.assertEqual(
            get_search_params_from_request(
                {
                    'chemical_element': "Fe",
                    'searchterm': "Ab",
                    'gravity_from': 3,
                    'gravity_to': 5,
                }
            ),
            SearchParams("Ab", "Fe", (3, 5))
        )


class MineralsSearchByFormViewTests(TestCase):
    """Tests the Search by Form Views"""
    def test_minerals_search_view_chem_element(self):
        """search with a chemical element only displays
        the expected minerals"""
        self.chemical_element = ChemicalElement.objects.first()
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
        """search with a search term only displays
        the expected minerals"""
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
        """search with gravity bounds only displays
        the expected minerals"""
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
        """search with only a lower garvity bound displays
        the expected minerals"""
        context = {
            'chemical_element': "",
            'searchterm': "",
            'gravity_from': 3,
            'gravity_to': "",
        }
        expected_minerals = \
            Mineral.minerals.filter_minerals_by_specific_gravity(
                (3, Mineral.MAX_SPECIFIC_GRAVITY)
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
        """search with only an upper garvity bound displays
        the expected minerals"""
        context = {
            'chemical_element': "",
            'searchterm': "",
            'gravity_from': "",
            'gravity_to': 5,
        }
        expected_minerals = \
            Mineral.minerals.filter_minerals_by_specific_gravity(
                (Mineral.MIN_SPECIFIC_GRAVITY, 5)
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
        """search with combination displays the
        the expected minerals"""
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
