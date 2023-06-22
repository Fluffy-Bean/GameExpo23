from random import randint

from flask import Flask, render_template, abort
from flask_assets import Bundle
from werkzeug.exceptions import HTTPException

from .extensions import db, migrate, cache, assets, login_manager
from .models import Users
from . import views, auth, api, filters


app = Flask(__name__)
app.config.from_pyfile("config.py")

db.init_app(app)
migrate.init_app(app, db)

with app.app_context():
    db.create_all()

login_manager.init_app(app)
login_manager.login_view = "auth.auth"

assets.init_app(app)

scripts = Bundle("js/*.js", filters="jsmin", output="gen/scripts.js", depends="js/*.js")
assets.register("scripts", scripts)

styles = Bundle(
    "sass/style.sass",
    filters="libsass, cssmin",
    output="gen/styles.css",
    depends="sass/*.sass",
)
assets.register("styles", styles)

cache.init_app(app)
app.register_blueprint(views.blueprint)
app.register_blueprint(auth.blueprint)
app.register_blueprint(api.blueprint)
app.register_blueprint(filters.blueprint)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(alt_id=user_id).first()


@app.errorhandler(Exception)
def error_page(err):
    if not isinstance(err, HTTPException):
        abort(500)

    return (
        render_template(
            "error.html", error=err.code, msg=err.description, image=str(randint(1, 3))
        ),
        err.code,
    )
