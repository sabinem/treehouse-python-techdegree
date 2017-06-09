# Pug or Ugh

## Requirements

Create the models, serializers, and views to power the provided Angular
application. You can check through the supplied JavaScript to see what
resources should be available or check below. You are allowed to change,
extend, and improve the JavaScript if desired, but the final result must still
meet all of the required features/abilities.

You've been provided with HTML and CSS for a basic, mobile-friendly design.
You've also been provided with a starter Django project and application, a
serializer and views for authentication, and a bit more.

## Starting

Create a virtualenv and install the project requirements, which are listed in
`requirements.txt`. The easiest way to do this is with `pip install -r
requirements.txt` while your virtualenv is activated.

If you need to import dogs, a `data_import` script has been provided but it
expects a `DogSerializer` and `Dog` model as outlined below to function
properly.

## Models

The following models and associated field names should be present as they 
will be expected by the JavaScript application.

* `Dog` - This model represents a dog in the app.

	Fields:

	* `name`
	* `image_filename`
	* `breed`
	* `age`, integer for months
	* `gender`, "m" for male, "f" for female, "u" for unknown
	* `size`, "s" for small, "m" for medium, "l" for large, "xl" for extra
	  large, "u" for unknown

* `UserDog` -  This model represents a link between a user an a dog

	Fields:

	* `user`
	* `dog`
	* `status`, "l" for liked, "d" for disliked

* `UserPref` - This model contains the user's preferences

	Fields:

	* `user`
	* `age`, "b" for baby, "y" for young, "a" for adult, "s" for senior
	* `gender`, "m" for male, "f" for female
	* `size`, "s" for small, "m" for medium, "l" for large, "xl" for extra
	  large

	`age`, `gender`, and `size` can contain multiple, comma-separated values

## Serializers

You'll need to provide serializers for both the `Dog` and `UserPref` models.
Each of them should reveal all of the fields with one exception: the `UserPref`
serializer doesn't need to reveal the user.

## Routes

The following routes are expected by the JavaScript application.

* To get the next liked/disliked/undecided dog

	* `/api/dog/<pk>/liked/next/`
	* `/api/dog/<pk>/disliked/next/`
	* `/api/dog/<pk>/undecided/next/`

* To change the dog's status

	* `/api/dog/<pk>/liked/`
	* `/api/dog/<pk>/disliked/`
	* `/api/dog/<pk>/undecided/`

* To change or set user preferences

	* `/api/user/preferences/`

