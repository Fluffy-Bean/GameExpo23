import re
import uuid

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from server.extensions import db
from server.models import Users, Sessions
from server.config import USER_REGEX, USER_EMAIL_REGEX


blueprint = Blueprint("auth", __name__)


@blueprint.route("/auth", methods=["GET"])
def auth():
    return render_template("auth.html")


@blueprint.route("/register", methods=["POST"])
def register():
    # Get the form data
    username = request.form["username"].strip()
    email = request.form["email"].strip()
    password = request.form["password"].strip()

    username_regex = re.compile(USER_REGEX)
    email_regex = re.compile(USER_EMAIL_REGEX)
    error = []

    # Validate the form
    if not username or not username_regex.match(username):
        error.append("Username is invalid! Must be alphanumeric, and can contain ._-")
    if not email or not email_regex.match(email):
        error.append("Email is invalid! Must be email format")
    if not password:
        error.append("Password is empty!")
    elif len(password) < 8:
        error.append("Password is too short! Must be at least 8 characters long.")
    if Users.query.filter_by(username=username).first():
        error.append("Username already exists!")

    # If there are errors, return them
    if error:
        for err in error:
            flash(err, "error")
        return redirect(url_for("auth.auth"))

    register_user = Users(
        alt_id=str(uuid.uuid4()),
        username=username,
        email=generate_password_hash(email, method="scrypt"),
        password=generate_password_hash(password, method="scrypt"),
    )
    db.session.add(register_user)
    db.session.commit()

    flash("Successfully registered!", "success")
    return redirect(url_for("auth.auth"))


@blueprint.route("/login", methods=["POST"])
def login():
    # Get the form data
    username = request.form["username"].strip()
    password = request.form["password"].strip()
    username_regex = re.compile(USER_REGEX)

    error = []

    # Validate the form
    if not username or not username_regex.match(username) or not password:
        error.append("Username or Password is incorrect!")

    user = Users.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        error.append("Username or Password is incorrect!")

    # If there are errors, return them
    if error:
        for err in error:
            flash(err, "error")
        return redirect(url_for("auth.auth"))

    login_user(user, remember=True)
    flash("Successfully logged in!", "success")
    return redirect(url_for("views.index"))
