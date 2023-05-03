"""
Database models for the server
"""
from server.extensions import db


class Scores(db.Model):
    """
    Post table
    """
    __tablename__ = "scores"

    id = db.Column(db.Integer, primary_key=True)

    score = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String, nullable=False)
    achievements = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    scored_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
    )


class Users(db.Model):
    """
    User table
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    steam_uuid = db.Column(db.String, unique=True, nullable=False)
    steam_name = db.Column(db.String, nullable=False)

    scores = db.relationship('Scores', backref='user', lazy=True)

    creation_data = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
    )
