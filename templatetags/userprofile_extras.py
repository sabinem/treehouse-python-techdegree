"""template tags and filters for the minerals app"""
from django import template


register = template.Library()


@register.filter('active_class')
def capitalize(url, path):
    """Filter that capitalizes attribute names: all words are capitalized"""
    return url == path
