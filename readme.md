# Mineral Catalog
- 6th project for [Treehouse Techdegree Python](https://teamtreehouse.com/techdegree/python-web-development)
- [detailed requirements for the project](docs/assigment.md)

## Description
The app is a mineral search site searching a given mineral database
- the user registers with a title and copyright-name
- the journal is password protected
- the journal consists of log entries, resources and tags
- markdown can be used for the descriptions

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

## Data
- the mineral data is provided as [csv file `data/minerals.json`](data/minerals.json)
- analysis of the data, see [`data/README.md`](data/README.md)

## Load the data
- with `python manage.py migrate`:
this will load the data into the database and copy the image-files
into the static directory `minerals/static/minerals/images` directory.

## Start application
Start the application with
    `python manage.py runserver.py`
