# 6 Project for the Treehous Techdegree
##Mineral catalog

###Install
Download and
Download the project files. We've supplied these files for you to use:

data/minerals.json is a JSON file that contains details about each mineral.

data/images are images of the minerals referenced in minerals.json.

example/index.html is an HTML file that shows the structure of the list view.
This is just a concrete example.
It isn’t meant to be used as a file in the project.
When you’re done, your pages should look like this though.

example/detail.html is an HTML file
that shows the structure of the mineral details view.
This is just a concrete example.
It isn’t meant to be used as a file in the project.
When you’re done, your pages should look like this.

example/css/global.css is the CSS style sheet for the site.
Look at the HTML files to see how these styles are used.

list-preview.png shows how the list page should look when completed.

detail-preview.png shows how the detail page should look when completed.

#task
Use SQLite to store the mineral data.
Open minerals.json and look at the attributes of a mineral.
Write a model to store the mineral data.
Each mineral can have the following attributes.
Some minerals will not have all of these attributes.
name
image filename
image caption
category
formula
strunz classification
crystal system
unit cell
color
crystal symmetry
cleavage
mohs scale hardness
luster
streak
diaphaneity
optical properties
refractive index
crystal habit
specific gravity

#script
Write a script to that constructs a mineral model instance for each mineral in minerals.json
and saves them to a SQLite database.

Create a layout template for the app.
The layout template should contain the title of the site.
You can name the site anything you want.

Create a template and view to show the names of all the minerals.
This view should display the name of each mineral in the database.
Each name in the list is a link to the detail view of the mineral.
See index.html and list-preview.png

Create a mineral details template and view.
The detail view should display the details of the selected mineral.
The details template should contain the mineral’s name, image, and image caption.
Other details that are available about the mineral should be displayed below the image caption.
See detail.html and detail-preview.png.

Use a template filter to display the name of each attribute in title case.

Write unit tests to test that each view is displaying the correct information.
Make the templates match the style used in the example files.
Look at the example HTML files and global.css to determine which id
and class attributes to use on the elements in the pages you generate.

##exceeds:
Display the most common or important details at the top of the details list.
You can decide on what order to display them in.
The other miscellaneous details can be in any order.
Add a link that goes to a random mineral details page.
In addition to those provided, additional styles are added and used.