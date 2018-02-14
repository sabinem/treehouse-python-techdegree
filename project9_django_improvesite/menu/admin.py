"""
admin for menu app
"""
from django.contrib import admin
from . import models

admin.site.register(models.Item)
admin.site.register(models.Ingredient)


@admin.register(models.Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('season', 'expiration_date',)
    list_filter = ('expiration_date',)
