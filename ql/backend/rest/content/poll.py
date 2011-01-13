from common import MethodAdapter
from quantumlounge.framework import json
from werkzeug.contrib.securecookie import SecureCookie
import werkzeug
import simplejson
import datetime

class Voted(MethodAdapter):
    """check if user has voted already"""

    @json(content_type="application/json")
    def get(self, **kw):
        """post a new vote to this poll"""
        _id = self.item._id
        data = self.request.cookies.get("qlpoll")
        if data is not None:
            poll_data = SecureCookie.unserialize(data, self.settings.secret_key)
        else:
            poll_data = {'_id' : None}
        voted = poll_data['_id']==_id
        return {'voted' : voted}
            

class Vote(MethodAdapter):
    """a voting adapter for polls"""

    def get(self, **kw):
        """post a new vote to this poll"""
        answer_no = self.request.args.get("answer_no",None)
        if answer_no is None:
            return {'error' : 'Answer number not given'}
        self.item.vote(answer_no)
        self.item._store.update(self.item)
        cookie = SecureCookie({
            '_id' : self.item._id
            }, self.settings.secret_key).serialize()
        data = {'status' : 'ok'}
        s = simplejson.dumps(data)
        if self.request.args.has_key("callback"):
            callback = self.request.args.get("callback")
            s = "%s(%s)" %(callback, s)
            response = werkzeug.Response(s)
            response.content_type = "application/javascript"
        else:
            response = werkzeug.Response(s)
            response.content_type = "application/json"
        response.set_cookie('qlpoll', cookie, expires=datetime.datetime(2017,7,7), httponly=True)
        return response

class Results(MethodAdapter):
    """a results adapter for polls"""

    @json(content_type="application/json")
    def get(self, answer_no=None, **kw):
        """post a new vote to this poll"""
        return self.item.results

