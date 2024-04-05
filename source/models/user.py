from source import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app
from time import time
import jwt
from icecream import ic

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    phone_number = db.Column(db.String(50))
    is_verified = db.Column(db.Boolean, nullable=True, default=False)
    verified_on = db.Column(db.DateTime, nullable=True)
    admin = db.Column(db.Boolean(), default=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256'
        )
    
    def is_admin(self):
        return self.admin
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return db.session.get(User, id)
    
    def get_email_verification_token(self, expires_in=600):
        return jwt.encode(
            {'verify_email': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256'
        )
    
    @classmethod
    def verify_email_verification_token(self, token):
        try:
            result = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['verify_email']
        except Exception as error:
            # if any error occurred, return false, otherwise true
            ic(error)
            return False
        return True
    
    def __repr__(self) -> str:
        return f'<User {self.id}>'
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)