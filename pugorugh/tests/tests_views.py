"""
Tests for the pugorugh app's views
"""

from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser

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
dog4 = {
    "name": "Cocoa",
    "image_filename": "7.jpg",
    "breed": "Chocolate Labrador Mix",
    "age": 60,
    "gender": "f",
    "size": "l"
}

user1 = {
    "username": "user1",
    "password": "password1"
}
useradmin = {
    "username": "useradmin",
    "password": "password2"
}

LIKED = models.Status.liked.value
DISLIKED = models.Status.disliked.value
UNDECIDED = models.Status.undecided.value

class PugorughViewTest(APITestCase):
    """Tests the Model Mineral"""
    def setUp(self):
        """a mineral is set up"""
        self.dog1 = models.Dog.objects.create(**dog1)
        self.dog2 = models.Dog.objects.create(**dog2)
        self.dog3 = models.Dog.objects.create(**dog3)
        self.dog4 = models.Dog.objects.create(**dog4)
        self.user = models.User.objects.create(**user1)
        self.user_unauthorized = AnonymousUser()
        self.userpref = models.UserPref.objects.get_or_create(
            user=self.user
        )
        self.useradmin = models.User.objects.create(**useradmin)
        self.dog1.update_userdog_status(status=LIKED, user=self.user)
        self.dog2.update_userdog_status(status=DISLIKED, user=self.user)
        self.dog3.update_userdog_status(status=UNDECIDED, user=self.user)
        self.client = APIClient()
        self.client_unauthorized = APIClient()
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token.key
        )

    def test_userdog_retrieve_next_liked_view(self):
        resp = self.client.get('/api/dog/-1/liked/next/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.data,
            {'id': 1, 'name': 'Francesca', 'image_filename': '1.jpg', 'breed': 'Labrador', 'age': 72, 'gender': 'f',
             'size': 'l'}
        )

    def test_userdog_retrieve_next_liked_view_404(self):
        resp = self.client.get('/api/dog/99/liked/next/')
        self.assertEqual(resp.status_code, 404)

    def test_userdog_retrieve_next_disliked_view(self):
        resp = self.client.get('/api/dog/-1/disliked/next/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.data,
            {'id': 2, 'name': 'Hank', 'image_filename': '2.jpg', 'breed': 'French Bulldog', 'age': 14, 'gender': 'm',
             'size': 's'}
        )

    def test_userdog_retrieve_next_disliked_view_404(self):
        resp = self.client.get('/api/dog/99/disliked/next/')
        self.assertEqual(resp.status_code, 404)

    def test_userdog_retrieve_next_undecided_view(self):
        resp = self.client.get('/api/dog/-1/undecided/next/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.data,
            {'id': 3, 'name': 'Pez', 'image_filename': '6.jpg', 'breed': 'Unknown Mix', 'age': 3, 'gender': 'm',
             'size': 'm'}
        )

    def test_userdog_retrieve_next_undecided_view_404(self):
        resp = self.client.get('/api/dog/99/undecided/next/')
        self.assertEqual(resp.status_code, 404)

    def test_userdog_update_status_liked_view(self):
        resp = self.client.put('/api/dog/3/liked/')
        dog = models.Dog.objects.get(id=3)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(dog.get_userdog_status(self.user), LIKED)

    def test_userdog_update_status_disliked_view(self):
        resp = self.client.put('/api/dog/2/disliked/')
        dog = models.Dog.objects.get(id=2)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(dog.get_userdog_status(self.user), DISLIKED)

    def test_userdog_update_status_undecided_view(self):
        resp = self.client.put('/api/dog/1/undecided/')
        dog = models.Dog.objects.get(id=1)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(dog.get_userdog_status(self.user), UNDECIDED)

    def test_user_preferences_retrieve_update_view_get(self):
        resp = self.client.get('/api/user/preferences/')
        self.assertEqual(resp.status_code, 200)

    def test_user_preferences_retrieve_update_view_put(self):
        resp = self.client.put(
            '/api/user/preferences/',
            data={'age': ['a', 'b'], 'gender': ['m'], 'size': ['s']})
        self.assertEqual(resp.status_code, 200)

    def test_user_preferences_retrieve_update_views_prevent_unauthorized_access(self):
        resp = self.client_unauthorized.get('/api/user/preferences/')
        self.assertEqual(resp.status_code, 401)
        resp = self.client_unauthorized.put('/api/user/preferences/')
        self.assertEqual(resp.status_code, 401)

    def test_userdog_update_status_views_prevent_unauthorized_access(self):
        resp = self.client_unauthorized.put('/api/dog/1/undecided/')
        self.assertEqual(resp.status_code, 401)
        resp = self.client_unauthorized.put('/api/dog/1/liked/')
        self.assertEqual(resp.status_code, 401)
        resp = self.client_unauthorized.put('/api/dog/1/disliked/')
        self.assertEqual(resp.status_code, 401)

    def test_userdog_retrieve_next_views_prevent_unauthorized_access(self):
        resp = self.client_unauthorized.get('/api/dog/-1/undecided/next/')
        self.assertEqual(resp.status_code, 401)
        resp = self.client_unauthorized.get('/api/dog/-1/liked/next/')
        self.assertEqual(resp.status_code, 401)
        resp = self.client_unauthorized.get('/api/dog/-1/disliked/next/')
        self.assertEqual(resp.status_code, 401)

    def test_user_register(self):
        resp = self.client_unauthorized.post(
            '/api/user/',
            data={"username": "user2", "password": "password2"})
        self.assertEqual(resp.status_code, 201)
