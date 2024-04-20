from flask import Blueprint
from source import db

bp = Blueprint('cli', __name__, cli_group=None)

@bp.cli.command('test')
def test_cli():
    print("This is a test.")
    print("-> done.")