"""
Tests for the pugorugh app's models
"""

from django.test import TestCase

from .. import models

dog1 = {
    "name": "Francesca",
    "image_filename": "1.jpg",
    "breed": "Labrador",
    "age": 72,
    "gender": "f",
    "size": "l"
}
dog2 = {
    "name": "Hank",
    "image_filename": "2.jpg",
    "breed": "French Bulldog",
    "age": 14,
    "gender": "m",
    "size": "s"
}
dog3 = {
    "name": "Pez",
    "image_filename": "6.jpg",
    "breed": "Unknown Mix",
    "age": 3,
    "gender": "m",
    "size": "m"
}
user1 = {
    "username": "user1",
    "password": "password1"
}
useradmin = {
    "username": "useradmin",
    "password": "password2"
}


class PugorughModelTest(TestCase):
    """Model Tests"""
    def setUp(self):
        self.dog1 = models.Dog.objects.create(**dog1)
        self.dog2 = models.Dog.objects.create(**dog2)
        self.dog3 = models.Dog.objects.create(**dog3)
        self.user = models.User.objects.create(**user1)
        self.userpref, created = models.UserPref.objects.get_or_create(
            user=self.user
        )
        self.useradmin = models.User.objects.create(**useradmin)
        self.user_dog1 = models.UserDog.objects.create(
            dog=self.dog1,
            user=self.user,
            status=models.LIKED
        )
        self.user_dog2 = models.UserDog.objects.create(
            dog=self.dog2,
            user=self.user,
            status=models.DISLIKED
        )

    def test_age_class(self):
        """the age in month should be transformed into a age class for a dog"""
        self.assertEqual(models.Dog(age=12).age_class, models.Age.baby.value)
        self.assertEqual(models.Dog(age=18).age_class, models.Age.young.value)
        self.assertEqual(models.Dog(age=56).age_class, models.Age.adult.value)
        self.assertEqual(models.Dog(age=80).age_class, models.Age.senior.value)

    def test_get_userdogs_dog_ids_status_by_user_liked(self):
        """the dog id for all dogs liked by a user should be returned"""
        test_qs = models.UserDog.objects.get_userdogs_dog_ids_status_by_user(
               user=self.user,
               status=models.LIKED)
        self.assertListEqual(
            list(test_qs),
            [self.dog1.id])

    def test_get_userdogs_dog_ids_status_by_user_disliked(self):
        """the dog id for all dogs disliked by a user should be returned"""
        test_qs = \
            models.UserDog.objects.get_userdogs_dog_ids_status_by_user(
                user=self.user,
                status=models.DISLIKED)
        self.assertListEqual(
            list(test_qs),
            [self.dog2.id])

    def test_get_userdogs_dog_ids_decided_by_user(self):
        """the dog id for all dogs a user is decided on
        should be returned"""
        test_qs = \
            models.UserDog.objects.get_userdogs_dog_ids_decided_by_user(
                user=self.user)
        self.assertListEqual(
            list(test_qs),
            [self.dog1.id, self.dog2.id])

    def test_get_next_dog_undecided(self):
        """the next dog a user is undecided on
        should be returned"""
        self.assertEqual(
            models.Dog.objects.get_next_dog_undecided(
                user=self.user, pk=-1), self.dog3)

    def test_get_next_dog_by_status_liked(self):
        """the next dog a user likes
        should be returned"""
        self.assertEqual(
            models.Dog.objects.get_next_dog_by_status(
                user=self.user, pk=-1, status=models.LIKED), self.dog1)

    def test_get_next_dog_by_status_disliked(self):
        """the next dog a user dislikes
        should be returned"""
        self.assertEqual(
            models.Dog.objects.get_next_dog_by_status(
                user=self.user, pk=-1, status=models.DISLIKED), self.dog2)

    def test_get_userdog_status_liked(self):
        """the status liked should be returned for a dog,
        the user likes"""
        self.assertEqual(
            self.dog1.get_userdog_status(user=self.user), models.LIKED)

    def test_get_userdog_status_disliked(self):
        """the status disliked should be returned for a dog,
        the user dislikes"""
        self.assertEqual(
            self.dog2.get_userdog_status(user=self.user), models.DISLIKED)

    def test_get_userdog_status_undecided(self):
        """the status undecided should be returned for a dog,
        the user is undecided on"""
        self.assertEqual(
            self.dog3.get_userdog_status(user=self.user), models.UNDECIDED)

    def test_update_userdog_status_undecided(self):
        """the status of the dog user relationship should be updated
        to be undecided"""
        self.dog3.update_userdog_status(self.user, status=models.UNDECIDED)
        self.assertEqual(
            models.UserDog.objects.filter(
                dog=self.dog3, user=self.user).count(),
            0)

    def test_update_userdog_status_undecided_after_liked(self):
        """the status of the dog user relationship should be updated
        to be first liked then undecided, checking that
        the status update works correctly"""
        self.dog3.update_userdog_status(
            self.useradmin, status=models.LIKED)
        self.dog3.update_userdog_status(
            self.useradmin, status=models.UNDECIDED)
        self.assertEqual(
            models.UserDog.objects.filter(
                 dog=self.dog3, user=self.useradmin).count(), 0)

    def test_update_userdog_status_disliked(self):
        """the status of the dog user relationship should be updated
        to be disliked"""
        self.dog3.update_userdog_status(self.user, status=models.DISLIKED)
        userdog, created = models.UserDog.objects.get_or_create(
                dog=self.dog3, user=self.user)
        self.assertFalse(created)
        self.assertEqual(userdog.status, models.DISLIKED)

    def test_update_userdog_status_liked(self):
        """the status of the dog user relationship should be updated
        to be liked"""
        self.dog3.update_userdog_status(self.user, status=models.LIKED)
        userdog, created = models.UserDog.objects.get_or_create(
                dog=self.dog3, user=self.user)
        self.assertFalse(created)
        self.assertEqual(userdog.status, models.LIKED)

    def test_dog_str(self):
        """a dog is represented by its name"""
        self.assertEqual(str(self.dog1), self.dog1.name)

    def test_userdog_str(self):
        """a dog user relationship is represented as
        user likes dog"""
        self.assertEqual(
            str(self.user_dog1),
            self.user.username + " " +
            models.Status.liked.name + " " + self.dog1.name)

    def test_userpref_str(self):
        """a user preference is represended as
        Age: a, Gender: m,f, Size: s"""
        self.assertEqual(
            str(self.userpref),
            "Age: {}, Gender: {}, Size: {}".format(
                self.userpref.age, self.userpref.gender, self.userpref.size))
