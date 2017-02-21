from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.own_profile, name='own'),
    url(r'^(?P<pk>\d+)$', views.other_profile, name='other'),
    url(r'^list$', views.list_profiles, name='list'),
    url(r'^edit$', views.edit_profile, name='edit'),
    url(r'^create$', views.create_profile, name='create'),
    url(r'^change_password$', views.change_password, name='change_password'),
    url(r'^edit_avatar$', views.edit_avatar, name='edit_avatar'),
    url(r'^img$', views.image, name='image'),
    url(r'^pil$', views.pil_image, name='pil_image'),
]