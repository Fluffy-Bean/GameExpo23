from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache
from flask_assets import Environment

db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
assets = Environment()
