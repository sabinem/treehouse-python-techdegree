from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models
from django.utils import timezone

from teambuilder.models import Position, Skill, Project


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
            
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email,password):
        user = self.create_user(
            email,
            password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField('Avatar', blank=True, null=True, upload_to='avatars/', )
    bio = models.TextField(blank=True)
    skills = models.ManyToManyField(
        Skill,
        related_name='skills',
        blank=True)
    name = models.CharField(max_length=255, blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = "email"
    
    def __str__(self):
        return self.name

    def get_projects(self):
        return self.projects.all()

    def get_jobs(self):
        return self.jobs.all()

    def get_skills(self):
        return self.skills.all()

    def get_short_name(self):
        return self.email