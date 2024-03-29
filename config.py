import os

# load .env file later
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'some-random-secure-string-to-be-generated-later'
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:1234@localhost:5432/flask_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig:
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