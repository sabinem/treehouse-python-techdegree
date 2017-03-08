# Project 7 for Python Tech Degree at Treehouse

## User-Profile Site

### Description
#### Requirements
- has user authentication
- the superuser can only acccess the admin
- a user is supposed to make a profile for himself
- he can upload a picture as his avatar
- there is a dialog, where he can crop rotate or flip his avatar
- he can circle through other users profiles, once he has established his own
- he can see how his profile is presented to other users

#### Profile Fields:
- email
- birthday
- biography
- he can decide whether to show email and or birthday to other users

###Installation
1. Download the project on your computer
2. Unzip and go into the newly established directory
3. Install a virtual environment:
    `python3 -m venv up_venv`
4. Activate the virtuale environment:
    `source up_venv/bin/activate`
5. Install the requirements
    `pip install -r requirements.txt`
   project has external dependencies: Python 3 and Pillow
6. Run `python manage.py migrate`
7. Create superuser with `python manage.py createsuperuser`.
   - The password must be 14 Characters, have lower- and uppercase letters,
   special characters and numbers.
8. Start the application with `python manage.py runserver`



