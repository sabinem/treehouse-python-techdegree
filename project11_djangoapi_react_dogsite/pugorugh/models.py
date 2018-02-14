"""
models for the pugorugh app
"""
from enum import Enum

from django.contrib.auth.models import User
from django.db import models

from multiselectfield import MultiSelectField

DISLIKED = 'd'
UNDECIDED = 'u'
LIKED = 'l'


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


class Status(Enum):
    liked = LIKED
    disliked = DISLIKED
    undecided = UNDECIDED


def get_choices(cls):
    """gets the choices from an Enum as lists of tuples with name and value:
    [('m', male), ('f', 'female)]
    """
    return [(x.value, x.name) for x in cls]


def get_choices_as_string(cls):
    """gets the choice values from an Enum as comma-separated-string:
   'f,m'
   """
    values = [x.value for x in cls]
    return ','.join(values)


class DogManager(models.Manager):
    def get_next_dog_by_status(self, user, pk, status):
        ids_for_status = UserDog.objects.get_userdogs_dog_ids_status_by_user(
            user, status)
        ids_for_userpref = Dog.objects.get_dogs_for_user_preference(user)
        ids_result = [id for id in ids_for_status if id in ids_for_userpref]
        return self.filter(id__in=ids_result).filter(id__gt=pk).first()

    def get_next_dog_undecided(self, user, pk):
        ids_exclude_for_status = \
            UserDog.objects.get_userdogs_dog_ids_decided_by_user(user)
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
        ids_for_userpref = \
            [dog.id for dog in prefdogs_size_gender
             if dog.age_class in userpref.age]
        return ids_for_userpref


class Dog(models.Model):
    """Dogs are stored with a picture and characteristics"""
    name = models.CharField('Name', max_length=255)
    image_filename = models.CharField(max_length=255)
    breed = models.CharField('Breed', max_length=255, blank=True)
    age = models.IntegerField('Age in month')
    gender = models.CharField(
        'Gender',
        max_length=1,
        choices=get_choices(Gender),
        blank=True
    )
    size = models.CharField(
        'Size',
        max_length=2,
        choices=get_choices(Size),
        blank=True
    )
    trained = models.BooleanField(default=False),
    vaccinated = models.BooleanField(default=False)
    objects = DogManager()

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name

    @property
    def age_class(self):
        """the dog age is evaluated against the
        age groups stored in the user preferences"""
        if self.age <= 12:
            return Age.baby.value
        elif self.age <= 24:
            return Age.young.value
        elif self.age <= 72:
            return Age.adult.value
        else:
            return Age.senior.value

    def update_userdog_status(self, user, status):
        """the users relationship towards a dog is updated,
        it is stored in the table UserDog"""
        if status != UNDECIDED:
            userdog, created = UserDog.objects.get_or_create(
                    user=user,
                    dog=self,
                )
            userdog.status = status
            userdog.save()
        else:
            UserDog.objects.filter(
                user=user,
                dog=self,
            ).delete()

    def get_userdog_status(self, user):
        """the status of the users relationship to a dog is
        retrieved from the table UserDog"""
        try:
            userdog = UserDog.objects.get(
                user=user,
                dog=self,
            )
        except UserDog.DoesNotExist:
            return UNDECIDED
        else:
            return userdog.status


class UserDogManager(models.Manager):
    """object manager for UserDog"""
    def get_userdogs_dog_ids_status_by_user(self, user, status):
        """gets the dog ids of all dogs that
        have a relationships to the user given in status"""
        return self.filter(user=user, status=status)\
                   .values_list('dog_id', flat=True)

    def get_userdogs_dog_ids_decided_by_user(self, user):
        """gets the dog ids of all dogs that
        the user is decided on, meaning a UserDog record exists"""
        return self.filter(user=user).values_list('dog_id', flat=True)


class UserDog(models.Model):
    """UserDog stores the relationship between user and dog"""
    user = models.ForeignKey(User, related_name='likes')
    dog = models.ForeignKey(Dog, related_name='votes')
    status = models.CharField(
        'Status',
        max_length=1,
        choices=get_choices(Status))

    objects = UserDogManager()

    class Meta:
        unique_together = ['user', 'dog']

    def __str__(self):
        """the relationship between user and dog is returned as
        user likes dog"""
        return "{} {} {}"\
               .format(self.user, self.get_status_display(), self.dog)


class UserPref(models.Model):
    """UserPref stores the preferences of users towards dogs"""
    user = models.OneToOneField(User, related_name='preferences')
    age = MultiSelectField(
        choices=get_choices(Age),
        max_length=50,
        default=get_choices_as_string(Age)
    )
    gender = MultiSelectField(
        choices=get_choices(Gender),
        max_length=50,
        default=get_choices_as_string(Gender)
    )
    size = MultiSelectField(
        choices=get_choices(Size),
        max_length=50,
        default=get_choices_as_string(Size)
    )

    def __str__(self):
        """the preference of a user is returned as lists of
        age, gender and size choices"""
        return "Age: {}, Gender: {}, Size: {}"\
               .format(self.age, self.gender, self.size)
