from flask import request
from flask_restplus import Namespace, Resource
from sqlalchemy import desc, func

from src import config, db
from src.api.messages.mapper import MessageSchema

namespace = Namespace("")


@namespace.route("/messages", endpoint="messages")
class Messages(Resource):
    def get(self):
        pass
        # TODO: THIS IS COMMENTED OUT BECAUSE SHOULD REALLY
        # BUILD OTHER PARTS FIRST THEN DO THIS WHEN NEEDED
        # E.G. USER MANAGEMENT FLOW (ADDING USERS ETC)
        # """
        # Allows the retrieval of messages from the server.
        #
        # Filters which can be applied are as follows:
        #     user_id
        #
        # params:
        #     search: ::str:: allows for searching messages from search
        #     limit: ::integer:: allows for limiting the number of messages returned
        #     user_id: ::integer:: allows for searching messages from a user_id
        #     order: ::str:: [choices = *newest*, 'oldest', *closest*, 'furthest']] allows for ordering the messages by
        #         created_datetime or similarity index. Can only order by created_datetime if search
        #         is not sent and can only order by similarity index if search is sent
        # """
        # # todo: work out if we should chunk these at max 500 messages
        # search = request.args.get("search") # todo: search
        # user_id = request.args.get("user_id")
        # limit = request.args.get("limit") # could just add or 500 here to limit the size of message
        # order = request.args.get("order", default="desc")
        #
        # session = config.get_session()
        #
        # messages = session.query(
        #     db.Message.id,
        #     db.Message.user_id,
        #     db.Message.message,
        #     db.Message.sent_datetime,
        #     db.Message.created_datetime,
        #     db.User.username,
        # ).join(db.User)
        #
        # if user_id:
        #     # todo: search for user id to make sure valid?
        #     messages = messages.filter_by(id=user_id)
        #
        # # todo: validate order to be a choice of "oldest" or "newest" or "closest" or "furthest"
        # if search:
        #     if order == "furthest":
        #         orderer = func.similarity(db.Message.message, search)
        #     else:
        #         orderer = desc(func.similarity(db.Message.message, search))
        # else:
        #     if order == "oldest":
        #         orderer = db.Message.created_datetime
        #     else:
        #         orderer = desc(db.Message.created_datetime)
        #
        # messages = messages.order_by(orderer)
        #
        # if limit:
        #     # todo: validate limits
        #     messages = messages.limit(limit)
        # else:
        #     messages = messages.all()
        #
        # return MessageSchema(many=True).dump(messages)
