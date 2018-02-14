"""this file has the custom user model
of the acounts app"""
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models
from django.utils import timezone

from teambuilder.models import Skill


class UserManager(BaseUserManager):
    """custom user manager"""
    def create_user(self, email, password=None):
        """create a user from email and password"""
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        """create a superuser from email and password"""
        user = self.create_user(
            email,
            password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """custom user model
    includes profile fields, such
    as bio, avatar and skills"""
    email = models.EmailField(
        unique=True
    )
    date_joined = models.DateTimeField(
        default=timezone.now
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(
        'Avatar',
        blank=True,
        null=True,
        upload_to='avatars/'
    )
    bio = models.TextField(
        blank=True
    )
    skills = models.ManyToManyField(
        Skill,
        related_name='skills',
        blank=True
    )
    name = models.CharField(
        max_length=255, blank=True
    )
    objects = UserManager()
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.name

    def get_user_projects(self):
        """gets all projects a user owns"""
        return self.projects.all()

    def get_user_project_ids(self):
        """get the ids of the that a user
        owns"""
        return self.projects.all().values('id')

    def get_user_jobs(self):
        """get all jobs where the user is involved"""
        return self.jobs.all()

    def get_user_skills(self):
        """get all skills that a user has himself"""
        return self.skills.all()

    def get_user_projects_needs(self):
        """get the skills needed in the projects that the user
        owns"""
        return Skill.objects.get_project_needs_for_users_projects(user=self)

    def get_short_name(self):
        """email replaces the name after sign up"""
        return self.email
