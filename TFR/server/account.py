import uuid
import os
from PIL import Image

from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from .config import (
    USER_REGEX,
    USER_EMAIL_REGEX,
    UPLOAD_EXTENSIONS,
    UPLOAD_MAX_SIZE,
    UPLOAD_DIR,
    UPLOAD_RESOLUTION,
)
from .models import Users, Sessions, Scores
from .extensions import db


blueprint = Blueprint("account", __name__, url_prefix="/account")


@blueprint.route("/settings", methods=["GET"])
@login_required
def get_settings():
    action = request.args.get("action", None)

    if action == "logout":
        logout_user()
        flash("Successfully logged out!", "success")
        return redirect(url_for("views.index"))

    sessions = Sessions.query.filter_by(user_id=current_user.id).all()
    return render_template("views/account_settings.html", sessions=sessions)


@blueprint.route("/settings", methods=["POST"])
@login_required
def post_settings():
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()
    error = []

    user = Users.query.filter_by(username=current_user.username).first()

    if not check_password_hash(user.password, password):
        flash("Password is incorrect!", "error")
        return redirect(url_for("account.settings"))

    if "file" in request.files and request.files["file"].filename:
        picture = request.files["file"]
        file_ext = picture.filename.split(".")[-1].lower()
        file_name = f"{user.id}.{file_ext}"

        if file_ext not in UPLOAD_EXTENSIONS:
            error.append("Picture is not a valid image!")
        if picture.content_length > UPLOAD_MAX_SIZE:
            error.append(f"Picture must be less than {UPLOAD_MAX_SIZE}MB!")

        image = Image.open(picture.stream)

        # Resizing gifs is more work than it's worth
        if file_ext != "gif":
            image_x, image_y = image.size
            image.thumbnail(
                (min(image_x, UPLOAD_RESOLUTION), min(image_y, UPLOAD_RESOLUTION))
            )

        if error:
            for err in error:
                flash(err, "error")
            return redirect(url_for("account.settings"))

        if user.picture:
            os.remove(os.path.join(UPLOAD_DIR, user.picture))

        user.picture = file_name

        if file_ext == "gif":
            image.save(os.path.join(UPLOAD_DIR, file_name), save_all=True)
        else:
            image.save(os.path.join(UPLOAD_DIR, file_name))

        image.close()

    if username:
        if USER_REGEX.match(username):
            user.username = username
        else:
            error.append("Username is invalid!")
    if email:
        if USER_EMAIL_REGEX.match(email):
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


@blueprint.route("/password", methods=["GET"])
@login_required
def get_password_reset():
    return render_template("views/reset_password.html")


@blueprint.route("/password", methods=["POST"])
@login_required
def post_password_reset():
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


@blueprint.route("/delete-account", methods=["GET"])
@login_required
def get_delete_account():
    return render_template("views/delete_account.html")


@blueprint.route("/delete", methods=["POST"])
@login_required
def post_delete_account():
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
    db.session.delete(user)
    db.session.commit()

    flash("Successfully deleted account!", "success")
    logout_user()
    return redirect(url_for("auth.auth"))
