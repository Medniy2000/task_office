from flask import jsonify


def template(data, code=500):
    return {"messages": {"errors": data}, "status_code": code}


UNKNOWN_ERROR = template([], code=500)


class InvalidUsage(Exception):
    status_code = 500

    def __init__(self, messages, status_code=500, payload=None):
        Exception.__init__(self)
        self.messages = template(data=messages, code=status_code)
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_json(self):
        rv = self.messages
        return jsonify(rv)

    @classmethod
    def unknown_error(cls):
        return cls(**UNKNOWN_ERROR)
