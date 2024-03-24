import os

# load .env file later

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'some-random-secure-string-to-be-generated-later'