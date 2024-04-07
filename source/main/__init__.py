from flask import Blueprint

bp = Blueprint('main', __name__)

# utils must be imported for template filters to work
from source.main import routes, utils