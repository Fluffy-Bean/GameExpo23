import os
from flask import Flask
from extensions import db, migrate, cache
from config import MIGRATION_DIR, INSTANCE_DIR
from views import blueprint

app = Flask(__name__, instance_path=INSTANCE_DIR)
app.config.from_pyfile('config.py')

db.init_app(app)
migrate.init_app(app, db, directory=MIGRATION_DIR)
cache.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(blueprint)
