"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework.authtoken import views as authtoken_views

from rest_framework import routers

from pugorugh import views as pugorugh_views
from accounts import views as accounts_views

router = routers.DefaultRouter()
router.register(r'dog', pugorugh_views.DogViewSet)



urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # login by by restframework
    url(r'^api/user/login/', authtoken_views.obtain_auth_token),


    # pugorugh application
    url(r'^', include('pugorugh.urls')),

    # set preferences
    url(r'^api/user/preferences/$',
        pugorugh_views.user_preferences_retrieve_update_view,
        name='user_preferences_retrieve_update'),

    # registration by pugorugh auth
    url(r'^api/user/x', accounts_views.UserRegisterView.as_view(), name='register-user'),


    # authorization by restframework
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),

    # pugorugh api
    url(r'^api/', include('pugorugh.urls', namespace='api')),
]

