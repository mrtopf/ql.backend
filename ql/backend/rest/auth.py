from quantumcore.storages import AttributeMapper

import restclient

class Session(AttributeMapper):
    """a simple dict like user object (which sessions basically are)"""

class Sessions(object):
    """a RAM based session store which stores sessions keyed by tokens"""

    def __init__(self, settings):
        """initialize the session store. ``settings`` is the settings object
        containing the poco endpoint etc."""
        self.sessions = {} # token -> user data
        self.settings = settings
        self.client_id = settings.um_client_id
        self.client_secret = settings.um_client_secret
        self.server = restclient.Server(settings.um_poco_endpoint,
                client_id = self.client_id,
                client_secret = self.client_secret)

    def __getitem__(self, token):
        """try to retrieve a session object for a token. If it's not available
        then try to obtain the PoCo user data from the user manager.
        If that fails, return None, otherwise the session object.  """
        session = self.sessions.get(token,None)
        if session is not None:
            return session

        # try to retrieve the PoCo data for the user "me" with this token
        try:
            data = self.server.get("me", access_token = token)
        except restclient.ClientError:
            return None
        data['roles'] = ["admin"] # TODO: should be slightly more configurable
        session = self.sessions[token] = Session(**data)
        return session

    def get(self, token):
        return self[token]

    def verify(self, token):
        """check if the given token is still active. We delete the user data
        for this token if it exists and try to re-retrieve it."""
        if self.sessions.has_key(token):
            del self.sessions[token]
        return self[token]

