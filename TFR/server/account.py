import uuid
import re

from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from .config import USER_REGEX, USER_EMAIL_REGEX
from .models import Users, Sessions, Scores, ProfileTags, PasswordReset
from .extensions import db


blueprint = Blueprint("account", __name__, url_prefix="/account")


@blueprint.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        user_regex = re.compile(USER_REGEX)
        email_regex = re.compile(USER_EMAIL_REGEX)
        error = []

        user = Users.query.filter_by(username=current_user.username).first()

        if not check_password_hash(user.password, password):
            flash("Password is incorrect!", "error")
            return redirect(url_for('account.settings'))

        if username:
            if user_regex.match(username):
                user.username = username
            else:
                error.append("Username is invalid!")
        if email:
            if email_regex.match(email):
                user.email = email
            else:
                error.append("Email is invalid!")

        if error:
            for err in error:
                flash(err, "error")
            return redirect(url_for("account.settings"))

        db.session.commit()

        flash("Successfully updated account!", "success")
        return redirect(url_for("account.settings"))
    else:
        action = request.args.get("action", None)

        if action == "logout":
            logout_user()
            flash("Successfully logged out!", "success")
            return redirect(url_for("views.index"))

        sessions = Sessions.query.filter_by(user_id=current_user.id).all()
        return render_template("views/account_settings.html", sessions=sessions)


@blueprint.route("/reset-password", methods=["GET", "POST"])
@login_required
def password_reset():
    if request.method == "POST":
        current = request.form.get("current", "").strip()
        new = request.form.get("new", "").strip()
        confirm = request.form.get("confirm", "").strip()
        error = []

        user = Users.query.filter_by(username=current_user.username).first()

        if not current or not new or not confirm:
            error.append("Please fill out all fields!")
        if not check_password_hash(user.password, current):
            error.append("Current password is incorrect!")
        if len(new) < 8:
            error.append("New password is too short! Must be at least 8 characters long.")
        if new != confirm:
            error.append("New passwords do not match!")

        if error:
            for err in error:
                flash(err, "error")
            return redirect(url_for("account.password_reset"))

        user.password = generate_password_hash(new, method="scrypt")
        user.alt_id = str(uuid.uuid4())
        db.session.commit()

        flash("Successfully changed password!", "success")
        logout_user()
        return redirect(url_for("auth.auth"))
    else:
        return render_template("views/reset_password.html")


@blueprint.route("/delete-account", methods=["GET", "POST"])
@login_required
def delete_account():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        error = []

        user = Users.query.filter_by(username=current_user.username).first()

        if username != user.username:
            error.append("Username does not match!")
        if not password:
            error.append("Please fill out all fields!")
        if not check_password_hash(user.password, password):
            error.append("Password is incorrect!")

        if error:
            for err in error:
                flash(err, "error")
            return redirect(url_for("account.delete_account"))

        db.session.query(Sessions).filter_by(user_id=current_user.id).delete()
        db.session.query(Scores).filter_by(user_id=current_user.id).delete()
        db.session.query(ProfileTags).filter_by(user_id=current_user.id).delete()
        db.session.query(PasswordReset).filter_by(user_id=current_user.id).delete()
        db.session.delete(user)
        db.session.commit()

        flash("Successfully deleted account!", "success")
        logout_user()
        return redirect(url_for("auth.auth"))
    else:
        return render_template("views/delete_account.html")
