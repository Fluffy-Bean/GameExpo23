from flask import Blueprint, request, render_template, abort
from sqlalchemy import func

from .models import Scores, Users
from .config import GAME_VERSION, MAX_TOP_SCORES
from .extensions import db


blueprint = Blueprint("views", __name__)


@blueprint.route("/")
def index():
    diff_arg = request.args.get("diff", 0)
    ver_arg = request.args.get("ver", GAME_VERSION)
    user_arg = request.args.get("user", None)

    scores = db.session.query(Scores).filter_by(difficulty=diff_arg)

    subquery = (
        db.session.query(Scores.user_id, func.min(Scores.score).label('min'))
        .group_by(Scores.user_id)
        .subquery()
    )

    if ver_arg:
        scores = scores.filter_by(version=ver_arg)

    if not user_arg:
        scores = (
            scores.join(subquery, Scores.user_id == subquery.c.user_id)
            .filter(Scores.score == subquery.c.min)
        )
    else:
        if user := Users.query.filter_by(username=user_arg).first():
            scores = scores.filter_by(user_id=user.id)
        else:
            abort(404, "User not found")

    scores = scores.order_by(Scores.score.asc()).limit(MAX_TOP_SCORES).all()

    return render_template(
        "views/scores.html",
        scores=scores,
        diff=int(diff_arg),
        ver=ver_arg,
        user=user_arg
    )


@blueprint.route("/about")
def about():
    return render_template("views/about.html")
