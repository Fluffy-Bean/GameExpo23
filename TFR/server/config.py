import os

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

GAME_VERSION = "alpha"
GAME_VERSIONS = ["alpha"]
GAME_DIFFICULTIES = [0, 1, 2, 3, 4]

USER_MAX_TOKENS = 3
