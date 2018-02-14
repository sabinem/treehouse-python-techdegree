"""data import for pugorugh app
importing dogs from
pugorugh/static/dog_details.json"""
import os
import django
import json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

# pugorugh objects can only be imported after
# django has been setup!
from pugorugh.serializers import DogSerializer
from pugorugh.models import Dog


os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "backend.settings")
django.setup()
count = Dog.objects.all().count()
if count != 0:
    print("The database already existed. Nothing was done.")
    print("--> The database contains {} dogs".format(count))
else:
    with open('pugorugh/static/dog_details.json', 'r') as file:
        data = json.load(file)
        serializer = DogSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            count = Dog.objects.all().count()
            print("The dogs have been sucessfully transferred from file")
            print("--> The database contains now {} dogs".format(count))
        else:
            print(serializer.errors)
