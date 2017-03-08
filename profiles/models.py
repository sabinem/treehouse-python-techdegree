"""
model for the user profile
- one on one with user
"""
from io import BytesIO
from PIL import Image

from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.db import models
from django.core.files.base import ContentFile


def image_path(instance, filename):
    """sets the upload path for images"""
    return 'images/{}'.format(filename)


def get_filename(filename):
    """the last part of the avatar url is the filename"""
    return filename.split(sep="/")[-1]


class Profile(models.Model):
    """
    user profile
    - primary key is the user
    - date of birth
    - biography
    - avatar
    - avatar thumbnail
    - github account: the username is stored
    - setting for showing the email to other users
    - setting for showing the birthday to other users
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    date_of_birth = models.DateField()
    bio = models.TextField()
    avatar = models.ImageField(
        upload_to=image_path
    )
    show_email = models.BooleanField(
        default=True
    )
    show_birthday = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ['user']

    def __str__(self):
        """
        users are represented by their username
        """
        return self.user.username

    def save(self, new_image=None, *args, **kwargs):
        """
        saves updated avatar image:
        - if new_image is set this is saved as an updated avatar image
        """
        if new_image:
            temp_name = get_filename(self.avatar.name)
            new_image_io = BytesIO()
            new_image.save(new_image_io, format='JPEG')
            self.avatar.delete(save=False)
            self.avatar.save(
                temp_name,
                content=ContentFile(new_image_io.getvalue()),
                save=False
            )
        super().save(*args, **kwargs)
