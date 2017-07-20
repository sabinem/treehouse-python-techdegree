# Learning Journal
- 5th project for [Treehouse Techdegree Python](https://teamtreehouse.com/techdegree/python-web-development)
- [detailed requirements for the project](docs/assigment.md)

###Description
I have am using that journal myself on a daily basis and have
adjusted it to my need: it comes with  the following feature,
additional to the requirements in the Treehouse-Project:
* It is meant for one person only to edit and is password-protected,
so you have to register before you can use it.
* I included a markdown-editor with syntax highlighting
Everything else is explained, just start the application and try.

###Installation
1. Download project on your computer
2. Go into the directory learning_journal
3. Install a virtual environment:
    `virtualenv -p python3 p3venv`
4. Activate the virtuale environment:
    `source p3venv/bin/activate`
5. Install the requirements
    `pip install -r requirements.txt` 

###Start Application
Start the application with
    `python3 runserver.py`

    # Worklog with a Database
    - 4th project for [Treehouse Techdegree Python](https://teamtreehouse.com/techdegree/python-web-development)
    - [detailed requirements for the project](docs/assigment.md)

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
        `python3 -m venv worklogdb`
    - Activate the virtuale environment:
        `source worklogdb/bin/activate`
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
