"""
mineral_catalog URL Configuration
"""

from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    url(r'^minerals/', include('minerals.urls', namespace='minerals')),
]

urlpatterns += staticfiles_urlpatterns()
