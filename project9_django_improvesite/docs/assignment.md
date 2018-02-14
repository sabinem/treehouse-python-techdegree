# Detailed Assignment

## Python Techdegree Treehouse Project 9

This project was an assignment of [Treehouse Techdegree Python](https://teamtreehouse.com/techdegree/python-web-development). Below you find the original description of the project.

## Description

We spent a weekend doing a hackathon a year or so ago and someone built this project. It's...not the best. It runs kind of slow and has been a real pain to debug and add onto. We need you to go through the project, find where it's inefficient, and fix it. Check the templates for bad inheritance and extra database calls. Check the views for extra views or extra database calls. Check the models to make sure they're using the best fields. Check the forms for proper validation and fields. Basically just check the whole thing over. Oh, and it doesn't have any tests, so please get test coverage up to at least 75%.

## Project Instructions

- Use the provided requirements.txt to install needed packages for the project.
- Use django-debug-toolbar to find places where database queries run too long or hit the database too many times.
- Use django-debug-toolbar to find places where templates aren't properly using inheritance.
- Check that models are using appropriate fields for the type of data they store. If not, correct them and create migrations to handle the data.
- Check that forms are using the correct fields and validation. If not, fix.
- Use coverage.py to check the code coverage amount. Write tests to increase test coverage to at least 75%.

## Extra Credit

- Increase test coverage to 90% or above.
- Decrease combined query time on all views to 60ms or less.
- Add migrations to correct existing data when data types change.
- Add custom form validators
