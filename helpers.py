from flask import redirect, render_template, request, session
from functools import wraps
from models import db, Users

def login_required(f): # This function code was taken from cs50x problem set 9 - Finance
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin = Users.query.filter_by(id=session.get("user_id"), user_type='admin').first()
        if not admin:
            return render_template("forbidden.html")
        return f(*args, **kwargs)
        
    return decorated_function