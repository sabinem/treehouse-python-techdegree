"""admin for accounts app
- uses custom user model"""
from django.contrib import admin

from . import models


class UserAdmin(admin.ModelAdmin):
    search_fields = ['name', 'email']
    list_display = ['name', 'email', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff', 'date_joined']

    def get_name(self, obj):
        return obj.userprofile.name

admin.site.register(models.User, UserAdmin)

