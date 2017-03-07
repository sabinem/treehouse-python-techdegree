"""
profile urls
- view own profile
- view own profile as others see it or view profile of others
- list profiles
- edit profile
- create profile
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.own_profile, name='own'),
    url(r'^(?P<pk>\d+)$', views.other_profile, name='other'),
    url(r'^list$', views.list_profiles, name='list'),
    url(r'^edit$', views.edit_profile, name='edit'),
    url(r'^create$', views.create_profile, name='create'),
    url(r'^transform_avatar$', views.transform_avatar, name='transform_avatar'),
]