from marshmallow import Schema, fields


class UserTokenSchema(Schema):
    created_datetime = fields.String(required=True)

    token_issuer_id = fields.Integer(required=True)
    token_issuer_username = fields.String(required=True)

    token_user_id = fields.Integer()
    token_user_username = fields.String()

    token = fields.String(required=True)

    used_datetime = fields.String()
    used = fields.Boolean(required=True)
