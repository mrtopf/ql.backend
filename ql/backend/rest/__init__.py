import usermanager
import users, content

def setup_handlers(map):
    """setup the handlers"""
    with map.submapper(path_prefix="/api/1/users") as m:
        m.connect(None, '/names', handler=usermanager.Names)
        m.connect(None, '/login', handler=usermanager.Login)
        m.connect(None, '/token', handler=usermanager.Token)
        m.connect(None, '/u/{username}/profile', handler=usermanager.PoCo)


    """
    with map.submapper(path_prefix="/api/1/tweets") as m:
        #m.connect(None, '/{path_info:.*}', handler = content.ContentHandler)
        # routes for now which use GET and POST on tweets
        m.connect(None, '/', 
                handler = content.ContentHandler)
        m.connect(None, '/{tweet_id}', 
                handler = content.TweetHandler,
                conditions=dict(method=["GET"]))
    """
    users.setup_handlers(map)
    content.setup_handlers(map)
    
