"""
Database models for the server
"""
import uuid
from flask_login import UserMixin
from server.extensions import db


class Scores(db.Model):
    """
    Post table
    Scores supports anonymous posting, and instead just wants to post a score,
    then the username must be provided.Otherwise, it's grabbed from the user table
    """

    __tablename__ = "scores"

    id = db.Column(db.Integer, primary_key=True)

    anonymous = db.Column(db.Boolean, nullable=False, default=False)
    username = db.Column(db.String(32), nullable=True)

    score = db.Column(db.Float, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    scored_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
    )

    scorer = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)


class Users(db.Model, UserMixin):
    """
    User table
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    alt_id = db.Column(db.String, nullable=False, unique=True)

    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    joined_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
    )

    scores = db.relationship("Scores", backref="user", lazy=True)
    tokens = db.relationship("Tokens", backref="user", lazy=True)

    def get_id(self):
        return str(self.alt_id)


class Tokens(db.Model):
    """
    Token table
    """

    __tablename__ = "tokens"

    id = db.Column(db.Integer, primary_key=True)
    holder = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    token = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
    )
