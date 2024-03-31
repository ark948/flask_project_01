import os
from dotenv import load_dotenv

# load .env file later
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'some-random-secure-string-to-be-generated-later'
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:1234@localhost:5432/flask_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email server
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 8025
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['admin@email.com']

class TestConfig:
    TESTING = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'some-random-secure-string-to-be-generated-later'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

CaptchaConfig = {
    'SECRET_CAPTCHA_KEY': 'LONG_KEY',
    'CAPTCHA_LENGTH': 4,
    'CAPTCHA_DIGITS': True,
    'EXPIRE_SECONDS': 600,
}