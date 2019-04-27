from flask import request
from flask_restplus import Namespace, Resource, abort
from sqlalchemy import func

from src import config, db
from src.api.exceptions import (MissingParameters, UserAlreadyExists,
                                UserTokenInvalid)
from src.api.users.mapper import UserSchema

namespace = Namespace("")


@namespace.route("/users", endpoint="users")
class UsersEndpoint(Resource):
    def post(self):
        """
        Allows creating a new user.
        Users user names are case insensitive.

        JSON data required:
        {
            "username": "str"
            "password": "str"
            "invitation_token": "str"
        }
        """
        # todo: really not happy with this function in general :(
        json_data = request.get_json()

        if json_data:
            invitation_token = json_data.get("invitation_token")

            if invitation_token is None:
                abort()
                return MissingParameters(["invitation_token"])
            del json_data["invitation_token"]
        else:
            return MissingParameters(["invitation_token", "username", "password"])

        session = config.get_session()

        token = (
            session.query(db.UserInviteToken)
            .filter_by(token=invitation_token)
            .one_or_none()
        )

        if not token:
            return UserTokenInvalid()

        new_user = UserSchema().load(json_data)

        # check that new user username doesn't already exist
        check_user = (
            session.query(db.User)
            .filter(func.lower(db.User.username) == new_user.username.lower().strip())
            .one_or_none()
        )

        if check_user:
            return UserAlreadyExists(check_user.username)

        session.add(new_user)
        token.set_used(new_user)

        session.commit()

        return {}
