"""template tags and filters for the minerals app"""
from django import template

from minerals.models import Mineral
import random


register = template.Library()


@register.inclusion_tag('minerals/random_link.html')
def random_mineral():
    '''Gets random mineral. The mineral is fetched by its url_name'''
    mineral_ids = Mineral.objects.values_list('id', flat=True)
    random_pk = random.choice(mineral_ids)
    random_name = Mineral.objects.get(pk=random_pk).url_name
    return {'random_name': random_name}


@register.inclusion_tag('minerals/mineral_fields.html')
def mineral_fields(mineral):
    '''Returns fields of the mineral in order of occurence'''
    weigthed_attributes_list = Mineral.attributes_weighted()
    weigthed_field_list = []
    for fieldname in weigthed_attributes_list:
        data = getattr(mineral, fieldname)
        label = mineral._meta.get_field(fieldname).verbose_name
        if data != '':
            weigthed_field_list.append({'label': label, 'data': data})
    return {'mineral_field_list': weigthed_field_list}


@register.filter('capitalize')
def capitalize(name):
    """Filter that capitalizes attribute names: all words are capitalized"""
    return ' '.join([part.capitalize() for part in name.split(' ')])
