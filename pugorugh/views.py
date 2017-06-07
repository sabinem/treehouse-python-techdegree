from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from . import serializers, models


class DogViewSet(viewsets.ModelViewSet):
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer


class UserDogViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet):
    queryset = models.UserDog.objects.all()
    serializer_class = serializers.UserDogSerializer


@api_view(['PUT'])
def userdog_update_status_liked_view(request, dog_pk):
    dog = get_object_or_404(models.Dog, pk=dog_pk)
    dog.update_userdog_status(request.user, models.Status.liked.value)
    serializer = serializers.DogSerializer(dog)
    return Response(serializer.data)


@api_view(['PUT'])
def userdog_update_status_disliked_view(request, dog_pk):
    dog = get_object_or_404(models.Dog, pk=dog_pk)
    dog.update_userdog_status(request.user, models.Status.disliked.value)
    serializer = serializers.DogSerializer(dog)
    return Response(serializer.data)


@api_view(['PUT'])
def userdog_update_status_undecided_view(request, dog_pk):
    dog = get_object_or_404(models.Dog, pk=dog_pk)
    dog.set_userdog_undecided(request.user)
    serializer = serializers.DogSerializer(dog)
    return Response(serializer.data)


@api_view(['GET'])
def userdog_retrieve_next_liked_view(request, dog_pk):
    next_dog = models.Dog.objects.get_next_dog_by_status(
        user=request.user,
        pk=dog_pk,
        status=models.Status.liked.value
    )
    if not next_dog:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = serializers.DogSerializer(next_dog)
    return Response(serializer.data)


@api_view(['GET'])
def userdog_retrieve_next_disliked_view(request, dog_pk):
    next_dog = models.Dog.objects.get_next_dog_by_status(
        user=request.user,
        pk=dog_pk,
        status=models.Status.disliked.value
    )
    if not next_dog:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = serializers.DogSerializer(next_dog)
    return Response(serializer.data)


@api_view(['GET'])
def userdog_retrieve_next_undecided_view(request, dog_pk):
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
    user = kwargs['instance']
    if kwargs['created']:
        user_pref = models.UserPref(user=user)
        user_pref.save()