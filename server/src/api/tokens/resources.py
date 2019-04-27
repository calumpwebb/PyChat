import datetime

from flask_jwt import current_identity, jwt_required
from flask_restplus import Namespace, Resource
from sqlalchemy import and_, text

from src import config, db
from src.api.exceptions import TokenLimitReached
from src.api.tokens.mapper import UserTokenSchema
from src.utils import generate_random_string

namespace = Namespace("")


@namespace.route("/token", endpoint="token")
class TokenEndpoint(Resource):
    @jwt_required()
    def get(self):
        """
        Allows a user to retrieve a new invitation token

        # todo: max per user?
        """
        user = current_identity

        session = config.get_session()

        number_of_tokens = session.query(db.UserInviteToken).filter(
            and_(
                db.UserInviteToken.token_issuer_id == user.id,
                db.UserInviteToken.created_datetime
                >= datetime.datetime.utcnow() - datetime.timedelta(days=1),
            )
        ).all()

        if len(number_of_tokens) >= 10:
            return TokenLimitReached()

        token_string_start = generate_random_string(8)
        token_string_end = generate_random_string(8)

        token_string = token_string_start + "-" + token_string_end

        session.add(db.UserInviteToken(token_issuer=user, token=token_string))

        session.commit()

        return {"token": token_string}


@namespace.route("/tokens", endpoint="tokens")
class TokensEndpoint(Resource):
    @jwt_required()
    def get(self):
        """
        Allows a user to retrieve a list of their invitation tokens and
        meta data associated to each token.
        """
        user = current_identity

        tokens_query = """
            SELECT
                TO_CHAR(UIT.created_datetime, 'YYYY-MM-DD HH:MM') as created_datetime,
                UIT.token_issuer_id,
                UIT.token_user_id,
                U_issuer.username as token_issuer_username,
                U_user.username as token_user_username,
                UIT.token,
                UIT.used,
                TO_CHAR(UIT.used_datetime, 'YYYY-MM-DD HH:MM') as used_datetime
            FROM
                user_invite_tokens UIT
            LEFT JOIN
                users U_issuer ON (
                    U_issuer.id = UIT.token_issuer_id
                )
            LEFT JOIN
                users U_user ON (
                    U_user.id = UIT.token_user_id
                )
            WHERE
                UIT.token_issuer_id = :user_id
            ORDER BY
                UIT.created_datetime
        """

        session = config.get_session()
        tokens = session.execute(text(tokens_query).params(user_id=user.id)).fetchall()

        return UserTokenSchema(many=True).dump(tokens)
