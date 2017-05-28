import json

from flask import Blueprint, make_response, request

from flask_restful import (Resource, Api)
# for marshaling responses
from flask_marshmallow import Marshmallow

# for parsing requests arguments
import webargs
from webargs.flaskparser import parser

from ..auth import auth
from .. import models


users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
mm = Marshmallow(users_api)


user_register_args = {
   'email': webargs.fields.Str(required=True),
   'username': webargs.fields.Str(required=True),
   'password': webargs.fields.Str(required=True, validate=webargs.validate.Length(min=6)),
   'verify_password': webargs.fields.Str(required=True),
}


class UserSchema(mm.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'email', 'username', 'created_at')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserApi(Resource):
    """User Api: not protected"""
    def get(self):
        all_users = models.User.select()
        result = users_schema.dump(all_users)
        return result.data

    def post(self):
        args = parser.parse(user_register_args, request)
        if args['password'] == args['verify_password']:
            user = models.User.create_user(**args)
            result = user_schema.dump(user)
            return result.data, 201
        return make_response(
            json.dumps({
                'error': 'Password and password verification do not match'
            }), 400)


api.add_resource(UserApi, '/users', endpoint='users')

