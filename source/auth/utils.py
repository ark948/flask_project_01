from source.auth import bp
from source.models.user import User
from source import db
from icecream import ic
ic.configureOutput(includeContext=True)

from convertdate import persian

@bp.add_app_template_filter
def to_persian(dt):
    return persian.from_gregorian(int(dt.strftime("%Y")), int(dt.strftime("%m")), int(dt.strftime("%d")))

def insert_user_object(username, email, password, confirm):
    try:
        new_user_object = User(username, email)
    except Exception as user_creation_error:
        ic(user_creation_error)
        return False
    if password == confirm:
        try:
            new_user_object.set_password(password)
            db.session.add(new_user_object)
            db.session.commit()
            return True
        except Exception as user_insertion_error:
            ic(user_insertion_error)
            return False
    else:
        return False
    
def check_username_availability(username):
    found = None
    try:
        found = User.query.filter_by(username=username).one()
    except Exception as read_error:
        # print(read_error)
        return False
    if found is None:
        return False
    else:
        return True