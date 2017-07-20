# Detailed Assignment

## Python Techdegree Treehouse Project 6

This project was an assignment of [Treehouse Techdegree Python](https://teamtreehouse.com/techdegree/python-web-development). Below you find the original description of the project.

## Description

As part of your job, you’ve been asked to build a website that displays information about various minerals (AKA rocks). The home page of the site contains a list of all of the minerals in a database. Clicking on a mineral’s name opens a page that displays information about the mineral.

A web designer has already designed the pages. You only need to write the code to created the pages as they’ve been designed. Use the included HTML/CSS files to see how to structure and style the pages. You don’t need to alter global.css - just use it as is.

## Project Instructions

### Use SQLite to store the mineral data.
Open minerals.json and look at the attributes of a mineral. Write a model to store the mineral data. Each mineral can have the following attributes. Some minerals will not have all of these attributes.
- name
- image filename
- image caption
- category
- formula
- strunz classification
- color
- crystal system
- unit cell
- crystal symmetry
- cleavage
- mohs scale hardness
- luster
- streak
- diaphaneity
- optical properties
- refractive index
- crystal habit
- specific gravity
Write a script to that constructs a mineral model instance for each mineral in minerals.json and saves them to a SQLite database.
### Create a layout template for the app.
The layout template should contain the title of the site. You can name the site anything you want.
### Create a template and view to show the names of all the minerals.
This view should display the name of each mineral in the database. Each name in the list is a link to the detail view of the mineral. See index.html and list-preview.png
### Create a mineral details template and view.
The detail view should display the details of the selected mineral.
The details template should contain the mineral’s name, image, and image caption. Other details that are available about the mineral should be displayed below the image caption. See detail.html and detail-preview.png.
### Use a template filter to display the name of each attribute in title case.
### Write unit tests to test that each view is displaying the correct information.
### Make the templates match the style used in the example files.
Look at the example HTML files and global.css to determine which id and class attributes to use on the elements in the pages you generate.

## Extra Credit

- Display the most common or important details at the top of the details list. You can decide on what order to display them in. The other miscellaneous details can be in any order.
- Add a link that goes to a random mineral details page.
- In addition to those provided, additional styles are added and used.
