#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
#from flaskext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
import config

# create our little application :)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
app.config['DEBUG'] = config.DEBUG
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['USERNAME'] = config.USERNAME
app.config['PASSWORD'] = config.PASSWORD
#app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

# Scheme
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    text = db.Column(db.String(120), unique=True)

    def __init__(self, title, text):
        self.title = title
        self.text = text

    def __repr__(self):
        return '<Entrie %r>' % self.title