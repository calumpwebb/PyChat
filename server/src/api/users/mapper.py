from marshmallow import Schema, fields, post_load

from src import db


class UserSchema(Schema):
    id = fields.Integer()
    created_datetime = fields.DateTime()
    username = fields.String(required=True)
    password = fields.Str(required=True)

    @post_load
    def make_user(self, data):
        return db.User(
            username=data['username'],
            password=data['password']
        )
