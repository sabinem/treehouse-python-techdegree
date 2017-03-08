"""
admin for the user profiles
- user and profile are defined as seperate entities in the admin
"""
from django.contrib import admin
from . import models


admin.site.register(models.Profile)
