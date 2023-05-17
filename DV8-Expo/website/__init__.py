from flask import Flask
from flask_assets import Bundle
from website.models import Users
from website.extensions import db, migrate, login_manager, assets
from website.config import INSTANCE_DIR, MIGRATION_DIR
from website import routes


app = Flask(__name__)  # instance_path=INSTANCE_DIR
app.config.from_pyfile("config.py")

db.init_app(app)
migrate.init_app(app, db)  # directory=MIGRATION_DIR
with app.app_context():
    db.create_all()

login_manager.init_app(app)

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

app.register_blueprint(routes.blueprint)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(id=user_id).first()
