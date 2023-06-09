from flask import Blueprint, request, render_template
from server.models import Scores


blueprint = Blueprint("views", __name__)


@blueprint.route("/")
# @cache.cached(timeout=60)
def index():
    difficulty = request.args.get("diff", 0)

    scores = (
        Scores.query.filter_by(difficulty=difficulty)
        .order_by(Scores.score.desc())
        .limit(10)
        .all()
    )
    return render_template("scores.html", scores=scores)


@blueprint.route("/about")
def about():
    return render_template("about.html")
