# Pug or Ugh:
- 11th project for [Treehouse Techdegree Python](https://teamtreehouse.com/techdegree/python-web-development)
- [detailed requirements for the project](docs/assigment.md)

## Description
The app is a dog matching site where users can pick their favorite dogs
and bookmark them.

## Programming languages, frameworks, libraries
- Backend: Django Restframework
- Frontend: React
the frontend was given, but had to be twisted to work with the backend

## Installation
- Download the zip file to your computer and unzip
- Go into the directory
- Install a virtual environment:
    `virtualenv -p python3 p3venv`
- Activate the virtuale environment:
    `source p3venv/bin/activate`
- Install the requirements
    `pip install -r requirements.txt`
- Establish the database: `python manage.py migrate`
- Load the data: `python data_import.py`

## Run the server
- `python manage.py runserver`

## Try the application
- go to `http://127.0.0.1:8000`
- open the tab `Register` and register with any username and password combination
- you will be automatically logged in an able to set your preferences
- scroll througn the dogs and decide on them!
- have fun using and testing the application!

## Test coverage
- run the tests with `coverage run manage.py test`
- get coverage report with `coverage report`

## Remarks
For the React frontend both js and jsx file are included,
even though in general js can be derived from jsx, by using babel
[here](docs/jsx.md)
