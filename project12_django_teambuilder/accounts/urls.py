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

    # a user can list applications to his projects
    url(r'^profile/applications$',
        views.ApplicationsListView.as_view(),
        name="applications"),

    # he filter applications by status
    url(r'^profile/applications/status/(?P<status>\w{1})$',
        views.ApplicationsListView.as_view(),
        name="applications_status"),

    # he can filter applications by need
    url(r'^profile/applications/need/(?P<need_pk>\d+)$',
        views.ApplicationsListView.as_view(),
        name="applications_need"),

    # he can filter applications by project
    url(r'^profile/applications/project/(?P<project_pk>\d+)$',
        views.ApplicationsListView.as_view(),
        name="applications_project"),

    # he can reject an application
    url(r'^reject-application/(?P<application_pk>\d+)$',
        views.reject_application,
        name='reject_application'),

    # he can approve application
    url(r'^approve-application/(?P<application_pk>\d+)$',
        views.approve_application,
        name='approve_application'),
]
