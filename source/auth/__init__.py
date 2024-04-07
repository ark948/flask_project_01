from flask import Blueprint
from source.auth.admin import bp as admin_bp

bp = Blueprint('auth', __name__)
bp.register_blueprint(admin_bp, url_prefix='admin')

from source.auth import routes