from flask import (
    abort
)

from functools import wraps
from flask_login import current_user
from source.models.user import User
from source import db

def admin_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin():
            return abort(403)
        return func(*args, **kwargs)
    return decorated_view

def insert_user_admin(username: str, email: str, password: str, admin: bool = False) -> dict:
    response = {}
    try:
        user = User(username, email)
        user.set_password(password)
        user.admin = admin
        try:
            db.session.add(user)
            db.session.commit()
            response.update({
                'result': True,
                'message': 'Successfully added user.'
            })
        except Exception as db_error:
            response.update({
                'result': False,
                'message': db_error
            })
            db.session.rollback()
    except Exception as model_error:
        response.update({
            'result': False,
            'message': model_error
        })
    
    return response