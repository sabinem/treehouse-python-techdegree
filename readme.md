# Mineral Catalog
- 8th project for [Treehouse Techdegree Python](https://teamtreehouse.com/techdegree/python-web-development)
- [detailed requirements for the project](docs/assigment.md)

## Description
The app is a mineral search site searching a given mineral database
- extension of an earlier project [project 6](https://github.com/sabinem/python_techdegree_project6_mineral_catalog)

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

## Data
- the mineral data is provided as [csv file `data/minerals.json`](data/minerals.json)
- analysis of the data, see [`data/README.md`](data/README.md)
- load the data with `python manage.py migrate`:
this will load the data into the database and copy the image-files
into the static directory `minerals/static/minerals/images` directory.

## Start application
Start the application with `python manage.py runserver.py`

## Test coverage
- Run: `coverage run manage.py test`
- Then see the coverage report at: `coverage report`
