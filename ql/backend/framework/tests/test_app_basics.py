from quantumlounge.framework.app import Application
from quantumlounge.framework.handler import Handler
import werkzeug

class TestHandler1(Handler):
    def get(self):
        return werkzeug.Response("test1")

class TestHandler2(Handler):
    def get(self):
        return werkzeug.Response("test2")

class TestHandler3(Handler):
    def get(self, id=''):
        return werkzeug.Response(str(id))
    
class App1(Application):
   
    def setup_handlers(self, map):
        map.connect(None, "/", handler=TestHandler1)
        map.connect(None, "/huhu", handler=TestHandler2)
        map.connect(None, "/post/{id}", handler=TestHandler3)

def test_app_basics():

    app = App1({'foo':'bar'}) # simple settings dict
    c = werkzeug.Client(app, werkzeug.BaseResponse)

    resp = c.get('/')
    assert resp.status=="200 OK"
    assert resp.data == "test1"
    
    resp = c.get('/huhu')
    assert resp.status=="200 OK"
    assert resp.data == "test2"

    
def test_app_wrong_method():    

    app = App1({'foo':'bar'}) # simple settings dict
    c = werkzeug.Client(app, werkzeug.BaseResponse)

    resp = c.post('/')
    assert resp.status=="405 METHOD NOT ALLOWED"
    
def test_app_unkown_path():

    app = App1({'foo':'bar'}) # simple settings dict
    c = werkzeug.Client(app, werkzeug.BaseResponse)

    resp = c.post('/no')
    assert resp.status=="404 NOT FOUND"
    
def test_path_params():

    app = App1({'foo':'bar'}) # simple settings dict
    c = werkzeug.Client(app, werkzeug.BaseResponse)

    resp = c.get('/post/33')
    assert resp.status=="200 OK"
    assert resp.data == "33"

        
