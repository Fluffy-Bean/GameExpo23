from os import getenv
import re


SECRET_KEY = getenv("FLASK_KEY")

UPLOAD_DIR = "/data/uploads"
UPLOAD_EXTENSIONS = ["png", "jpg", "jpeg", "gif", "webp"]
UPLOAD_RESOLUTION = 169
UPLOAD_MAX_SIZE = 3 * 1024 * 1024  # 3MB

GAME_VERSION = "alpha"
GAME_DIFFICULTY = 0

GAME_VERSIONS = {
    "alpha": "Alpha",
    "alpha-expo": "Alpha (Expo Build)",
}
GAME_DIFFICULTIES = {
    0: "Easy - Level 1",
    1: "Easy - Level 2",
    2: "Easy - Level 3",
    3: "Medium",
    4: "Hard",
}

USER_REGEX = re.compile(r"\b[A-Za-z0-9._-]+\b")
USER_EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

MAX_TOP_SCORES = 15
MAX_SEARCH_RESULTS = 5

user = getenv("DB_USER")
password = getenv("DB_PASSWORD")
host = getenv("DB_HOST")
db = getenv("DB_NAME")
port = 5432

SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_RECYCLE = 621

LOGS_DIR = "/data/logs"
