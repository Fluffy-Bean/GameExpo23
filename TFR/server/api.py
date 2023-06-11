import shortuuid

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from server.models import Tokens, Scores
from server.extensions import db
from server.config import GAME_VERSION, GAME_VERSIONS, GAME_DIFFICULTIES, USER_MAX_TOKENS


blueprint = Blueprint("api", __name__, url_prefix="/api")


@blueprint.route("/tokens", methods=["DELETE", "POST"])
@login_required
def tokens():
    if request.method == "DELETE":
        token_id = request.form["token_id"]
        if not token_id:
            return jsonify({"error": "No token ID provided!"}), 400

        token = Tokens.query.filter_by(id=token_id).first()
        if not token:
            return jsonify({"error": "Token not found!"}), 404
        if token.user_id != current_user.id:
            return jsonify({"error": "You do not own this token!"}), 403

        db.session.delete(token)
        db.session.commit()

        return jsonify({"success": "Token deleted!"}), 200
    elif request.method == "POST":
        if len(Tokens.query.filter_by(user_id=current_user.id).all()) >= USER_MAX_TOKENS:
            return jsonify({"error": f"You already have {USER_MAX_TOKENS} tokens!"}), 403

        new_string = str(shortuuid.ShortUUID().random(length=20))
        token = Tokens(token=new_string, user_id=current_user.id)
        db.session.add(token)
        db.session.commit()

        return jsonify({"success": "Token added!"}), 200


@blueprint.route("/post", methods=["POST"])
def post():
    form = request.form
    errors = []

    if not form:
        errors += "No form data provided!"
    if not form["token"]:
        errors += "No token provided!"
    if not form["version"]:
        errors += "No version provided!"

    if errors:
        return jsonify(errors), 400

    try:
        int(form["score"])
        int(form["difficulty"])
    except TypeError:
        errors += "Invalid score and difficulty must be valid numbers!"

    if int(form["difficulty"]) not in GAME_DIFFICULTIES:
        errors += "Invalid difficulty!"

    token_data = Tokens.query.filter_by(token=form["token"]).first()
    if not token_data:
        errors += "Authentication failed!"

    if errors:
        return jsonify(errors), 400

    score = Scores(
        score=int(form["score"]),
        difficulty=int(form["difficulty"]),
        version=form["version"],
        user_id=token_data.user_id,
    )

    db.session.add(score)
    db.session.commit()

    return "Success!", 200
