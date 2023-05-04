import os

# Purely to make the code a bit more readable
def env(key):
    return os.getenv(key)

SECRET_KEY = env('FLASK_KEY')
BEARER_TOKEN = env('BEARER_TOKEN')

user = env('DB_USER')
password = env('DB_PASSWORD')
host = env('DB_HOST')
port = env('DB_PORT')
database = env('DB_NAME')

SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_RECYCLE = 621

MIGRATION_DIR = '/data/storage/migrations'
INSTANCE_DIR = '/data/storage/instance'