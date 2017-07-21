# Social Team Builder
- 12th project for [Treehouse Techdegree Python](https://teamtreehouse.com/techdegree/python-web-development)
- [detailed requirements for the project](docs/assignment.md)

## Description
The app is again a mineral search site searching a given mineral database
- the queries are optimized in this version
- additional search features have been added

## Programming languages, frameworks, libraries
- [Django](https://www.djangoproject.com/) (Python Framework)
- django-debug-toolbar
- coverage is used for determining test-coverage

## Installation
- Download the zip file to your computer and unzip
- Go into the directory
- Install a virtual environment:
    `virtualenv -p python3 p3venv`
- Activate the virtuale environment:
    `source p3venv/bin/activate`
- Install the requirements
    `pip install -r requirements.txt`

- Migrate with `python manage.py migrate`

## Start application
Start the application with `python manage.py runserver.py`

## Test coverage
- Run: `coverage run manage.py test`
- Then see the coverage report at: `coverage report`

##TODO:

1. avatar mit javascript kombinieren
2. projects auf der profile seite speichern:
modelformfactory verstehen!!!

3.
