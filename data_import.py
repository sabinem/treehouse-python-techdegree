import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from pugorugh.serializers import DogSerializer
from pugorugh.models import Dog

import json

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




