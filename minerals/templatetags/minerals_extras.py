from django import template
from django.forms import model_to_dict
import os
import re

from minerals.models import Mineral
import random

register = template.Library() 

@register.inclusion_tag('minerals/random_link.html')
def random_mineral():
    '''Gets random mineral'''
    mineral_ids =  Mineral.objects.values_list('id', flat=True)
    random_pk = random.choice(mineral_ids)
    return {'random_pk': random_pk}


@register.inclusion_tag('minerals/mineral_fields.html')
def mineral_fields(mineral):
    '''Returns fields of the mineral in order of occurence'''
    field_dict = model_to_dict(mineral)
    weigthed_attributes_list = Mineral.attributes_weighted()
    weigthed_field_list = []
    for fieldname in weigthed_attributes_list:
        data = getattr(mineral, fieldname)
        label = mineral._meta.get_field(fieldname).verbose_name
        if data != '':
            weigthed_field_list.append({'label':label, 'data':data})
    return {'mineral_field_list': weigthed_field_list}


@register.filter('truncate_name')
def truncate_mineral_name(name):
    return re.match('^[\w]+', name).group(0)


@register.filter('capitalize')
def capitalize(name):
    return ' '.join([part.capitalize() for part in name.split(' ')])

