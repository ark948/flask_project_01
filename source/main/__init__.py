from flask import Blueprint

bp = Blueprint('main', __name__)

from source.main import routes, utils