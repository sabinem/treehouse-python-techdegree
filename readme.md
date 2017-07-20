# User Profile
- 7th project for [Treehouse Techdegree Python](https://teamtreehouse.com/techdegree/python-web-development)
- [detailed requirements for the project](docs/assigment.md)

## Description
This is a userprofile site.
- users can register and are required to fill in some information about them before they are allowed to explore the profile of other users
- the admin user has no profile
- users can upload avatars and transform them on-site

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
- Run `python manage.py migrate`
- Create superuser with `python manage.py createsuperuser`.
   - The password must be 14 Characters, have lower- and uppercase letters,
   special characters and numbers.    

## Start application
Start the application with
    `python manage.py runserver.py`
