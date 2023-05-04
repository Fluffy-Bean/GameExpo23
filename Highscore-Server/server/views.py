from flask import Blueprint, jsonify, request, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

from models import Scores, Users
from extensions import db, cache
from config import BEARER_TOKEN


blueprint = Blueprint('views', __name__)


class ScoreForm(FlaskForm):
    playerName = StringField('Player Name', validators=[DataRequired()])
    playerId = StringField('Player ID', validators=[DataRequired()])
    score = IntegerField('Score', validators=[DataRequired()])
    difficulty = StringField('Difficulty', validators=[DataRequired()])
    achievements = StringField('Achievements', validators=[DataRequired()])


@blueprint.route('/', methods=['GET'])
@cache.cached(timeout=60)
def index():
    top_scores = Scores.query.order_by(Scores.score.desc()).limit(10).all()
    return render_template('scores.html', top_scores=top_scores, show_sub=True)


@blueprint.route('/post', methods=['POST'])
def post():
    form = ScoreForm()

    if not form:
        return "Invalid form", 400
    if request.headers.get('Authentication') != 'Bearer ' + BEARER_TOKEN:
        return "Invalid authentication", 401

    if not isinstance(form.score.data, int):
        return "Score must be an integer", 400
    if form.score.data < 0:
        return "Score must be greater than 0", 400
    if form.difficulty.data not in ['easy', 'medium', 'hard']:
        return "Invalid difficulty", 400

    user = Users.query.filter_by(steam_uuid=form.playerId.data).first()
    if not user:
        user = Users(
            steam_uuid=form.playerId.data,
            steam_name=form.playerName.data,
        )
        db.session.add(user)
        db.session.commit()

    score = Scores(
        score=form.score.data,
        difficulty=form.difficulty.data,
        achievements=form.achievements.data,
        user_id=user.id,
    )
    db.session.add(score)
    db.session.commit()
    return jsonify({'message': 'Success!'})
