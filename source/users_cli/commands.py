from source.users_cli import bp
from source import db
from source.models.user import User

@bp.cli.command('test')
def test_users_cli():
    print("testing users cli...")
    print("-> done.")

@bp.cli.command('list')
def users_list():
    users_list = User.query.all()
    for i in users_list:
        print(f"id: {i.id} - Username: {i.username}")
    print("-> done.")

@bp.cli.command('total')
def total_number_of_users():
    print(f"Total no. of users: {len(User.query.all())}")
    print("-> done.")