from os import getenv


UPLOAD_DIR = "/data/uploads"
UPLOAD_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]
UPLOAD_RESOLUTION = (512, 512)
UPLOAD_MAX_SIZE = 3 * 1024 * 1024  # 3MB

GAME_VERSION = "alpha"
GAME_VERSIONS = ["alpha"]
GAME_DIFFICULTIES = [0, 1, 2, 3, 4]

USER_REGEX = r"\b[A-Za-z0-9._-]+\b"
USER_EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"

MAX_TOP_SCORES = 15
MAX_SEARCH_RESULTS = 5

# Postgres
SECRET_KEY = getenv("FLASK_KEY")

user = getenv("DB_USER")
password = getenv("DB_PASSWORD")
host = getenv("DB_HOST")
db = getenv("DB_NAME")

SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{user}:{password}@{host}:5432/{db}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_RECYCLE = 621

"""
# SQLite
SECRET_KEY = "dev"
SQLALCHEMY_DATABASE_URI = "sqlite:///tfr.db"
"""
