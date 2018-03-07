# Worklog with a Database
- 4th project for [Treehouse Techdegree Python](https://teamtreehouse.com/techdegree/python-web-development)
- [detailed requirements for the project](docs/assignment.md)

## Description
The app builds a dialog for a worklog with a database for the employees of a company
- you pick your worklog by entering your username, the log will then be stored in the corresponding csv file.
- you may enter logentries
- you may search your worklog

## Programm languages used
- Python
- Peewee as ORM for SQLite
- dateutils for handeling datetime parsing

## Installation
- Download the zip file to your computer and unzip
- Go into the directory
- Install a virtual environment:
    `virtualenv -p python3 venv`
- Activate the virtuale environment:
    `source venv/bin/activate`
- Install the requirements
    `pip install -r requirements.txt`        

## Run program
- Start the application with `python3 worklog.py`
- The application comes preconfigured with some test data.
So you can immediately try it out.

## Testcoverage
To see the test coverage you can additionally install:
    `pip install -r requirements-test.txt`

After that you get a coverage report by running:
    `python3 manage.py`
