"""admin forms for the teambuilder app"""
from django.contrib import admin

from . import models


admin.site.register(models.Skill)
admin.site.register(models.Project)
admin.site.register(models.Application)
admin.site.register(models.Position)
