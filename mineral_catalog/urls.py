"""
mineral_catalog URL Configuration
"""

from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings


urlpatterns = [
    url(r'^', include('minerals.urls', namespace='minerals')),
]

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

