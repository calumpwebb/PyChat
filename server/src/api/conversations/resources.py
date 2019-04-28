
from flask_jwt import current_identity, jwt_required
from flask_restplus import Namespace, Resource

from src.api.conversations.queries import get_conversations_ids_and_last_messages, get_conversation_messages
from src import config, db
from src.api.exceptions import NotAuthorised

namespace = Namespace("")


@namespace.route("/conversations", endpoint="converastions")
class ConversationsEndpoint(Resource):
    @jwt_required()
    def get(self):
        """
        Allows retrieving all the conversations (with their last message)
        """

        return get_conversations_ids_and_last_messages(current_identity.id)


@namespace.route("/conversation/<string:conversation_id>", endpoint="conversation")
class ConversationEndpoint(Resource):
    @jwt_required()
    def get(self, conversation_id):
        """
        Allows retreiving all the messages in a conversation (limit
        """

        # validate that conversation id is valid for that user and the conversation exists
        session = config.get_session()
        conversation = session.query(db.Conversation).get(conversation_id)

        if not conversation:
            return NotAuthorised()

        if conversation.user_id_1 != current_identity.id and current_identity.user_id_2 != current_identity.id:
            return NotAuthorised()

        return get_conversation_messages(conversation_id)
