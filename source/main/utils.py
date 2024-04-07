from source.main import bp
from source.models.user import User
from flask_login import current_user

@bp.add_app_template_filter
def is_admin_filter(u):
    if u.is_authenticated:
        return u.is_admin()
    else:
        return False