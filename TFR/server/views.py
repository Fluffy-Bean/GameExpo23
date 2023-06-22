from flask import Blueprint, request, render_template, abort
from .models import Scores, Users
from .config import GAME_VERSION, MAX_TOP_SCORES


blueprint = Blueprint("views", __name__)


@blueprint.route("/")
def index():
    diff_arg = request.args.get("diff", 0)
    ver_arg = request.args.get("ver", GAME_VERSION)
    user_arg = request.args.get("user", None)

    scores = Scores.query.filter_by(difficulty=diff_arg).order_by(Scores.score.asc())

    if ver_arg:
        scores = scores.filter_by(version=ver_arg)
    if user_arg:
        if user := Users.query.filter_by(username=user_arg).first():
            scores = scores.filter_by(user_id=user.id)
            print(user.id)
        else:
            abort(404, "User not found")

    scores = scores.limit(MAX_TOP_SCORES).all()

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
