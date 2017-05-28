# Todo Api with Flask and Angular

## Install
1. Download the project on your computer
2. Unzip and go into the newly established directory
3. Install a virtual environment: `python3 -m venv fa_venv`
4. Activate the virtuale environment: `source fa_venv/bin/activate`
5. Install the requirements `pip install -r requirements.txt`

## Run the server
- Run the project with `python runserver.py`

## Try the todo app
- go to `http://127.0.0.1:8000`
- login with username `testuser`and password: `treehouse`
- you can then start you todo-list

## Testcoverage
- `coverage run tests.py`
- `coverage report -m`

## UserApi
- there is a fully functional and testcovered user api, which is
not used by the angular app so far

### Explore the User Api
to explore ist:

- open another terminal window and install httpie with
`pip install httpie`

using **httpie** in that new window you can:
- you can get all users at `http  GET  http://127.0.0.1:8000/api/v1/users`
- you can also post a new user at http  `POST  http://127.0.0.1:8000/api/v1/users username="something"`
- follow the instructions, that the api returns to you
- with this new user you can log in at `http://127.0.0.1:8000` and continue working on your list