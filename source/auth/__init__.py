from flask import Blueprint

bp = Blueprint('auth', __name__)

from source.auth import routes, utils