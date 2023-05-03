from flask import Flask
from server.extensions import db, migrate, cache
from server.views import blueprint

app = Flask(__name__)
app.config.from_pyfile('config.py')

db.init_app(app)
migrate.init_app(app, db)
cache.init_app(app)

db.create_all(app=app)

app.register_blueprint(blueprint)
