import re
import uuid

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db
from .models import Users
from .config import USER_REGEX


blueprint = Blueprint("auth", __name__)


@blueprint.route("/auth", methods=["GET"])
def auth():
    return render_template("auth.html")


@blueprint.route("/register", methods=["POST"])
def register():
    # Get the form data
    username = request.form.get("username", None).strip()
    password = request.form.get("password", None).strip()
    confirm = request.form.get("confirm", None).strip()

    username_regex = re.compile(USER_REGEX)
    error = []

    # Validate the form
    if not username or not username_regex.match(username):
        error.append("Username is invalid! Must be alphanumeric, and can contain ._-")
    if not password or len(password) < 8:
        error.append("Password is too short! Must be at least 8 characters long.")
    if not confirm or password != confirm:
        error.append("Passwords do not match!")
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
