from flask import Blueprint

bp = Blueprint('admin', __name__)

from source.auth.admin import routes