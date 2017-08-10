"""
This migraton is used to load the initial data into
the database. The file minerals.json is read and
the images are copied under a new name, that
takes care of special charaters, that the filename
might include
"""
import json
import os

from django.db import migrations

from teambuilder_project.settings import BASE_DIR
DATA_DIR = os.path.join(BASE_DIR, 'teambuilder', 'data', 'skills.json')


def load_data(apps, schema_editor):
    """
    This migration reads the datafile of skills and imports
    them it into the database.
    """
    datapath = DATA_DIR
    Skill = apps.get_model("teambuilder", "Skill")
    with open(datapath) as datafile:
        skills = json.load(datafile)
        for skill in skills:
            Skill.objects.create(**skill)


class Migration(migrations.Migration):

    dependencies = [
        ('teambuilder', '0005_auto_20170725_1120'),
    ]

    operations = [
        migrations.RunPython(load_data),
    ]