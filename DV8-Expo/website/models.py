"""
Database models for the server
"""
from website.extensions import db


class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    downloadLink = db.Column(db.String, nullable=False)
    approved = db.Column(db.Boolean, nullable=False, default=False)


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))


class TriggerWarning(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    warning = db.Column(db.String, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))


class Authros(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False, default='Developer')
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, nullable=False)