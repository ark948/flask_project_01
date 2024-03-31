from flask import Blueprint

bp = Blueprint('blog', __name__)

from source.blog import routes