from source.models.user import User

def is_username_available(username: str) -> bool:
    """
    Checks if a given username is available for new user object
    """
    try:
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return False
        else:
            return True
    except Exception as error:
        return False
