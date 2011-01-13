class UserManagerError(Exception):
    """just a base class for all exceptions around the user manager"""
    
class UserNotFound(UserManagerError):
    """a user was not found in the database"""
    
    msg = "The user was not found"
    
    def __init__(self, username):
        self.username = username
        
class ClientNotFound(UserManagerError):
    """exception raised if an unkown client_id is retrieved"""
    
    msg = "The client id is unkown"
    
    def __init__(self, client_id):
        """store client id in question"""
        self.client_id = client_id
        
class AuthorizationCodeNotFound(UserManagerError):
    """exception raised if an unkown auth code is retrieved"""
    
    code = "unauthorized_client"
    msg = "The authorization code was not found or is invalid."
    
    def __init__(self, auth_code):
        self.msg 
        self.auth_code = auth_code
        
class InvalidAuthorizationCode(UserManagerError):
    """exception raised if authorization code and client do not match"""
    
    code = "invalid_client"
    msg = "The authorization does not match the client id"
    
    def __init__(self, auth_code, client_id):
        self.auth_code = auth_code
        self.client_id = client_id
