from marshmallow import Schema, fields, post_load

import db


class UserSchema(Schema):
    id = fields.Integer(required=True)
    created_datetime = fields.DateTime(required=True)
    username = fields.String(required=True)
    password = fields.Str(required=True)

    @post_load
    def make_user(self, data):
        return db.User(**data)
