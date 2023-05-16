import os


# Purely to make the code a bit more readable
def env(key):
    return os.getenv(key)


SECRET_KEY = env("FLASK_KEY")

SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"

MIGRATION_DIR = "/data/storage/migrations"
INSTANCE_DIR = "/data/storage/instance"
