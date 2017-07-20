# User Profile
- 7th project for [Treehouse Techdegree Python](https://teamtreehouse.com/techdegree/python-web-development)
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

# Project 7 for Python Tech Degree at Treehouse

## User-Profile Site

### Task

#### Profile Page
Create a profile page that adds details to registered user.
Display the details to the profile page that is visible on login.
Create a page to edit the profile.
The profile page will include:
 - first name, last name, email, date of birth,
confirm email, short bio and avatar upload.

#### Validation
Set up validation for email,
date of birth and bio.
Date of Birth validation will check for a proper date format:
YYYY-MM-DD, MM/DD/YYYY, or MM/DD/YY.
Email validation will check that the email addresses match
and are in a valid format.
Bio validation will check that the bio is 10 characters or
longer and properly escapes HTML formatting.

#### Password-Validation
Create a "change password page", that updates the user password.
This page will ask for current password,
new password and confirm password.
Set up validation which checks that the current password is valid,
that the new password and confirm password fields match,
and that the new password follows the following policy
must not be the same as the current password
minimum password length of 14 characters.
must use of both uppercase and lowercase letters
must include of one or more numerical digits
must include of special characters, such as @, #, $
cannot contain the user name or parts of the user’s full name, such as his first name.

### Extras

The site includes some extras

- a **list**, where users can **"cycle"** through the profiles of all other users
- they can **style their avatar** in a dialog, where they can crop flip and rotate it
- all **forms have a switch** so you can choose between client and serverside validation
- I included two **extra profile fields**, where users can decide whether they want to
show their birthday or email to user users
- the **superuser has no profile** and can only log in and out of the admin
- **regular users must fill in their profile** before they can see other users profiles


### Intentions

I played around a lot with the user profile. My goal was to complete it in a way that I could imagine in a real project:
I did not include many extra fields, but rather put the focus on a smooth workflow:

- I wanted the admin to be extra with no profile:
the superuser is just logged in and out of the admin, he is not part of the real site.
- I imagined the user to be able to sign up,
but he is only able to be part of the community after he finishes his profile, so he is redirected every time he logs in
- once he has filled out his profile, he can see all profiles of other users, to the extent that they allow him

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
