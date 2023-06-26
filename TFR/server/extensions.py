import logging
from os import path

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_assets import Environment
from flask_caching import Cache
from flask_login import LoginManager

from .config import LOGS_DIR

logger = logging
logger.getLogger(path.join(LOGS_DIR, "server.log"))
logger.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)

db = SQLAlchemy()
migrate = Migrate()
assets = Environment()
cache = Cache(config={"CACHE_TYPE": "simple"})
login_manager = LoginManager()
