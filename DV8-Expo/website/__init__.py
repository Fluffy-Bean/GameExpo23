from flask import Flask, render_template, request, redirect, flash
from flask_login import login_required, login_user, logout_user, current_user
from flask_assets import Bundle
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from website.models import Users
from website.extensions import db, migrate, login_manager, assets
from website.config import INSTANCE_DIR, MIGRATION_DIR


class LoginForm(FlaskForm):
    uuid = StringField(
        "uuid",
        validators=[DataRequired()],
        render_kw={"placeholder": "12345678-ABCD-ABCD-ABCD-123456789EFG"},
    )


app = Flask(__name__, instance_path=INSTANCE_DIR)
app.config.from_pyfile("config.py")

db.init_app(app)
migrate.init_app(app, db, directory=MIGRATION_DIR)
with app.app_context():
    db.create_all()

assets.init_app(app)
styles = Bundle(
    "sass/styles.sass",
    filters="libsass, cssmin",
    output="gen/packed.css",
    depends="sass/*.sass",
)
assets.register("styles", styles)
scripts = Bundle("js/*.js", filters="jsmin", output="gen/packed.js")
assets.register("scripts", scripts)


@login_manager.user_loader
def load_user(user_id):
    return Users.get(user_id)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if user := Users.query.filter_by(uuid=str(form.uuid)).first():
            login_user(user, remember=True)
            return redirect(index)
        else:
            flash("Inncorrect login")

    return render_template("login.html", form=form)
