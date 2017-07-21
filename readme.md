# Improve a Django project
- 9th project for [Treehouse Techdegree Python](https://teamtreehouse.com/techdegree/python-web-development)
- [detailed requirements for the project](docs/assigment.md)

## Description
The task was to improve a simple given Django project

## Programming languages, frameworks, libraries
- [Django](https://www.djangoproject.com/) (Python Framework)

## Installation
- Download the zip file to your computer and unzip
- Go into the directory
- Install a virtual environment:
    `virtualenv -p python3 p3venv`
- Activate the virtuale environment:
    `source p3venv/bin/activate`
- Install the requirements
    `pip install -r requirements.txt`
- Migrate the data `python manage.py migrate`
- Create a user with `python manage.py createsuperuser`    

## Start application
- Start the application with `python manage.py runserver.py`
- Open a browser and login at `http://127.0.0.1:8000/admin`
- Go to `http://127.0.0.1:8000` and try the site

## Test coverage
- Run: `coverage run manage.py test`
- Then see the coverage report at: `coverage report`
