"""views of the menu app"""
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q

from . import models
from . import forms


def menu_list(request):
    """list all menus that have no expiration date or expire
    in the future"""
    today = timezone.now().date()
    menus = models.Menu.objects.filter(
        Q(expiration_date__gte=today) | Q(expiration_date=None),
    ).prefetch_related('items')
    return render(request, 'menu/menu_list_current.html', {'menus': menus})


def menu_detail(request, pk):
    """detail view of a menu"""
    menu = get_object_or_404(models.Menu, pk=pk)
    items = menu.items.all()
    return render(
        request, 'menu/menu_detail.html',
        {'menu': menu, 'items': items})


def item_detail(request, pk):
    """detail view of an item"""
    item = get_object_or_404(models.Item, pk=pk)
    ingredients = item.ingredients.all()
    return render(
        request, 'menu/item_detail.html',
        {'item': item, 'ingredients': ingredients})


def create_new_menu(request):
    """create a new menu"""
    form = forms.MenuForm()
    if request.method == "POST":
        form = forms.MenuForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu_detail', pk=form.instance.pk)
    return render(request, 'menu/menu_create.html', {'form': form})


def edit_menu(request, pk):
    """edit an existing menu"""
    menu = get_object_or_404(models.Menu, pk=pk)
    form = forms.MenuForm(instance=menu)
    if request.method == "POST":
        form = forms.MenuForm(instance=menu, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu_detail', pk=form.instance.pk)
    return render(request, 'menu/menu_edit.html', {'form': form})
