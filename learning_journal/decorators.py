"""
This file collects custom decorators
"""
from functools import wraps
from flask import g, request, redirect, url_for


def owner_required(f):
    """
    This decorator prevents routes, when no owner of the
    journal is established yet and redirects to registering
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.owner is None:
            return redirect(url_for('register', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
