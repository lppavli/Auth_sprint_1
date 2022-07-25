# flask_app/db.py
import redis as redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_db(app: Flask):
    app.config['SECRET_KEY'] = 'SECRET'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://app:123qwe@localhost:5432/movies_database'
    db.init_app(app)
