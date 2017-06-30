"""urls for the accounts app"""
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'login/$', views.LoginView.as_view(), name="login"),
    url(r'^logout/$', views.LogoutView.as_view(), name="logout"),
    url(r'^register/$', views.RegisterView.as_view(), name="register"),

    url(r'^profile$',
        views.ProfileView.as_view(),
        name='profile'),

    url(r'^profile/(?P<profile_pk>\d+)$',
        views.ProfileView.as_view(),
        name='profile_other'),

    url(r'^profile/edit$',
        views.profile_edit_view,
        name='profile_edit'),

    url(r'^profile/(?P<profile_pk>\d+)/applications$',
        views.ApplicationsListView.as_view(),
        name="applications"),
]
