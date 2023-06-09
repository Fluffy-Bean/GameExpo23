"""
Database models for the server
"""
from website.extensions import db
from flask_login import UserMixin


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
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))

    def get_id(self):
        return int(self.id)


class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    approved = db.Column(db.Boolean, nullable=False, default=False)
    visible = db.Column(db.Boolean, nullable=False, default=False)

    name = db.Column(db.String, nullable=False)
    studio = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    logo = db.Column(db.String)
    background = db.Column(db.String)

    downloadLink = db.Column(db.String)
    ageRating = db.Column(db.String, nullable=False)

    tags = db.relationship("Tags", backref="game", lazy=True)
    authors = db.relationship("Authors", backref="game", lazy=True)
    images = db.relationship("Images", backref="game", lazy=True)
    owner_id = db.relationship("Users", backref="game", lazy=True)