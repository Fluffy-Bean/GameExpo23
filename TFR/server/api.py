import re
import shortuuid

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash

from server.models import Scores, Sessions, Users
from server.extensions import db
from server.config import GAME_VERSION, GAME_VERSIONS, GAME_DIFFICULTIES, USER_MAX_TOKENS, MAX_SEARCH_RESULTS, USER_REGEX


blueprint = Blueprint("api", __name__, url_prefix="/api")


@blueprint.route("/tokens", methods=["POST"])
@login_required
def tokens():
    session_id = request.form["session_id"]

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
    form = request.form
    error = []

    if not form:
        error.append("No form data provided!")
    if not form["session"]:
        error.append("No session key provided!")
    if not form["version"]:
        error.append("No version provided!")

    if error:
        return jsonify(error), 400

    try:
        int(form["score"])
        int(form["difficulty"])
    except TypeError:
        error.append("Invalid score and difficulty must be valid numbers!")

    if int(form["difficulty"]) not in GAME_DIFFICULTIES:
        error.append("Invalid difficulty!")

    session_data = Sessions.query.filter_by(auth_key=form["session"]).first()
    if not session_data:
        error.append("Authentication failed!")

    if error:
        return jsonify(error), 400

    score = Scores(
        score=int(form["score"]),
        difficulty=int(form["difficulty"]),
        version=form["version"],
        user_id=session_data.user_id,
    )

    db.session.add(score)
    db.session.commit()

    return "Success!"


@blueprint.route("/search", methods=["GET"])
def search():
    search_arg = request.args.get("q")

    if not search_arg:
        return "No search query provided!", 400

    users = Users.query.filter(Users.username.icontains(search_arg)).limit(MAX_SEARCH_RESULTS).all()

    return jsonify([user.username for user in users])


@blueprint.route("/login", methods=["POST"])
def login():
    username = request.form["username"].strip()
    password = request.form["password"].strip()
    device = request.form["device"].strip()
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
        device_type=device
    )
    db.session.add(session)
    db.session.commit()

    return str(session.auth_key)


@blueprint.route("/authenticate", methods=["POST"])
def authenticate():
    auth_key = request.form["auth_key"].strip()

    session = Sessions.query.filter_by(auth_key=auth_key).first()

    if not session:
        return "Invalid session", 400

    user_data = Users.query.filter_by(id=session.user_id).first()

    return jsonify({'username':user_data.username})
