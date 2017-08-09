"""
Tests for accounts models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from teambuilder.models import Skill, Project, Position


User = get_user_model()


newuser_valid = {
    "email": "roger@gmail.com",
    "password": "password1"
}
newuser_invalid = {
    "email": "",
    "password": "password2",
}
newadminuser_valid = {
    "email": "admin@gmail.com",
    "password": "password3"
}
newuser1 = {
    "name": "Roger Moore",
    "email": "roger@gmail.com",
    "bio": "Math Student",
    "password": "password2",
}
newuser2 = {
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



class CustomUserModelManagerTest(TestCase):
    """Model Tests for Custom User Model Manager"""
    def test_create_user_valid(self):
        """a user can be created with just email
        and password"""
        user_count = User.objects.all().count()
        User.objects.create_user(**newuser_valid)
        self.assertEqual(User.objects.all().count(), user_count + 1)

    def test_create_user_without_email(self):
        """a user can not be created without
        email"""
        with self.assertRaises(ValueError):
            User.objects.create_user(**newuser_invalid)

    def test_create_superuser(self):
        """a superuser is created with privileges
        email"""
        user = User.objects.create_superuser(**newadminuser_valid)
        self.assertEquals(user, User.objects.get(email=newadminuser_valid['email']))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class CustomUserModelTest(TestCase):
    """Models Test for Custom User"""
    def setUp(self):
        """users are set up along with skills, projects,
        positions and applications"""
        self.user1 = User.objects.create(**newuser1)
        self.user2 = User.objects.create(**newuser2)
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

    def test_get_user_skills(self):
        """a users skills should be returned"""
        self.assertSetEqual(
            set(self.user1.get_user_skills()),
            {self.skill1, self.skill3})

    def test_get_short_name(self):
        """the short name of a user should be the email"""
        self.assertEquals(self.user1.get_short_name(), self.user1.email)

    def test_user_repr(self):
        """user is printed by his name"""
        self.assertEquals(str(self.user1), self.user1.name)

    def test_get_user_projects(self):
        """a users skills should be returned"""
        self.assertSetEqual(
            set(self.user1.get_user_projects()),
            {self.project1})

    def test_get_user_jobs(self):
        """a users past jobs are returned"""
        self.assertSetEqual(
            set(self.user1.get_user_jobs()),
            {self.position1})

    def test_get_user_projects_needs(self):
        """all needs that appear in the
        users projects are returned"""
        self.assertSetEqual(
            set(self.user1.get_user_projects_needs()),
            {self.skill2})


