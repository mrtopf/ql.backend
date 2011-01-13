from content import Model, Collection
import uuid
import errors

class Token(Model):
    """a security session called Token (used as OAuth Access Token"""
    TYPE = "token"
    _attribs = ['_id', 'username','valid_until','roles','client_id',
                'state','auth_code']
    _defaults = {
            'username' : '',
            'valid_until' : None,
            'client_id' : None,
            'state' : "initialized",
            'roles' : ['admin'],
    }

class AuthorizationManager(Collection):
    """the AuthorizationManager handles everything around OAuth based authorization
    such as access tokens, authorization codes and clients"""

    data_class = Token
    
    client_ids = ['pm'] # our one client id for now
    tokens = {} # the list of tokens this manager manages
    authorization_codes = {} # mapping from code -> access token
    
    def new_token(self, username, client_id):
        """create a new access token and authorization code for it and
        store it related to this user"""
        if client_id not in self.client_ids:
            raise errors.ClientNotFound(client_id)
        _id = unicode(uuid.uuid4())
        token = Token(
                _id= unicode(uuid.uuid4()), 
                username=username, 
                auth_code= unicode(uuid.uuid4()), 
                client_id=client_id,
                state="initialized")
        tid = self.put(token) 
        return tid, token.auth_code
        
    def get_token_for_code(self, authorization_code, client_id):
        """return the token for the given authorization code. Will raise an
        ``AuthorizationCodeNotFound`` exception if it's not found"""
        tokens = self.find({'auth_code' : authorization_code})
        if len(tokens)==1:
            token = tokens[0]
            if token.client_id != client_id:
                raise errors.InvalidAuthorizationCode(authorization_code, client_id)
            if token.state!="initialized":
                raise errors.AuthorizationCodeNotFound(authorization_code)
            token.state="active"
            self.update(token)
            return token
        raise errors.AuthorizationCodeNotFound(authorization_code)
        
    def get_token(self, access_token, default=None):
        r = self.get(access_token)
        if r is None:
            return default
        return r
        
    
    
    
    
