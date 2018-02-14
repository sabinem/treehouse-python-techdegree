"""
URL Configuration
"""
from django.conf.urls import url, include

from rest_framework.authtoken import views as authtoken_views

from rest_framework import routers

from pugorugh import views as pugorugh_views

router = routers.DefaultRouter()
router.register(r'dogs', pugorugh_views.DogViewSet)
router.register(r'userprefs', pugorugh_views.UserPrefViewSet)
router.register(r'userprefs', pugorugh_views.UserViewSet)


urlpatterns = [
    # login by by restframework
    url(r'^api/user/login/', authtoken_views.obtain_auth_token),

    # pugorugh application
    url(r'^', include('pugorugh.urls')),

    # set preferences
    url(r'^api/user/preferences/$',
        pugorugh_views.user_preferences_retrieve_update_view,
        name='user_preferences_retrieve_update'),

    # registration by pugorugh auth
    url(r'^api/user/',
        pugorugh_views.UserRegisterView.as_view(),
        name='register-user'),

    # used for authorization by restframework
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),

    # admin users can use this url to get to browsable api
    url(r'^api/admin/', include(router.urls, namespace='api-admin')),
]
