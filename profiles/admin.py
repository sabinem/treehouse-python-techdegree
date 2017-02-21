from django.contrib import admin
from . import models

# register models
admin.site.register(models.Profile)
admin.site.register(models.TestModel)
