from flask import (
    Blueprint
)

bp = Blueprint('admin', __name__)

from source.admin import routes