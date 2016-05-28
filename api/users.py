from flask import Blueprint, request, session

from decorators import api_wrapper, WebException
from models import db, User

import utils

blueprint = Blueprint("users", __name__)

@blueprint.route("/register", methods=["POST"])
@api_wrapper
def register():
    form = request.form
    name = form.get("name")
    email = form.get("email")
    password = form.get("password")
    confirm_password = form.get("confirm_password")

    if password != confirm_password:
        raise WebException("Passwords do not match.")

    if len(password) < 4:
        raise WebException("Passwords should be at least four characters long.")

    user = get_user(email=email).first()
    if user is not None:
        raise WebException("Email already in use.")

    user = User(name, email, password)
    db.session.add(user)
    db.session.commit()
    return { "success": 1, "message": "Success!" }

@blueprint.route("/login", methods=["POST"])
@api_wrapper
def login():
    form = request.form
    email = form.get("email")
    password = form.get("password")

    user = get_user(email=email).first()
    if user is None:
        raise WebException("Invalid credentials.")

    if utils.check_hash(user.password, password):
        session["uid"] = user.uid
        session["logged_in"] = True
        return { "success": 1, "message": "Success!" }

    raise WebException("Invalid credentials.")

def is_logged_in():
    return "logged_in" in session and session["logged_in"]

def get_user(uid=None, name=None, email=None):
    match = {}
    if uid is not None:
        match.update({"uid": uid})
    if name is not None:
        match.update({"name": name})
    if email is not None:
        match.update({"email": email})

    return User.query.filter_by(**match)

def get_data():
    data = {}
    logged_in = "logged_in" in session and session["logged_in"]
    user = get_user(session.get("uid")).first()
    if user is not None:
        data["uid"] = user.uid
        data["name"] = user.name
    data["logged_in"] = logged_in
    return data
