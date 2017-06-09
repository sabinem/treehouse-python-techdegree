"""urls for the pugorugh app"""
from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns

from . import views


# API endpoints
urlpatterns = format_suffix_patterns([

    # favicon
    url(r'^favicon\.ico$',
        RedirectView.as_view(
            url='/static/icons/favicon.ico',
            permanent=True
        )),

    # application
    url(r'^$', TemplateView.as_view(template_name='index.html')),

    # -------- Api ------------------------

    # change userdog status
    url(r'^api/dog/(?P<dog_pk>\d+)/liked/$',
        views.userdog_update_status_liked_view,
        name='userdog_update_like'),
    url(r'^api/dog/(?P<dog_pk>\d+)/disliked/$',
        views.userdog_update_status_disliked_view,
        name='userdog_update_dislike'),
    url(r'^api/dog/(?P<dog_pk>\d+)/undecided/$',
        views.userdog_update_status_undecided_view,
        name='userdog_update_undecided'),

    # get next dog with same status from pk
    url(r'^api/dog/(?P<dog_pk>-?\d+)/liked/next/$',
        views.userdog_retrieve_next_liked_view,
        name='userdog_retrieve_next_liked'),
    url(r'^api/dog/(?P<dog_pk>-?\d+)/disliked/next/$',
        views.userdog_retrieve_next_disliked_view,
        name='userdog_retrieve_next_disliked'),
    url(r'^api/dog/(?P<dog_pk>-?\d+)/undecided/next/$',
        views.userdog_retrieve_next_undecided_view,
        name='userdog_retrieve_next_undecided'),

])
