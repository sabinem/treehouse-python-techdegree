"""
Tests for accounts views
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from teambuilder.models import Skill, Project, Position


User = get_user_model()


user1 = {
    "name": "Roger Moore",
    "email": "roger@gmail.com",
    "bio": "Math Student",
    "password": "password1",
}
credentials1 = {
    "email": "roger@gmail.com",
    "password": "password1",
}
user2 = {
    "name": "Alice Ever",
    "email": "ever@gmail.com",
    "bio": "Microsoft Employee",
    "password": "password2",
}
skill1 = {
    "skill": "php",
    "need": "php developer"
}
skill2 = {
    "skill": "python",
    "need": "python developer"
}
skill3 = {
    "skill": "angular",
    "need": "angular developer"
}
position1 = {
    "title": "cat site",
    "url": "http://cats.com"
}


class AccountsRegisterTest(TestCase):
    """Model Tests for Custom User Model Manager"""
    def test_user_register_view(self):
        """everyone should be able to get to the register view"""
        resp = self.client.get(reverse(
            'accounts:register')
        )
        self.assertEquals(resp.status_code, 200)
        resp = self.client.post(
            reverse('accounts:register'),
            {'email': 'foo@gmail.com',
             'password1': 'bar123',
             'password2': 'bar123'})
        self.assertEquals(resp.status_code, 200)


class AccountsRegisteredUserTest(TestCase):
    def setUp(self):
        """users are set up along with skills, projects,
        positions and applications"""
        self.user1 = User.objects.create(**user1)
        self.user2 = User.objects.create(**user2)
        self.skill1 = Skill.objects.create(**skill1)
        self.skill2 = Skill.objects.create(**skill2)
        self.skill3 = Skill.objects.create(**skill3)
        self.user1.skills.add(self.skill1)
        self.user1.skills.add(self.skill3)
        project1 = {
            "title": "dog site",
            "link": "http://dogs.com",
            "owner": self.user1
        }
        project2 = {
            "title": "cat site",
            "link": "http://cats.com",
            "owner": self.user2
        }
        self.project1 = Project.objects.create(**project1)
        self.project2 = Project.objects.create(**project2)
        position1 = {
            "open": False,
            "developer": self.user1,
            "project": self.project2,
            "skill": self.skill1
        }
        position2 = {
            "open": False,
            "developer": self.user2,
            "project": self.project1,
            "skill": self.skill2
        }
        position3 = {
            "project": self.project2,
            "skill": self.skill3
        }
        self.position1 = Position.objects.create(**position1)
        self.position2 = Position.objects.create(**position2)
        self.position3 = Position.objects.create(**position3)
        test_user1 = User.objects.create_user(email='testuser1',
                                              password='12345')
        test_user1.save()
        test_user2 = User.objects.create_user(email='testuser2',
                                              password='12345')
        test_user2.save()

    def test_user_logout_view(self):
        """after logout the user is redirected to the projects page"""
        resp = self.client.get(reverse(
            'accounts:logout')
        )
        self.assertEquals(resp.status_code, 302)
        self.assertRedirects(resp, reverse('teambuilder:projects'),
                             status_code=302)

    def test_user_login_view_accessible(self):
        """everyone should be able to get to the login view"""
        resp = self.client.get(reverse(
            'accounts:login')
        )
        self.assertEquals(resp.status_code, 200)

    def test_user_login_view(self):
        """login should work and redirect to the profile after success"""
        resp = self.client.get(
            reverse('accounts:profile', )
        )
        self.assertEquals(resp.status_code, 200)
