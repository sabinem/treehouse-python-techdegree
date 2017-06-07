from enum import Enum

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save

from rest_framework import pagination

from multiselectfield import MultiSelectField


class Unknown(Enum):
    unknown = 'u'


class Gender(Enum):
    male = 'm'
    female = 'f'


class Age(Enum):
    baby = 'b'
    young = 'y'
    adult = 'a'
    senior = 's'


class Size(Enum):
    small = 's'
    medium = 'm'
    large = 'l'
    xlarge = 'xl'
    unknown = 'u'


class Status(Enum):
    liked = 'l'
    disliked = 'd'


def get_choices_with_unknown(cls):
    choices = get_choices(cls)
    choices.append((Unknown.unknown.value, Unknown.unknown.name))
    return choices


def get_choices(cls):
    return [(x.value, x.name) for x in cls]



class DogManager(models.Manager):
    def get_next_dog_by_status(self, user, pk, status):
        ids_for_status = UserDog.objects.get_userdogs_dog_ids_status_by_user(user, status)
        ids_for_userpref = Dog.objects.get_dogs_for_user_preference(user)
        ids_result = [id for id in ids_for_status if id in ids_for_userpref]
        return self.filter(id__in=ids_result).filter(id__gt=pk).first()

    def get_next_dog_undecided(self, user, pk):
        ids_exclude_for_status = UserDog.objects.get_userdogs_dog_ids_decided_by_user(user)
        ids_for_userpref = Dog.objects.get_dogs_for_user_preference(user)
        return self.exclude(id__in=ids_exclude_for_status)\
                   .filter(id__in=ids_for_userpref)\
                   .filter(id__gt=pk).first()

    def get_dogs_for_user_preference(self, user):
        userpref = UserPref.objects.get(user=user)
        prefdogs_size_gender = self.filter(
            size__in=userpref.size,
            gender__in=userpref.gender
        )
        ids_for_userpref = [dog.id for dog in prefdogs_size_gender if dog.age_class in userpref.age]
        return ids_for_userpref


class Dog(models.Model):
    name = models.CharField('Name', max_length=255)
    image_filename = models.CharField(max_length=255)
    breed = models.CharField('Breed', max_length=255, blank=True)
    age = models.IntegerField('Age in month')
    userdog = models.ManyToManyField(User)
    gender = models.CharField(
        'Gender',
        max_length=1,
        choices=get_choices_with_unknown(Gender)
    )
    size = models.CharField(
        'Size',
        max_length=2,
        choices=get_choices_with_unknown(Size)
    )
    objects = DogManager()

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name

    @property
    def age_class(self):
        if self.age <= 12:
            return Age.baby.value
        elif self.age <= 24:
            return Age.young.value
        elif self.age <= 72:
            return Age.adult.value
        else:
            return Age.senior.value

    def update_userdog_status(self, user, status):
        try:
            userdog = UserDog.objects.get(
                user=user,
                dog=self,
            )
            userdog.status = status
            userdog.save()
        except UserDog.DoesNotExist:
            userdog = UserDog.objects.create(
                user=user,
                dog=self,
                status=status
            )

    def set_userdog_undecided(self, user):
        try:
            userdog = UserDog.objects.get(
                user=user,
                dog=self,
            )
            userdog.delete()
        except UserDog.DoesNotExist:
            pass


class UserDogManager(models.Manager):
    def get_userdogs_dog_ids_status_by_user(self, user, status):
        return self.filter(user=user, status=status).values_list('dog_id', flat=True)

    def get_userdogs_dog_ids_decided_by_user(self, user):
        return self.filter(user=user).values_list('dog_id', flat=True)


class UserDog(models.Model):
    user = models.ForeignKey(User, related_name='likes')
    dog = models.ForeignKey(Dog, related_name='votes')
    status = models.CharField(
        'Status',
        max_length=1,
        choices=get_choices_with_unknown(Status))

    objects = UserDogManager()

    class Meta:
        unique_together = ['user', 'dog']

    def __str__(self):
        return "{} {} {}".format(self.user, self.status, self.dog)


class UserPref(models.Model):
    user = models.OneToOneField(User, related_name='preferences')
    age = models.CharField(
        choices=get_choices(Age),
        max_length=50,
    )
    gender = models.CharField(
        choices=get_choices(Gender),
        max_length=50,
    )
    size = models.CharField(
        choices=get_choices(Size),
        max_length=50,
    )

    def __str__(self):
        return "{} {} {}".format(self.age, self.gender, self.size)


