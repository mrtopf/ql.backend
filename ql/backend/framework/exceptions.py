from werkzeug.exceptions import HTTPException
import json

class BadRequest(HTTPException):
    """a bad request with JSON body"""

    code = 400
    payload = {}

    def __init__(self, payload=None):
        Exception.__init__(self, '%d %s' % (self.code, self.name))
        if payload is not None:
            self.payload = payload

    def get_body(self, environ):
        """Get the JSON body."""
        return json.dumps(self.payload)

    def get_headers(self, environ):
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]



