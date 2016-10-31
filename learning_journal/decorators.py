from functools import wraps
from flask import g, request, redirect, url_for

def owner_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.owner is None:
            return redirect(url_for('register', next=request.url))
        return f(*args, **kwargs)
    return decorated_function