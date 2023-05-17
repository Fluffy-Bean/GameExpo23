from flask import Blueprint, render_template, redirect, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from website.models import Users, Games
from website.extensions import db


blueprint = Blueprint("website", __name__)


class LoginForm(FlaskForm):
    uuid = StringField(
        "uuid",
        validators=[DataRequired()],
        render_kw={"placeholder": "12345678-ABCD-ABCD-ABCD-123456789EFG"},
    )


@blueprint.route("/")
def index():
    games = (Games.query
                  .filter_by(approved=True)
                  .filter_by(visible=True)
                  .all())
    return render_template("index.html", games=games)


@blueprint.route("/g/<int:game_id>")
def g(game_id):
    game = (Games.query
                 .filter_by(id=game_id)
                 .filter_by(approved=True)
                 .filter_by(visible=True)
                 .first())

    if not game:
        abort(404)

    return render_template("game.html", game=game)


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if user := Users.query.filter_by(uuid=str(form.uuid.data)).first():
            login_user(user, remember=True)
            return redirect("/")
        else:
            flash("Incorrect login")

    return render_template("login.html", form=form)


@blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
