from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_caching import Cache
from flask_assets import Environment

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
cache = Cache(config={"CACHE_TYPE": "simple"})
assets = Environment()
