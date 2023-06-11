"""
Database models for the server
"""
import uuid
from flask_login import UserMixin
from server.extensions import db
from server.config import GAME_VERSION


class Scores(db.Model):
    """
    Post table
    Scores supports anonymous posting, and instead just wants to post a score,
    then the username must be provided. Otherwise, it's grabbed from the user
    table
    """
    id = db.Column(db.Integer, primary_key=True)

    score = db.Column(db.Float, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    scored_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
    )
    posted_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
    )

    version = db.Column(db.String, default=GAME_VERSION)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", use_alter=True))


class Tokens(db.Model):
    """
    Token table
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", use_alter=True))
    token = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
    )


class Users(db.Model, UserMixin):
    """
    User table
    """
    id = db.Column(db.Integer, primary_key=True)
    alt_id = db.Column(db.String, nullable=False, unique=True)

    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    joined_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
    )


    scores = db.relationship("Scores", backref=db.backref('users', lazy=True))
    tokens = db.relationship("Tokens", backref=db.backref('users', lazy=True))

    def get_id(self):
        return str(self.alt_id)
