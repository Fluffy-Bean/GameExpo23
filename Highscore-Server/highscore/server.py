import os

from flask import Flask
from flask_migrate import init as migrate_init
from extensions import db, migrate, cache
from config import MIGRATION_DIR, INSTANCE_DIR
from views import blueprint

app = Flask(__name__, instance_path=INSTANCE_DIR)
app.config.from_pyfile('config.py')

db.init_app(app)
migrate.init_app(app, db, directory=MIGRATION_DIR)
cache.init_app(app)

if not os.path.exists(os.path.join(INSTANCE_DIR, 'db.sqlite')):
    with app.app_context():
        db.create_all()

if not os.path.exists(MIGRATION_DIR):
    with app.app_context():
        migrate_init(directory=MIGRATION_DIR)

app.register_blueprint(blueprint)
