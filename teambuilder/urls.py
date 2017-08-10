"""urls for the teambuilder app"""
from django.conf.urls import url

from . import views


urlpatterns = [
    # projects accessible for anonymous users
    url(r'^$', views.ProjectListView.as_view(), name="projects"),
    url(r'^search/(?P<term>\w+)$', views.ProjectListView.as_view(), name="projects"),
    url(r'^need/(?P<need_pk>\d+)$', views.ProjectListView.as_view(), name="projects_by_need"),

    # project detail
    url(r'^project/(?P<project_pk>\d+)$', views.ProjectDetailView.as_view(), name="project"),

    # project CRUD view for authenticated users only
    url(r'^project/(?P<project_pk>\d+)/edit$', views.project_edit_view, name="project_edit"),
    url(r'^project/(?P<project_pk>\d+)/delete$', views.project_delete, name="project_delete"),
    url(r'^project/new$', views.project_create_view, name="project_new"),

    # action views
    url(r'^(?P<position_pk>\d+)/apply$', views.position_apply, name="apply"),

]

