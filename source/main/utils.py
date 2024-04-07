from source.main import bp

@bp.add_app_template_filter
def is_admin_filter(current_user):
    return current_user.is_admin