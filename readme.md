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
7. Create a user with `python mange.py createsuperuser`
8. Run the project with `python manage.py runserver`
9. Login to the admin by going to `/admin` on the localhost
10. Test with `coverage run manage.py test`
11. Look at the coverage report with `coverage report`


