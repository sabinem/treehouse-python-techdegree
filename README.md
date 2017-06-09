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
- Load the data: `python data_import.py`

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

