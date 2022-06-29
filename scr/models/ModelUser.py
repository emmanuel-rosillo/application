from .db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    firstName = db.Column(db.String(25), nullable=False)
    lastName = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(80), nullable=False)

    def __init__(self, name, firstName, lastName, email):
        self.name = name
        self.firstName = firstName
        self.lastName = lastName
        self.email = email

    def __repr__(self):
        return f'{self.name}'


class Face(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vectorEyes = db.Column(db.Integer, nullable=False)
    vectorEars = db.Column(db.Integer, nullable=False)
    vectorLips = db.Column(db.Integer, nullable=False)
    pic = db.Column(db.BLOB)
    user = db.Column(db.String(80), nullable=False)

    def __init__(self, vectorEyes, vectorEars, vectorLips, user):
        self.vectorEyes = vectorEyes
        self.vectorEars = vectorEars
        self.vectorLips = vectorLips
        self.user = user

    def face(self, pic, user):
        self.user = user
        self.pic = pic

    def __repr__(self):
        return f'{self.pic, self.user}'


class Tickets(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    fullNameUser = db.Column(db.String(80), nullable=False)
    ticket = db.Column(db.Integer, nullable=False)

    def __init__(self, fullNameUser, ticket):
        self.fullnameUser = fullNameUser
        self.ticket = ticket



