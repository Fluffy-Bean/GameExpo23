"""
Database models for the server
"""
from website.extensions import db
from flask_login import UserMixin


class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ageRating = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    thumbnail = db.Column(db.String, nullable=False)
    background = db.Column(db.String, nullable=False)
    downloadLink = db.Column(db.String, nullable=False)
    approved = db.Column(db.Boolean, nullable=False, default=False)


class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))


class Authors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False, default="Developer")
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, nullable=False)

    def get_id(self):
        return int(self.id)
