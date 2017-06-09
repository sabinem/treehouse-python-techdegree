"""
views for the pugorugh app
- there are for the token based frondend api
- a browsable backend api
- automatic creation of UserPref and Token
when a user registers
"""
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token

from rest_framework import permissions
from django.contrib.auth import get_user_model

from . import serializers, models


@api_view(['PUT'])
def userdog_update_status_liked_view(request, dog_pk):
    """updating dog status to liked for request user,
    api-url used by the frontend"""
    dog = get_object_or_404(models.Dog, pk=dog_pk)
    dog.update_userdog_status(request.user, models.LIKED)
    serializer = serializers.DogSerializer(dog)
    return Response(serializer.data)


@api_view(['PUT'])
def userdog_update_status_disliked_view(request, dog_pk):
    """updating dog status to disliked for request user,
    api-url used by the frontend"""
    dog = get_object_or_404(models.Dog, pk=dog_pk)
    dog.update_userdog_status(request.user, models.DISLIKED)
    serializer = serializers.DogSerializer(dog)
    return Response(serializer.data)


@api_view(['PUT'])
def userdog_update_status_undecided_view(request, dog_pk):
    """updating dog status to undecided for request user,
    api-url used by the frontend"""
    dog = get_object_or_404(models.Dog, pk=dog_pk)
    dog.update_userdog_status(request.user, models.UNDECIDED)
    serializer = serializers.DogSerializer(dog)
    return Response(serializer.data)


@api_view(['GET'])
def userdog_retrieve_next_liked_view(request, dog_pk):
    """retriving next liked dog for request user,
    api-url used by the frontend"""
    next_dog = models.Dog.objects.get_next_dog_by_status(
        user=request.user,
        pk=dog_pk,
        status=models.LIKED
    )
    if not next_dog:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = serializers.DogSerializer(next_dog)
    return Response(serializer.data)


@api_view(['GET'])
def userdog_retrieve_next_disliked_view(request, dog_pk):
    """retriving next disliked dog for request user,
    api-url used by the frontend"""
    next_dog = models.Dog.objects.get_next_dog_by_status(
        user=request.user,
        pk=dog_pk,
        status=models.DISLIKED
    )
    if not next_dog:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = serializers.DogSerializer(next_dog)
    return Response(serializer.data)


@api_view(['GET'])
def userdog_retrieve_next_undecided_view(request, dog_pk):
    """retriving next undecided dog for request user,
    api-url used by the frontend"""
    next_dog = models.Dog.objects.get_next_dog_undecided(
        user=request.user,
        pk=dog_pk,
    )
    if not next_dog:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = serializers.DogSerializer(next_dog)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
def user_preferences_retrieve_update_view(request):
    """retriving and updating UserPref Table,
    api-url used by the frontend"
    """
    user = request.user
    user_pref = models.UserPref.objects.get(user=user)
    if request.method == 'PUT':
        data = request.data
        user_pref.age = data.get('age')
        user_pref.gender = data.get('gender')
        user_pref.size = data.get('size')
        user_pref.save()
    serializer = serializers.UserPrefSerializer(user_pref)
    return Response(serializer.data)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_userpref(sender, **kwargs):
    """a UserPref instance is created
    automatically for any new user"""
    user = kwargs['instance']
    if kwargs['created']:
        user_pref = models.UserPref(user=user)
        user_pref.save()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """a token is created automatically for any new user"""
    if created:
        Token.objects.create(user=instance)


class UserRegisterView(CreateAPIView):
    """User Registration,
    api-url used by the frontend"""
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class DogViewSet(viewsets.ModelViewSet):
    """view set to administer Dog data,
    to use for admin user in browseable api only"""
    permission_classes = (permissions.IsAdminUser,)
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer
    authentication_classes = (SessionAuthentication,)


class UserPrefViewSet(viewsets.ModelViewSet):
    """view set to administer UserPref data,
     to use for admin user in browseable api only"""
    permission_classes = (permissions.IsAdminUser,)
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer
    authentication_classes = (SessionAuthentication,)


class UserViewSet(viewsets.ModelViewSet):
    """view set to administer User data,
     to use for admin user in browseable api only"""
    permission_classes = (permissions.IsAdminUser,)
    queryset = models.User.objects.all()
    serializer_class = serializers.UserPrefSerializer
    authentication_classes = (SessionAuthentication,)
