from flask import request
from flask_restplus import Namespace, Resource
from sqlalchemy import desc, func

import config
import db
from api import NotAuthorised, UserSchema

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
        }
        """
        # TODO: stop people spamming the sign up?
        json_data = request.get_json()

        new_user = UserSchema().load(json_data)

        # check that new user username doesn't already exist
        session = config.get_session()
        check_user = (
            session.query(db.User)
            .filter(func.lower(db.User.username) == new_user.username.lower().strip())
            .one_or_none()
        )

        if check_user:
            return NotAuthorised()

        session.add(new_user)
        session.commit()

        return {}

    def get(self):
        """
        Allows querying either for ALL users OR users which match a certain pattern in their username.

        params:
            search: ::string:: allows searching for users via a matching algorithm (trigram)
            limit: ::int:: allows for returning only a certain number of matches from the search
        """
        search = request.args.get("search")
        limit = request.args.get("limit", default=10)

        session = config.get_session()

        if search:
            users = (
                session.query(db.User)
                .filter(func.similarity(db.User.username, search))
                .order_by(desc(func.similarity(db.User.username, search)))
                .limit(limit)
                .all()
            )
        else:
            users = session.query(db.User).order_by(db.User.username).all()

        return UserSchema(many=True, exclude=["password"]).dump(users)
