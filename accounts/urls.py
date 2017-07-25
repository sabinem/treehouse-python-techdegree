"""urls for the accounts app"""
from django.conf.urls import url

from . import views


urlpatterns = [
    # handeling login, logout and registration
    url(r'login/$', views.LoginView.as_view(), name="login"),
    url(r'^logout/$', views.LogoutView.as_view(), name="logout"),
    url(r'^register/$', views.RegisterView.as_view(), name="register"),

    # profile view of own profile
    url(r'^profile$',
        views.ProfileView.as_view(),
        name='profile'),

    # profile view of other profiles
    url(r'^profile/(?P<profile_pk>\d+)$',
        views.ProfileView.as_view(),
        name='profile_other'),

    # edit own profile
    url(r'^profile/edit$',
        views.profile_edit_view,
        name='profile_edit'),

    # work with applications to own projects
    url(r'^profile/(?P<profile_pk>\d+)/applications$',
        views.ApplicationsListView.as_view(),
        name="applications"),

    # search applications
    url(r'^search/$', views.search_applications, name='search_by_term'),

    # reject application
    url(r'^reject-application/(?P<application_pk>\d+)$',
        views.reject_application,
        name='reject_application'),

    # approve application
    url(r'^approve-application/(?P<application_pk>\d+)$',
        views.approve_application,
        name='approve_application'),
]
