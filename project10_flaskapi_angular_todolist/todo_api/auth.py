from flask import g
from flask_httpauth import HTTPTokenAuth
from . import models

auth = HTTPTokenAuth(scheme='Token')


@auth.verify_token
def verify_token(token):
    user = models.User.verify_auth_token(token)
    if user is not None:
        g.user = user
        return True
    return False
