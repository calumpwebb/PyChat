import requests
from settings import Configuration

BASE_URL = Configuration.API_URL

USERS_URL = "/v1/users"
AUTH_URL = "/auth"

# TODO: build API client
# TODO: build API client
# TODO: build API client
# TODO: build API client
# TODO: build API client
# TODO: build API client
# TODO: build API client
# TODO: build API client
# TODO: build API client
# TODO: build API client


def authenticate_user(username, password):

    url = BASE_URL + AUTH_URL

    json_body = {
        "username": username,
        "password": password
    }

    return requests.post(url, json=json_body)


def post_user_sign_up(username, password, invitation_token):

    url = BASE_URL + USERS_URL

    json_body = {
        "username": username,
        "password": password,
        "invitation_token": invitation_token,
    }

    return requests.post(url, json=json_body)
