# -*- coding: utf-8 -*-

#   Proyecto GPM: Generic Project Manager
#   Revisado el 6 Abril de 2013, por Francisco Quiñonez (franqur17@gmail.com)
#   Controlado:
#      - Adolfo Salas
#      - Pablo Sanchez

r"""
Clase config

Establece el path, user, password y otros atributos de la Base de datos con la que interactúa el sistema.
"""
import os


class BaseConfig(object):

    # Get app root path
    # ../../configs/config.py
    _basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    PROJECT = "webapp"
    DEBUG = False
    TESTING = False

    ADMINS = frozenset(['youremail@yourdomain.com'])

    # os.urandom(24)
    SECRET_KEY = 'secret key'


class DevConfig(BaseConfig):

    DEBUG = True

    # ===========================================
    # Flask-Sqlalchemy
    #
    # http://packages.python.org/Flask-SQLAlchemy/config.html
    SQLALCHEMY_ECHO = True
    # Database connection URI, change to suit yourself.
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@127.0.0.1/webapp'
    #SQLALCHEMY_DATABASE_URI = 'mysql://username:password@server/db' # mysql

    # ===========================================
    # Flask-babel
    #
    ACCEPT_LANGUAGES = ['zh']
    BABEL_DEFAULT_LOCALE = 'en'

    # ===========================================
    # Flask-cache
    #
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 60

    # ===========================================
    # Flask-mail
    #
    # Should be imported from env var.
    # https://bitbucket.org/danjac/flask-mail/issue/3/problem-with-gmails-smtp-server
    MAIL_DEBUG = DEBUG
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'gmail_username'
    MAIL_PASSWORD = 'gmail_password'
    DEFAULT_MAIL_SENDER = '%s@gmail.com' % MAIL_USERNAME

    # You should overwrite in production.py
    # Limited the maximum allowed payload to 16 megabytes.
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    USER_AVATAR_UPLOAD_FOLDER = os.path.join(BaseConfig._basedir, 'avatar')


class TestConfig(BaseConfig):
    TESTING = True
    CSRF_ENABLED = False

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@127.0.0.1/webapp'
