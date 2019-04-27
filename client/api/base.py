import requests

from settings import Configuration


class Base:
    BASE_URL = Configuration.API_URL

    USERS_URL = "/v1/users"
    AUTH_URL = "/auth"

    # TODO: retries?

    def build_url(self, route):
        return self.BASE_URL + route

    def post_request(self, route, data):

        url = self.build_url(route)

        return requests.post(url, json=data)
