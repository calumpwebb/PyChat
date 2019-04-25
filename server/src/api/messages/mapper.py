from marshmallow import Schema, fields


class MessageSchema(Schema):
    id = fields.Integer(required=True)
    user_id = fields.Str(required=True)
    message = fields.Str(required=True)
    sent_datetime = fields.DateTime(required=True)
    created_datetime = fields.DateTime(required=True)

    username = fields.Str(required=True)
