"""
Todo Api with Flask
"""
import json

from flask import (Flask,
    make_response,
    jsonify,
    render_template,
    g,
    request)

from flask_cors import CORS

import webargs
from webargs.flaskparser import parser

from . import config
from . import models

# resources are imported as the api
from .resources.todos import todos_api
from . resources.users import users_api


app = Flask(__name__)

# using CORS
CORS(app)

# API is versioned
url_prefix = '/api/v1'
app.register_blueprint(users_api, url_prefix=url_prefix)
app.register_blueprint(todos_api, url_prefix=url_prefix)


login_args = {
   'username': webargs.fields.Str(required=True),
   'password': webargs.fields.Str(required=True),
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/v1/login', methods=['POST'])
def login():
    args = parser.parse(login_args, request)
    try:
        user = models.User.select().where(
            models.User.username == args['username']).get()
    except models.User.DoesNotExist:
        pass
    else:
        if user and user.verify_password(args['password']):
            token = user.generate_auth_token()
            g.user = user
            g.user.token = token
            return jsonify({'token': token.decode('ascii')})
    return make_response(
        json.dumps({
            'error': 'user and password combination unknown'
        }), 400)


