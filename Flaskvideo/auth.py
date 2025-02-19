from flask import session, redirect
from functools import wraps

ALLOWED_EXTENSIONS = {'mp4', 'png', 'jpg', 'jpeg'}


def get_current_user():
    user = None
    if 'user' in session:
        user = session['user']
    return user


def is_authorised():
    return get_current_user() is not None


def authorised_only(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if is_authorised():
            return f(*args, **kwargs)
        redirect('/')
    return wrapper


def is_file_allowed(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS