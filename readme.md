# Project 6 Treehouse Techdegree Python
## Mineral Catalog
### Description
The mineral catalog comes with data to be loaded.
It is not password protected and can only be displayed.

### Installation
1. Download the project on your computer
2. Unzip and go into the newly established directory
3. Install a virtual environment:
    `python3 -m venv mc_venv`
4. Activate the virtuale environment:
    `source mc_venv/bin/activate`
5. Install the requirements
    `pip install -r requirements.txt`

### Dependencies
Only for Development purposes django-debug-toolbar and coverage are included
in the dependencies.

### Analyze Data (optional: you can skip that step)
If you want you can analyze the data by starting
`python analyze.py` this will output two
testfile `data_summary.txt` and `data_detail.txt`
in you directory: the summary contains information about the data
that resides in `data/minerals.json`. The second file contains all the
different values for each field, that has been found in there.

### Load the data into the database

Run:
```
python manage.py migrate
```
This will load the data into the database and copy the image-files
into the static directory `minerals/static/minerals/images` directory.

###Start the application
Run:
```
python manage.py runserver
```
This will start the application.

### See test coverage
Run:
`coverage run manage.py test`

Then see the coverage report at:
`coverage report`

