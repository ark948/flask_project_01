from flask import Blueprint, render_template
from app import db

error_handler_bp = Blueprint('error', __name__)

@error_handler_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@error_handler_bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

@error_handler_bp.app_errorhandler(401)
def unauthorized_error(error):
    return render_template('errors/401.html'), 401
