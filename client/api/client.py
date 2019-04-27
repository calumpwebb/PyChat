from api import Base


class ApiClient(Base):
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
