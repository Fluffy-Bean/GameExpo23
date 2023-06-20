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


class PasswordReset(db.Model):
    """
    Password reset table
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", use_alter=True))

    reset_key = db.Column(db.String, nullable=False, unique=True)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
    )


class Permissions(db.Model):
    """
    Permissions table
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", use_alter=True))

    user_ban = db.Column(db.Boolean, default=False)
    user_warn = db.Column(db.Boolean, default=False)

    score_removal = db.Column(db.Boolean, default=False)
    score_edit = db.Column(db.Boolean, default=False)

    admin_panel = db.Column(db.Boolean, default=False)
    admin_promote = db.Column(db.Boolean, default=False)
    admin_demote = db.Column(db.Boolean, default=False)


class ProfileTags(db.Model):
    """
    Profile Tags table
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", use_alter=True))

    tag = db.Column(db.String, nullable=False)


class Users(db.Model, UserMixin):
    """
    User table
    """

    id = db.Column(db.Integer, primary_key=True)
    alt_id = db.Column(db.String, nullable=False, unique=True)

    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    joined_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
    )

    scores = db.relationship("Scores", backref=db.backref("users", lazy=True))
    tokens = db.relationship("Sessions", backref=db.backref("users", lazy=True))
    reset = db.relationship("PasswordReset", backref=db.backref("users", lazy=True))
    tags = db.relationship("ProfileTags", backref=db.backref("users", lazy=True))

    def get_id(self):
        return str(self.alt_id)
