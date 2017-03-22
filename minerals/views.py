"""
views for the minerals app
"""
from collections import namedtuple
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from . import models


SearchParams = namedtuple(
    'Search', ['searchterm', 'chem_element_code', 'gravity_bounds'])
SearchParams.__new__.__defaults__ = (None, None, None)


def minerals_letter_listview(request, search_letter):
    """filters minerals by letter
    - when no letter is provided a default letter is used
    - minerals are returned when their slugified first letter
    is equal to the given letter (slugification is necessary
    for special characters)
    """
    search_letter = models.Mineral.get_search_letter(search_letter)
    minerals = models.Mineral.minerals.get_minerals_for_letter(search_letter)
    return render(
        request,
        'minerals/mineral_list.html',
        {'minerals': minerals,
         'search_letter': search_letter})


def minerals_group_listview(request, group_slug):
    """This filters the minerals by group
    - every mineral has the group attribut
    - the group comes in as a slug and the group has to be derived
    from the slug
    """
    group = models.Mineral.get_group_from_slug(group_slug)
    minerals = models.Mineral.minerals.get_minerals_by_group(group)
    return render(
        request,
        'minerals/mineral_list.html',
        {'minerals': minerals,
         'search_group': group})


def mineral_detail_view(request, mineral_slug):
    """
    renders a mineral that is picked by its slug.
    """
    mineral = models.Mineral.minerals.get_mineral_from_slug(mineral_slug)
    return render(
        request,
        'minerals/mineral_detail.html',
        {'mineral': mineral})


def get_search_params_from_request(request_get):
    """get the searchparamters from the request"""
    searchterm, chem_element_code, gravity_bounds \
        = None, None, None
    if request_get['searchterm'] != "":
        searchterm = request_get['searchterm']
    if request_get['chemical_element'] != "":
        chem_element_code = request_get['chemical_element']
    if (request_get['gravity_from'] != ""
        or request_get['gravity_to'] != ""):
        gravity_from = int(request_get['gravity_from']) \
            if request_get['gravity_from'] != "" \
            else models.Mineral.MIN_SPECIFIC_GRAVITY
        gravity_to = int(request_get['gravity_to']) \
            if request_get['gravity_to'] != "" \
            else models.Mineral.MAX_SPECIFIC_GRAVITY
        gravity_bounds = (gravity_from, gravity_to)
    return SearchParams(
        searchterm=searchterm,
        chem_element_code=chem_element_code,
        gravity_bounds=gravity_bounds,
        )


def minerals_search_listview(request):
    """
    This view is called via a search form. The minerals are searched
    guided by the search parameters that are contained in the request
    """
    search_params = get_search_params_from_request(request.GET)
    minerals = models.Mineral.minerals.get_minerals_from_search_params(search_params)
    return render(
        request,
        'minerals/mineral_list.html',
        {'minerals': minerals,
         'search_params': search_params})


