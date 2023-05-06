from flask import Flask
from flask_assets import Bundle
from extensions import db, migrate, cache, assets
from config import MIGRATION_DIR, INSTANCE_DIR
from views import blueprint

app = Flask(__name__, instance_path=INSTANCE_DIR)
app.config.from_pyfile('config.py')

db.init_app(app)
migrate.init_app(app, db, directory=MIGRATION_DIR)

with app.app_context():
    db.create_all()

assets.init_app(app)
styles = Bundle("style.sass", filters="libsass, cssmin", output="gen/styles.css", depends="style.sass")
assets.register("styles", styles)

cache.init_app(app)
app.register_blueprint(blueprint)
