from flask import Blueprint, request, render_template
from server.models import Scores


blueprint = Blueprint('views', __name__)


@blueprint.route('/')
# @cache.cached(timeout=60)
def index():
    difficulty = request.args.get('diff', 0)

    top_scores = (Scores.query
                  .order_by(Scores.score.desc())
                  .filter_by(difficulty=difficulty)
                  .limit(10)
                  .all())
    return render_template('scores.html', top_scores=top_scores)


@blueprint.route('/about')
def about():
    return render_template('about.html')
