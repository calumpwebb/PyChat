from exceptions import ApplicationError

import requests

from settings import Configuration
from state import get_state


class Base:
    BASE_URL = Configuration.API_URL

    USERS_URL = "/v1/users"
    AUTH_URL = "/auth"
    TOKENS_URL = "/v1/tokens"
    TOKEN_URL = "/v1/token"

    # TODO: retries?

    def build_url(self, route):
        return self.BASE_URL + route

    def post_request(self, route, data):

        url = self.build_url(route)

        return requests.post(url, json=data)

    def get_request(self, route, params=None):

        if params is None:
            params = {}

        url = self.build_url(route)

        return requests.get(url, params=params, headers=self.headers())

    def headers(self):
        return {"Authorization": self.jwt_token()}

    @staticmethod
    def jwt_token():
        jwt_token = get_state("app")["jwt_token"]

        if jwt_token == "":
            raise ApplicationError("JWT not available, something must be wrong?")

        # Some reason flask jwt requires it to have JWT at the front
        return "JWT " + jwt_token
