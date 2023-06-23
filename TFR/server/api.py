import re
import shortuuid

from flask import Blueprint, request, jsonify, send_from_directory
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from .models import Scores, Sessions, Users
from .extensions import db
from .config import (
    GAME_DIFFICULTIES,
    MAX_SEARCH_RESULTS,
    USER_REGEX,
    UPLOAD_DIR,
)


blueprint = Blueprint("api", __name__, url_prefix="/api")


@blueprint.route("/uploads/<filename>", methods=["GET"])
def upload_dir(filename):
    filename = secure_filename(filename)
    return send_from_directory(UPLOAD_DIR, filename)


@blueprint.route("/tokens", methods=["POST"])
@login_required
def tokens():
    session_id = request.form.get("session", "").strip()

    if not session_id:
        return jsonify({"error": "No Session provided!"}), 400

    session = Sessions.query.filter_by(id=session_id).first()

    if not session:
        return jsonify({"error": "Session not found!"}), 404
    if session.user_id != current_user.id:
        return jsonify({"error": "You do not own this session!"}), 403

    db.session.delete(session)
    db.session.commit()

    return jsonify({"success": "Session deleted!"})


@blueprint.route("/post", methods=["POST"])
def post():
    session_key = request.form.get("session", "").strip()
    version = request.form.get("version", "alpha").strip()
    difficulty = request.form.get("difficulty", 0)
    score = request.form.get("score", 0)

    if not session_key:
        return "No session key provided!"
    if not score:
        return "Score is not valid!"

    try:
        float(score)
        int(difficulty)
    except TypeError:
        return "Invalid score and difficulty must be valid numbers!"

    if int(difficulty) not in GAME_DIFFICULTIES:
        return "Invalid difficulty!"
    # This is a fix for a bug in the game that we dunno how to actually fix
    # if score < 10:
    #     return "Score is impossible!"

    session_data = Sessions.query.filter_by(auth_key=session_key).first()
    if not session_data:
        return "Authentication failed!"

    score_upload = Scores(
        score=float(score),
        difficulty=int(difficulty),
        version=version,
        user_id=session_data.user_id,
    )

    session_data.last_used = db.func.now()

    db.session.add(score_upload)
    db.session.commit()

    return "Success!"


@blueprint.route("/search", methods=["GET"])
def search():
    search_arg = request.args.get("q").strip()

    if not search_arg:
        return "No search query provided!", 400

    users = (
        Users.query.filter(Users.username.icontains(search_arg))
        .limit(MAX_SEARCH_RESULTS)
        .all()
    )

    return jsonify([user.username for user in users])


@blueprint.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    device = request.form.get("device", "Unknown").strip()
    username_regex = re.compile(USER_REGEX)

    if not username or not username_regex.match(username) or not password:
        return "Username or Password is incorrect!", 400

    user = Users.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return "Username or Password is incorrect!", 400

    session = Sessions(
        user_id=user.id,
        auth_key=str(shortuuid.ShortUUID().random(length=32)),
        ip_address=request.remote_addr,
        device_type=device,
    )
    db.session.add(session)
    db.session.commit()

    return str(session.auth_key)


@blueprint.route("/authenticate", methods=["POST"])
def authenticate():
    auth_key = request.form.get("session", "").strip()

    session = Sessions.query.filter_by(auth_key=auth_key).first()
    if not session:
        return "Invalid session", 400

    user_data = Users.query.filter_by(id=session.user_id).first()

    return jsonify({"username": user_data.username})
