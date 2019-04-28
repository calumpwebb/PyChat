from flask import Blueprint, Flask
from flask_jwt import JWT
from flask_restplus import Api
from flask_socketio import SocketIO

from src.api.auth import authenticate, identity
from src.config import Configuration
from src.exceptions import ServerTypeError

app = Flask(__name__)

socketio = SocketIO(app)


def set_up_api(api_app):
    from src.api.users.resources import namespace as user_namespace
    from src.api.tokens.resources import namespace as token_namespace
    from src.api.conversations.resources import namespace as conversation_namespace

    app.config["SECRET_KEY"] = Configuration.SECRET_KEY

    JWT(app, authenticate, identity)

    api_authorizations = {
        "apitoken": {"type": "apiKey", "in": "header", "name": "Authorization"}
    }

    v1_blueprint = Blueprint("v1", __name__, url_prefix="/v1")

    api = Api(
        version="1.0",
        title="PyChat API",
        authorizations=api_authorizations,
        validate=False,
    )

    api.init_app(v1_blueprint)

    api.add_namespace(user_namespace)
    api.add_namespace(token_namespace)
    api.add_namespace(conversation_namespace)

    app.register_blueprint(v1_blueprint)


def set_up_websocket(socket_app):
    # socket_app.on_namespace()
    pass


if __name__ == "__main__":
    if Configuration.SERVER_TYPE == "api":
        set_up_api(app)
        app.run(debug=True, host="0.0.0.0", port=8001)
    elif Configuration.SERVER_TYPE == "websocket":
        set_up_websocket(socketio)
        socketio.run(app, host="0.0.0.0", port=5000)
    else:
        raise ServerTypeError("SERVER_TYPE must be either api or websocket")
