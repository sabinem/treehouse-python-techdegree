# Project 9 Treehouse Techdegree Python

## Improve Django Project

### Description
- Use the provided requirements.txt to install needed packages for the project.
- Use django-debug-toolbar to find places where database queries
  run too long or hit the database too many times.
- Use django-debug-toolbar to find places where templates
  aren't properly using inheritance.
- Check that models are using appropriate
fields for the type of data they store. If not,
correct them and create migrations to handle the data.
- Check that forms are using the correct fields and validation. If not, fix.
- Use coverage.py to check the code coverage amount.
Write tests to increase test coverage to at least 75%.

### Extra credit
- Increase test coverage to 90% or above.
- Decrease combined query time on all views to 60ms or less.
- Add migrations to correct existing data when data types change.
- Add custom form validators

## How you will be graded

### Database queries
- No improvement over original number of queries.
- No view has more than 5 queries. Queries take less than 100ms combined.
- Queries take less than 60ms combined.

### Template Inheritance
- Little or no template inheritance is used.
- Templates inherit nicely to reduce the total amount of code written.
- N/A

### Model fields
- Model fields aren't changed.
- Model fields are corrected to store correct value types.
Migrations are included to change the field types.
- Migrations handle converting existing data to new data types.

### Form validation
- No change in form validation.
- Form validation is corrected for proper use of clean(),
clean_field(), and validators.
- Custom validators are written where needed.

### Testing
- Test coverage is below 75%.
- Test coverage is at or above 75%.
- Test coverage is over 90%.

### Python Code Style
- Code is disorganized, difficult to follow. It doesn’t comply with the basic PEP 8 standards.
- The code is clean, readable, and well organized. It complies with most common PEP 8 standards of style.
- N/A

coverage run manage.py test
coverage report

