from flask import Flask
from flask_migrate import init as migrate_init
from extensions import db, migrate, cache
from views import blueprint

app = Flask(__name__)
app.config.from_pyfile('config.py')

db.init_app(app)
migrate.init_app(app, db)
cache.init_app(app)

with app.app_context():
    db.create_all()
    migrate_init()

app.register_blueprint(blueprint)
