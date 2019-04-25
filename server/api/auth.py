from sqlalchemy import func

import config
import db


def authenticate(username, password):
    session = config.get_session()

    # username is case insensitive for authentication
    username = username.strip().lower()

    user = (
        session.query(db.User)
        .filter(func.lower(db.User.username) == username)
        .one_or_none()
    )

    if user and user.validate_password(password):
        return user


def identity(payload):
    session = config.get_session()
    user_id = payload["identity"]

    return session.query(db.User).filter_by(id=user_id).first()
