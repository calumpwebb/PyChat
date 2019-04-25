# TODO: Implment proper exceptions here
# from json import JSONEncoder

# https://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable
# This will monkey-patch json module when it's imported so JSONEncoder.default()
# automatically checks for a special "to_json()" method and uses it to encode the object if found.

#
# def _default(self, obj):
#     return getattr(obj.__class__, "to_json", _default.default)(obj)
#
#
# _default.default = JSONEncoder().default
# JSONEncoder.default = _default


class JsonSerializable(object):
    message = None
    status_code = None

    def __init__(self, payload=None):
        self.payload = payload

    def to_json(self):
        result = {"message": self.message, "status_code": self.status_code}

        if self.payload:
            result["payload"] = self.payload

        return result


class NotAuthorised(JsonSerializable):
    message = "Not authorised for this resource"
    status_code = 401

