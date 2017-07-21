# Detailed Assignment

## Python Techdegree Treehouse Project 6

This project was an assignment of [Treehouse Techdegree Python](https://teamtreehouse.com/techdegree/python-web-development). Below you find the original description of the project.

## Description

Create a profile page that adds details to registered user. Display the details to the profile page that is visible on login. Create a page to edit the profile. The profile page will include first name, last name, email, date of birth, confirm email, short bio and avatar upload. Set up validation for email, date of birth and bio. Date of Birth validation will check for a proper date format: YYYY-MM-DD, MM/DD/YYYY, or MM/DD/YY. Email validation will check that the email addresses match and are in a valid format. Bio validation will check that the bio is 10 characters or longer and properly escapes HTML formatting.

Create a "change password page", that updates the user password. This page will ask for current password, new password and confirm password. Set up validation which checks that the current password is valid, that the new password and confirm password fields match, and that the new password follows the following policy

- must not be the same as the current password
- minimum password length of 14 characters.
- must use of both uppercase and lowercase letters
- must include of one or more numerical digits
- must include of special characters, such as @, #, $
- cannot contain the user name or parts of the user’s full name, such as his first name

## Project Instructions

- Use the supplied HTML/CSS to build and styles the pages.
- Create Django model for user profile
- Add necessary routes
- Update “profile” view to display the user profile with the following fields: First Name, Last Name, Email, Date of Birth, Bio and Avatar. Include a link to edit the profile.
- Create “edit” view with the route “/profile/edit” that allows the user to edit the user profile with the following fields: First Name, Last Name, Email, Date of Birth, Confirm Email, Bio and Avatar.
- Validate user input "Email" field: check that the email addresses match and are in a valid format.
- Validate user input "Date of Birth" field: check for a proper date format (YYYY-MM-DD, MM/DD/YYYY, or MM/DD/YY)
- Validate user input "Bio" field: check that the bio is 10 characters or longer and properly escapes HTML formatting.
- Create “change-password” view with the route “/profile/change_password” that allows the user to update their password using User.set_password() and then User.save(). Form fields will be: current password, new password, confirm password
- Validate user input "Password" fields: check that the old password is correct using User.check_password() and the new password matches the confirm password field and follows the password policy.
- Use CSS to style headings, font, and form.

## Extra Credit

- Add additional form fields to build a more complex form with additional options
- Use HTML5 validation to make sure that required fields are filled out and input is formatted correctly.
- Add an online image editor to the avatar. Include the basic functionality: rotate, crop and flip. PNG mockup supplied.
