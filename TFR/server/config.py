import os


GAME_VERSION = "alpha"
GAME_VERSIONS = ["alpha"]
GAME_DIFFICULTIES = [0, 1, 2, 3, 4]

USER_MAX_TOKENS = 3
USER_REGEX = r"\b[A-Za-z0-9._-]+\b"

MAX_TOP_SCORES = 15
MAX_SEARCH_RESULTS = 5

# Postgres
SECRET_KEY = os.getenv("FLASK_KEY")

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
db = os.getenv("DB_NAME")

SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{user}:{password}@{host}:5432/{db}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_RECYCLE = 621

MIGRATION_DIR = "/data/storage/migrations"
INSTANCE_DIR = "/data/storage/instance"

"""
# SQLite
SECRET_KEY = "dev"
SQLALCHEMY_DATABASE_URI = "sqlite:///tfr.db"
"""
