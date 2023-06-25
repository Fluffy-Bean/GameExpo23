"""
Database models for the server
"""
from flask_login import UserMixin
from .extensions import db
from .config import GAME_VERSION


class Scores(db.Model):
    """
    Post table
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", use_alter=True))

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


class Sessions(db.Model):
    """
    Sessions table
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", use_alter=True))

    auth_key = db.Column(db.String, nullable=False, unique=True)
    ip_address = db.Column(db.String)
    device_type = db.Column(db.String)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
    )
    last_used = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
    )


class TagJunction(db.Model):
    """
    Tag Junction table
    """

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", use_alter=True))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id", use_alter=True))


class Tags(db.Model):
    """
    Profile Tags table
    """

    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship("TagJunction", backref=db.backref("tags", lazy=True))

    tag = db.Column(db.String, nullable=False)
    icon = db.Column(db.String)
    color = db.Column(db.String)


class Users(db.Model, UserMixin):
    """
    User table
    """

    id = db.Column(db.Integer, primary_key=True)
    alt_id = db.Column(db.String, nullable=False, unique=True)
    superuser = db.Column(db.Boolean, default=False)

    picture = db.Column(db.String)

    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String)
    password = db.Column(db.String, nullable=False)

    joined_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
    )

    scores = db.relationship("Scores", backref=db.backref("users", lazy=True))
    tokens = db.relationship("Sessions", backref=db.backref("users", lazy=True))
    tags = db.relationship("TagJunction", backref=db.backref("users", lazy=True))

    def get_id(self):
        return str(self.alt_id)
