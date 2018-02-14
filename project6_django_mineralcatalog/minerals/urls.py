"""
urls for the minerals app
Each mineral has a pretty url, which is
derived from the name of the mineral: the url_name
"""
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.mineral_list, name='list'),
    url(r'(?P<name>\w+)/$', views.mineral_detail, name='detail'),
]
