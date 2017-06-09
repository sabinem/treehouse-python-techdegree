# Pug or Ugh:
- 11th project for Treehouse Techdegree Python

[Project Description]
- You find the project description [here](docs/README.md)

## Install
- Download the project on your computer
- Unzip and go into the newly established directory
- Install a virtual environment: `python3 -m venv dog_venv`
- Activate the virtuale environment: `source dog_venv/bin/activate`
- Install the requirements `pip install -r requirements.txt`
- Establish the database: `python manage.py migrate`
- Load the data: `python pugorugh/scripts/data_import.py`

## Run the server
- `python manage.py runserver`

## Try the application
- go to `http://127.0.0.1:8000`
- register
- use the application: set your preferences and scroll througn the dogs and decide
whether you like them or not!

## Test coverage
- run the tests with `coverage run manage.py test`
- get coverage report with `coverage report`

## React
This project uses React for the frontend. It includes both js and jsx file,
even though in general you can generate js from jsx, see
[here](purorugh/static/jsx/README.md)


1. download / virtual env

2. python manage.py migrate

3. python data_import.py

4. python manage.py runserver

from django.contrib import admin

coverage run manage.py test

Todo Api with Flask and Angular

Install

Download the project on your computer
Unzip and go into the newly established directory
Install a virtual environment: python3 -m venv fa_venv
Activate the virtuale environment: source fa_venv/bin/activate
Install the requirements pip install -r requirements.txt
Run the server

Run the project with python runserver.py
Try the todo app

go to http://127.0.0.1:8000
login with username testuserand password: treehouse
you can then start you todo-list
Testcoverage

coverage run tests.py
coverage report -m
UserApi

there is a fully functional and testcovered user api, which is not used by the angular app so far
Explore the User Api

to explore ist:

open another terminal window and install httpie with pip install httpie
using httpie in that new window you can:

you can get all users at http GET http://127.0.0.1:8000/api/v1/users
you can also post a new user at http POST http://127.0.0.1:8000/api/v1/users username="something"
follow the instructions, that the api returns to you
with this new user you can log in at http://127.0.0.1:8000 and continue working on your list




