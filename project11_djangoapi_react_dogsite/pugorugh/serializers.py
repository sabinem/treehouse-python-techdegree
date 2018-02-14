"""
serializers for the pugorugh app
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers

from . import models


class DogSerializer(serializers.ModelSerializer):
    """serializing the Dog model"""
    class Meta:
        fields = ('id', 'name', 'image_filename',
                  'breed', 'age', 'gender', 'size')
        model = models.Dog


class UserDogSerializer(serializers.ModelSerializer):
    """serializing the UserDog model"""
    class Meta:
        fields = ('id', 'user', 'dog', 'status',)
        model = models.UserDog


class UserPrefSerializer(serializers.ModelSerializer):
    """serializing the UserPref model
    - uses Multpile Choice Field to get choices into a list
    """
    age = serializers.MultipleChoiceField(
        choices=models.get_choices(models.Age))
    gender = serializers.MultipleChoiceField(
        choices=models.get_choices(models.Gender))
    size = serializers.MultipleChoiceField(
        choices=models.get_choices(models.Size))

    class Meta:
        fields = ('id', 'user', 'age', 'gender', 'size',)
        model = models.UserPref


class UserSerializer(serializers.ModelSerializer):
    """serializing the User model"""
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = get_user_model()
