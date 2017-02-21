from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from location_field.models.spatial import LocationField
from io import StringIO
import os

from django.db import models
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage

from PIL import Image

# Thumbnail size tuple defined in an app-specific settings module - e.g. (400, 400)
THUMB_SIZE = (200,200)

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    date_of_birth = models.DateField()
    bio = models.TextField()
    avatar = models.ImageField(
        upload_to='pic_folder/'
    )
    avatar_thumbnail = models.ImageField(
        upload_to='pic_folder/thumbnails/',
        blank=True,
        null=True,
        editable=False,
    )
    show_email = models.BooleanField(default=True)
    show_birthday = models.BooleanField(default=True)
    github_account = models.CharField(blank=True, max_length=20)

    class Meta:
        ordering = ['user']

    def __str__(self):
        return self.user.username

