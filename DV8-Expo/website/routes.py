from flask import Blueprint, render_template, redirect, flash
from flask_login import login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from website.models import Users


blueprint = Blueprint("website", __name__)


class LoginForm(FlaskForm):
    uuid = StringField(
        "uuid",
        validators=[DataRequired()],
        render_kw={"placeholder": "12345678-ABCD-ABCD-ABCD-123456789EFG"},
    )


@blueprint.route("/")
def index():
    return render_template("index.html")


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
