import urllib
import urllib2
import urlparse

try:
    import json
except ImportError:
    import simplejson as json

class ClientError(Exception):

    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self):
        return "<Exception: %s>" %self.msg

class Server(object):
    """models a oauth protected server with resources"""

    def __init__(self, baseurl, 
                client_id=None, 
                client_secret=None, 
                access_token = u"",
                refresh_token=u""):
        """initialize the server with oauth client credentials and the base URL. You
        can also pass in the access and refresh token in case you should have it 
        already."""
        if not baseurl.endswith("/"):
            baseurl = baseurl+"/"
        self.baseurl = baseurl
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token

    def authorize_password(self, path, username=u"", password=u""):
        """get an access token for the resource owner"""
        values = {
            'grant_type' : 'password',
            'client_id' : self.client_id,
            'client_secret' : self.client_secret,
            'username' : username,
            'password' : password
        }
        if path.startswith("/"):
            path = path[1:]
        url = urlparse.urljoin(self.baseurl, path)
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        result = response.read()
        if response.headers['Content-Type']=="application/json":
            result = json.loads(result)
        if response.code!=200:
            raise ClientError(str(result))
        self.access_token = result['access_token']
        self.refresh_token = result['refresh_token']

    def get(self, path, **kw):
        """retrieve a resource via GET using the access token"""
        values = {'access_token' : self.access_token}
        values.update(kw)
        data = urllib.urlencode(values)
        if path.startswith("/"):
            path = path[1:]
        url = urlparse.urljoin(self.baseurl,path)+"?"+data
        try:
            response = urllib2.urlopen(url)
        except urllib2.HTTPError:
            raise ClientError()
        result = response.read()
        if response.headers['Content-Type']=="application/json":
            result = json.loads(result)
        if response.code!=200:
            raise ClientError(str(result))
        return result
        

