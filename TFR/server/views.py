from flask import Blueprint, request, render_template, abort
from sqlalchemy import func

from .models import Scores, Users, TagJunction, Tags
from .config import GAME_VERSION, MAX_TOP_SCORES
from .extensions import db


blueprint = Blueprint("views", __name__)


@blueprint.route("/", methods=["GET"])
def index():
    diff_arg = request.args.get("diff", 0)
    ver_arg = request.args.get("ver", GAME_VERSION).strip()
    user_arg = request.args.get("user", "").strip()
    user = None
    tags = None

    scores = db.session.query(Scores).filter_by(difficulty=diff_arg)

    subquery = (
        db.session.query(Scores.user_id, func.min(Scores.score).label("min"))
        .group_by(Scores.user_id)
        .subquery()
    )

    if ver_arg:
        scores = scores.filter_by(version=ver_arg)

    if not user_arg:
        scores = scores.join(subquery, Scores.user_id == subquery.c.user_id).filter(
            Scores.score == subquery.c.min
        )
    else:
        user = Users.query.filter_by(username=user_arg).first()
        if user:
            scores = scores.filter_by(user_id=user.id)
            tags = (
                db.session.query(Tags)
                .join(TagJunction)
                .filter(TagJunction.user_id == user.id)
                .all()
            )
        else:
            abort(404, "User not found")

    scores = scores.order_by(Scores.score.asc()).limit(MAX_TOP_SCORES).all()

    return render_template(
        "views/scores.html",
        scores=scores,
        diff=int(diff_arg),
        ver=ver_arg,
        user=user,
        tags=tags,
    )


@blueprint.route("/about", methods=["GET"])
def about():
    return render_template("views/about.html")
