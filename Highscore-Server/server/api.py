import uuid

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from server.models import Tokens, Scores
from server.extensions import db
from server.config import BEARER_TOKEN


blueprint = Blueprint('api', __name__, url_prefix='/api')


@blueprint.route('/tokens', methods=['DELETE', 'POST'])
@login_required
def tokens():
    if request.method == 'DELETE':
        token_id = request.form['token_id']
        if not token_id:
            return jsonify({"error": "No token ID provided!"}), 400

        token = Tokens.query.filter_by(id=token_id).first()
        if not token:
            return jsonify({"error": "Token not found!"}), 404
        if token.holder != current_user.id:
            return jsonify({"error": "You do not own this token!"}), 403

        db.session.delete(token)
        db.session.commit()

        return jsonify({"success": "Token deleted!"}), 200
    elif request.method == 'POST':
        if len(Tokens.query.filter_by(holder=current_user.id).all()) >= 5:
            return jsonify({"error": "You already have 5 tokens!"}), 403

        token = Tokens(token=str(uuid.uuid4()), holder=current_user.id)
        db.session.add(token)
        db.session.commit()

        return jsonify({"success": "Token added!"}), 200


@blueprint.route('/post', methods=['POST'])
def post():
    form = request.form

    if not form:
        return "Invalid form", 400
    if not request.headers.get('Authentication'):
        return "Invalid authentication", 401

    if not isinstance(form['score'], int):
        return "Score must be an integer", 400
    if int(form['score']) < 0:
        return "Score must be greater than 0", 400
    if form['difficulty'] not in [0, 1, 2, 3, 4]:
        # 0 = Easy, Level 1
        # 1 = Easy, Level 2
        # 2 = Easy, Level 3
        # 3 = Normal
        # 4 = Hard
        return "Invalid difficulty", 400

    if token_data := Tokens.query.filter_by(token=request.headers.get('Authentication')).first():
        # User is authenticated
        # This is a registered user

        score = Scores(
            score=form['score'],
            difficulty=form['difficulty'],
            achievements=form['achievements'],
            user_id=token_data.holder,
        )
        db.session.add(score)
        db.session.commit()

        return "Success!", 200
    elif request.headers.get('Authentication') == BEARER_TOKEN:
        # User is not authenticated, but has the correct token
        # This is an anonymous user

        if not form['playerName'] or len(form['playerId']) != 4:
            return "Invalid player name", 400

        score = Scores(
            anonymous=True,
            username=form['playerName'],
            score=form['score'],
            difficulty=form['difficulty'],
        )
        db.session.add(score)
        db.session.commit()

        return "Success!", 200

    return "Authentication failed", 401
