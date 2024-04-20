from flask import Blueprint

bp = Blueprint('users_cli', __name__, cli_group='users')

from source.users_cli.commands import *