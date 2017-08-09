# Social Team Builder
- 12th project for [Treehouse Techdegree Python](https://teamtreehouse.com/techdegree/python-web-development)
- [detailed requirements for the project](docs/assignment.md)
- [project files: html, that should be matched as appereance of the site](docs/projectfiles)

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

## email
- open second terminal window:
- start email server with
```
python -m smtpd -n -c DebuggingServer localhost:1025
```

## Tests
there are some tests, but testing was not part of the project
requirements in this case