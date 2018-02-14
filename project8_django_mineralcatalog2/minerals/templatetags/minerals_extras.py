"""template tags and filters for the minerals app"""
import string

from django import template

from .. import forms, models


register = template.Library()


@register.inclusion_tag('minerals/random_link.html')
def random_mineral():
    '''renders random mineral'''
    random_mineral = models.Mineral.minerals.get_random_mineral()
    return {'random_mineral': random_mineral}


@register.inclusion_tag('minerals/mineral_fields.html')
def mineral_fields(mineral):
    '''renders attributes of the mineral in order of occurence'''
    weigthed_attributes_list = models.Mineral.attributes_weighted()
    weigthed_field_list = []
    for fieldname in weigthed_attributes_list:
        data = getattr(mineral, fieldname)
        label = mineral._meta.get_field(fieldname).verbose_name
        if data != '':
            weigthed_field_list.append({'label': label, 'data': data})
    return {'mineral_field_list': weigthed_field_list}


@register.filter('capitalize')
def capitalize(name):
    """Filter that capitalizes all words in a string"""
    return ' '.join([part.capitalize() for part in name.split(' ')])


@register.inclusion_tag('minerals/search_letter.html', takes_context=True)
def search_letter(context):
    '''renders the alphabet as search navigation for filtering
     the minerals by their first letter'''
    letters = string.ascii_lowercase
    if 'search_letter' in context:
        active_letter = context['search_letter']
    else:
        active_letter = None
    return {'letters': letters, 'active_letter': active_letter}


@register.inclusion_tag('minerals/search_group.html', takes_context=True)
def search_group(context):
    '''renders groups as search navigation for filtering
    mineral by their group'''
    groups = models.Mineral.minerals.get_ordered_groups()
    if 'search_group' in context:
        active_group = context['search_group']
    else:
        active_group = None
    return {'groups': [(g, models.Mineral.get_group_slug(g)) for g in groups],
            'active_group': active_group}


@register.inclusion_tag('minerals/search_form.html')
def search_form():
    '''renders a search form for different kind of
    searches: see forms.SearchForm'''
    form = forms.SearchForm
    return {'form': form}
