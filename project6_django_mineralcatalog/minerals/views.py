"""
views for the minerals app
"""
from django.shortcuts import get_list_or_404, render

from .models import Mineral


def mineral_list(request):
    """renders a list of all minerals"""
    minerals = Mineral.objects.all()
    return render(
        request,
        'minerals/mineral_list.html',
        {'minerals': minerals})


def mineral_detail(request, name):
    """
    renders a mineral that is picked by its short name. There may be
    more then on mineral in the database, that start with that short name
    but the short name itself is unique
    """
    search_name = name.capitalize()
    minerals = get_list_or_404(Mineral, name__startswith=search_name)
    mineral = [mineral
               for mineral in minerals
               if mineral.short_name == search_name].pop()
    return render(
        request,
        'minerals/mineral_detail.html',
        {'mineral': mineral})
