from flask import Blueprint, request, render_template, abort
from server.models import Scores, Users
from server.config import GAME_VERSION


blueprint = Blueprint("views", __name__)


@blueprint.route("/")
def index():
    diff_arg = request.args.get("diff", 0)
    ver_arg = request.args.get("ver", GAME_VERSION)
    user_arg = request.args.get("user", "")

    scores = Scores.query.filter_by(difficulty=diff_arg)

    if ver_arg:
        scores.filter_by(version=ver_arg)
    if user_arg:
        if user := Users.query.filter_by(username=user_arg).first():
            scores.filter_by(user_id=user.id)
        else:
            abort(404, "User not found")

    scores.order_by(Scores.score.desc()).limit(10).all()

    return render_template("scores.html", scores=scores, diff=int(diff_arg), ver=ver_arg, user=user_arg)


@blueprint.route("/about")
def about():
    return render_template("about.html")
