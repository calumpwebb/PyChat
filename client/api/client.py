from api import Base


class ApiClient(Base):

    # todo: maybe split this file into multiple with each namespace?
    """

    Login Flow

    """

    def authenticate_user(self, username, password):
        post_data = {"username": username, "password": password}

        return self.post_request(self.AUTH_URL, post_data)

    def post_user_sign_up(self, username, password, invitation_token):
        post_data = {
            "username": username,
            "password": password,
            "invitation_token": invitation_token,
        }
        return self.post_request(self.USERS_URL, post_data)

    """
    
    Tokens
    
    """

    def get_all_tokens(self):
        return self.get_request(self.TOKENS_URL)

    def get_new_token(self):
        return self.get_request(self.TOKEN_URL)


    """
    
    Conversations
    
    """

    def get_all_conversations(self):
        return self.get_request(self.CONVERSATIONS_URL)

    def get_conversation_messages(self, conversation_id):
        return self.get_request(self.CONVERSATION_URL.format(conversation_id))
