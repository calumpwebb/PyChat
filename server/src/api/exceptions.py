# TODO: Implment proper exceptions here
from json import JSONEncoder
from flask_restplus import abort

# https://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable
# This will monkey-patch json module when it's imported so JSONEncoder.default()
# automatically checks for a special "to_json()" method and uses it to encode the object if found.


def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder().default
JSONEncoder.default = _default


class JsonSerializable(object):
    message = None
    status_code = None

    def to_json(self):
        # bit of a hack here but it works nicely
        abort(self.status_code, message=self.message)


class MissingParameters(JsonSerializable):
    status_code = 400

    def __init__(self, missing_params):
        super().__init__()

        self.message = ["{} is required".format(param) for param in missing_params]


class UserAlreadyExists(JsonSerializable):
    status_code = 409

    def __init__(self, username):
        super().__init__()

        self.message = "username '{}' already exists".format(username)


class UserTokenInvalid(JsonSerializable):
    status_code = 401
    message = "Invite Token not valid"


class NotAuthorised(JsonSerializable):
    message = "Not authorised for this resource"
    status_code = 401
