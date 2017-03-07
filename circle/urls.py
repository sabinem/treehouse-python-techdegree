"""
circle URL Configuration
- admins are redirected to the home page on logout
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^', include('accounts.urls', namespace='accounts')),
    url(r'^admin/logout/$', views.home),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^profile/', include('profiles.urls', namespace='profiles')),
    url(r'^$', views.home, name='home'),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
