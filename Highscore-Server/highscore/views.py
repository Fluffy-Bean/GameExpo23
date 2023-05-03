from flask import Blueprint, jsonify, render_template_string, request, abort
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

from models import Scores, Users
from extensions import db, cache

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
    users = Users.query.all()
    return render_template_string('''
        <h1>Top Scores</h1>
        <table>
            <tr>
                <th>Score</th>
                <th>Difficulty</th>
                <th>Achievements</th>
                <th>Player</th>
            </tr>
            {% for score in top_scores %}
                <tr>
                    <td>{{ score.score }}</td>
                    <td>{{ score.difficulty }}</td>
                    <td>{{ score.achievements }}</td>
                    <td>{{ score.user.steam_name }}</td>
                </tr>
            {% endfor %}
        </table>
        
        <h1>Players</h1>
        <table>
            <tr>
                <th>Steam ID</th>
                <th>Steam Name</th>
            </tr>
            {% for user in users %}
                <tr>
                    <td>{{ user.steam_uuid }}</td>
                    <td>{{ user.steam_name }}</td>
                </tr>
            {% endfor %}
        </table>
        ''', top_scores=top_scores, users=users)


@blueprint.route('/post', methods=['POST'])
def post():
    form = ScoreForm()

    if not form:
        return "Invalid form", 400
    if request.headers.get('Authentication') != 'Bearer 1234':
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


