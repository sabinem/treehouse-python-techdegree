"""template tags for the profile app"""
from django import template


register = template.Library()


@register.inclusion_tag('profiles/form_js.html')
def form_js():
    '''get js for forms'''
    return {}


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