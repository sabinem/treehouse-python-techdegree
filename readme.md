# Project 9 Treehouse Techdegree Python

## Task description
[task description](task_description.md)

## Installation
1. Download the project on your computer
2. Unzip and go into the newly established directory
3. Install a virtual environment:
    `python3 -m venv mc_venv`
4. Activate the virtuale environment:
    `source mc_venv/bin/activate`
5. Install the requirements
    `pip install -r requirements.txt`
6. Migrate the data `python manage.py migrate`
7. Create a user with `python manage.py createsuperuser`
8. Run the project with `python manage.py runserver`
9. Open a browser and login at `http://127.0.0.1:8000/admin`
10. Go to `http://127.0.0.1:8000` and try the site
11. Test with `coverage run manage.py test`
11. Look at the coverage report with `coverage report`


