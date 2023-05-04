import os

SECRET_KEY = os.getenv('SECRET_KEY')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False

MIGRATION_DIR = '/data/storage/migrations'
INSTANCE_DIR = '/data/storage/instance'