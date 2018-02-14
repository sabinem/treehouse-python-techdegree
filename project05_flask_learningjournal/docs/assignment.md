# Detailed Assignment

## Python Techdegree Treehouse Project 5

This project was an assignment of [Treehouse Techdegree Python](https://teamtreehouse.com/techdegree/python-web-development). Below you find the original description of the project.

## Description

Create a local web interface of a learning journal. The main (index) page will list journal entry titles with a title and date. Each journal entry title will link to a detail page that displays the title, date, time spent, what you learned, and resources to remember. Include the ability to add or edit journal entries. When adding or editing a journal entry, there must be prompts for title, date, time spent, what you learned, resources to remember. The results for these entries must be stored in a database and displayed in a blog style website. The HTML/CSS for this site has been supplied for you.

For each part choose from the tools we have covered in the courses so far. Please don’t employ more advanced tools we haven’t covered yet, even if they are right for the job. However, if you identify a place where a more advanced tool is appropriate, please mention that in a code comment as you and your mentor may want to discuss it later.

## Project Instructions

- Create a Flask project. Add all required dependencies, and create the directory and package structure of the application. Save all static assets into the proper directory.
Use the supplied HTML/CSS to build and styles the pages.
- Create Peewee model classes for journal entries
Add necessary routes
- Create “list” view using the route “/list”. The list view contains a list of journal entries, which displays Title, Date for Entry. Title should be hyperlinked to the detail page for each journal entry. Include a link to add an entry.
- Create “add/edit” view with the route “/entry” that allows the user to add or edit journal entry with the following fields: Title, Date, Time Spent, What You Learned, Resources to Remember.
- Create “details” view with the route “/details” displaying the journal entry with all fields: Title, Date, Time Spent, What You Learned, Resources to Remember. Include a link to edit the entry.
- Add the ability to delete a journal entry.
- Use CSS to style headings, font colors, journal entry container colors, body colors.

## Extra Credit

- Add tags to journal entries. Selecting tag takes you to a list of specific tags and the details pages shows tags.
- Create password protection or user login (provide credentials for code review)
- Routing uses slugs in URLs.
