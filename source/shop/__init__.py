from flask import Blueprint

bp = Blueprint('shop', __name__)

from source.shop import routes