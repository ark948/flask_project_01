from source.main import bp

@bp.add_app_template_filter
def is_admin_filter(u):
    if u.is_authenticated:
        return u.is_admin()
    else:
        return False