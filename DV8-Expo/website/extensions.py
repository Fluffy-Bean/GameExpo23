from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_assets import Environment

db = SQLAlchemy()
cache = Cache()
assets = Environment()
