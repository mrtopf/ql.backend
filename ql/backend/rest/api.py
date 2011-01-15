from ql.backend.framework import RESTfulHandler, json, html, Handler
from ql.backend.framework import role
import werkzeug
import simplejson
import uuid

class Method(RESTfulHandler):
    """call a method
    """
    
    def handle(self, **m):
        """handle a single request. This means checking the method to use, looking up
        the method for it and calling it. We have to return a WSGI application"""
        http_method = self.request.method.lower()

        rest_method = m.get('method','default')
        if http_method == "post": 
            rest_method = "post"
        content_id = m['content_id']
        handler = m['handler']
        if m.has_key('method'):
            del m['method']
        del m['content_id']
        del m['handler']

        # retrieve the object
        cm = self.settings.contentmanager
        item = cm.get(content_id)

        # retrieve the adapter for this object
        _type = item._type
        methods = self.settings.representations.get(_type, {})
        adapter = methods.get(rest_method, None)
        if adapter is None:
            return werkzeug.exceptions.NotFound()
        adapter_instance = adapter(item, **self.kw)
        self.settings.log.debug("found adapter %s" %adapter)

        if hasattr(adapter, http_method):
            self.settings.log.debug("calling HTTP method %s and REST method %s on adapter '%s' " %(http_method, rest_method, adapter))
            return getattr(adapter_instance, http_method)(**m)
        return werkzeug.exceptions.MethodNotAllowed()

