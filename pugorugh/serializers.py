from rest_framework import serializers

from . import models


class DogSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'image_filename',
                  'breed', 'age', 'gender', 'size')
        model = models.Dog


class UserDogSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'user', 'dog', 'status',)
        model = models.UserDog


class UserPrefSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'user', 'age', 'gender', 'size',)
        model = models.UserPref
