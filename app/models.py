from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db
from app import drive
from albums.planche_to_pdf import create_album
from albums.pdf_to_drive import upload_on_drive


def get_class_variables(class_name):
    return {key:value for key, value in class_name.__dict__.items() if not key.startswith('__') and not callable(key)}


class Buyer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    address_1 = db.Column(db.String(120))
    address_2 = db.Column(db.String(120))
    city = db.Column(db.String(120))
    country = db.Column(db.String(120))
    postal_code = db.Column(db.String(64))
    state = db.Column(db.String(120))
    stories = db.relationship('Story', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<Buyer {}>'.format(self.email)


class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(10))
    nickname = db.Column(db.String(64))
    location = db.Column(db.String(64))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.id'))
    album = db.Column(db.String(2083))

    def __repr__(self):
        return '<Story {}>'.format(self.nickname)


    def link_album(self):
        variable_dict = get_class_variables(self)
        album_name = f"{self.nickname.lower()}_{self.location.lower()}"
        create_album(variable_dict, album_name)
        drive_url = upload_on_drive(drive, album_name)
        self.album = drive_url

