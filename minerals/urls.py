"""
urls for the minerals app
Each mineral has a pretty url, which is
derived from the name of the mineral: the url_name
"""
from django.conf.urls import include, url
from django.conf import settings

from . import views


urlpatterns = [
    url(r'^searchresults$',
        views.minerals_search_listview,
        name='filter_by_form'),
    url(r'^(?P<search_letter>\w{1})?$',
        views.minerals_letter_listview,
        name='filter_by_letter'),
    url(r'group/(?P<group_slug>[a-z-]+)$',
        views.minerals_group_listview,
        name='filter_by_group'),
    url(r'^mineral/(?P<mineral_slug>[a-z-]+)$',
        views.mineral_detail_view,
        name='detail'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls))
    ]

