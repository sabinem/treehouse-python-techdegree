# -*- coding: utf-8 -*-
"""
This migraton is used to load the initial data into
the database. The file minerals.json is read and
the images are copied under a new name, that
takes care of special charaters, that the filename
might include
"""
from __future__ import unicode_literals
import json
import os
import csv
from shutil import copyfile

from django.db import migrations
from django.template.defaultfilters import slugify

from mineral_catalog.settings import DATA_DIR, MINERALS_IMAGE_DIR


def load_data(apps, schema_editor):
    """
    This migration reads the datafile of minerals and imports
    it into the database. The images that go along with the data
    are copied into the static directory of the package 'minerals'.
    The data contains duplicates that are eliminated.
    """
    datapath = os.path.join(DATA_DIR, 'minerals.json')
    with open(datapath) as datafile:
        mineralsjson = json.load(datafile)
        minerals_nameset = set()
        Mineral = apps.get_model("minerals", "Mineral")
        for mineral_json in mineralsjson:
            if mineral_json['name'] in minerals_nameset:
                continue
            else:
                minerals_nameset.add(mineral_json['name'])
            mineral = Mineral()
            for key, value in mineral_json.items():
                if key == 'image filename':
                    file = os.path.join(
                        DATA_DIR, 'images', value)
                    if os.path.isfile(file):
                        fileparts = value.split('.')
                        new_filename = '.'.join(
                            [slugify(fileparts[0]),
                             fileparts[-1]])
                        filepath = os.path.join(
                            MINERALS_IMAGE_DIR,
                            new_filename)
                        copyfile(file, filepath)
                        setattr(mineral, 'image_filename', new_filename)
                elif key == 'name':
                    setattr(mineral, 'name', value.capitalize())
                    setattr(mineral, 'mineral_slug', slugify(value))
                else:
                    setattr(mineral, '_'.join(key.split()), value)
            mineral.save()

    datapath = os.path.join(DATA_DIR, 'chemical_elements.csv')
    with open(datapath, newline='') as datafile:
        ChemicalElement = apps.get_model("minerals", "ChemicalElement")
        chemreader = csv.reader(datafile, delimiter=',')
        for row in chemreader:
            ChemicalElement.objects.create(
                code=row[1].strip(),
                name=row[2].strip()
            )


class Migration(migrations.Migration):

    dependencies = [
        ('minerals', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_data),
    ]
