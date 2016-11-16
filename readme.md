# Project 6 Treehouse Techdegree Python
## Mineral Catalog
###Description
The mineral catalog comes with data to be loaded.
It is not password protected and can only be displayed.

###Installation
1. Download the project on your computer
2. Go into the directory mineral_catalog
3. You do not need a virtual environment, since this
project has no external dependencies, other then Python 3

###Analyze Data (optional: you can skip that step)
If you want you can analyze the data by starting
`python3 analyze/analyze_minerals.py` this will output two
testfile `analyze_minerals_summary.txt` and `analyze_minerals_detail.txt`
in you directory: the summary contains information about the data
that resides in `data/minerals.json`. The second file contains all the
different values for each field, that has been found in there.

####Findings
* The data does include 3 duplicates, since the names are not all distinct.
* Some minerals seem to have the same image file.
* Only the group seems
appropriate for a select field.
* All fields are character fields.
* Only the image caption needs to be a Textfield with a length of > 400.
* Some names have to be shortened for the list page

###Load the data into the database
Run:
```
python3 manage.py migrate
```
This will load the data into the database and copy the image-files
into the static directory `minerals/static/minerals/images` directory.

###Start the application
Run:
```
python3 manage.py runserver
```
This will start the application.





