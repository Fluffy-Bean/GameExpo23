from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_assets import Environment
from flask_caching import Cache
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
assets = Environment()
cache = Cache(config={'CACHE_TYPE': 'simple'})
login_manager = LoginManager()
