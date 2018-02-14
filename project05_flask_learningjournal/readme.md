# Learning Journal
- 5th project for [Treehouse Techdegree Python](https://teamtreehouse.com/techdegree/python-web-development)
- [detailed requirements for the project](docs/assignment.md)

## Description
The app builds a learning journal for one person
- the user registers with a title and copyright-name
- the journal is password protected
- the journal consists of log entries, resources and tags
- markdown can be used for the descriptions

## Programming languages, frameworks, libraries
- [Flask](http://flask.pocoo.org/) (Python Framework)
- [Peewee](http://docs.peewee-orm.com/) (SQLite-ORM)
- [Markdown](https://de.wikipedia.org/wiki/Markdown)

## Installation
- Download the zip file to your computer and unzip
- Go into the directory
- Install a virtual environment:
    `virtualenv -p python3 p3venv`
- Activate the virtuale environment:
    `source p3venv/bin/activate`
- Install the requirements
    `pip install -r requirements.txt`

## Start application
Start the application with
    `python3 runserver.py`
