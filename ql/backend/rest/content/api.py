from quantumlounge.framework import RESTfulHandler, json, html, Handler
from quantumlounge.framework import role
import werkzeug
import simplejson
import uuid
import functools
import pprint

import common
import registry

class Item(RESTfulHandler):
    """handle all methods for an item
    """

    def error(self, code, msg):
        self.settings.log.error("%s: %s" %(code, msg))
        return { 
            'error' : code, 
            'error_msg' : msg 
            }

    def _query_objs(self, query):
        """perform the query using the sort order etc. passed in to the 
        request and return a list of JSON formatted objects"""
        so = self.request.values.get("so","date") # sort order
        sd = self.request.values.get("sd","down") # sort direction
        try:
            l = int(self.request.values.get("l","30")) # limit
        except:
            return self.error(400, "wrong value for 'l'")
        try:
            o = int(self.request.values.get("o","0")) #offset
        except:
            return self.error(400, "wrong value for 'o'")
    
        items = self.settings.contentmanager.index(
            query = query,
            sort_on = so,
            sort_order = sd,
            limit = l,
            offset = o
        )
        items = [i.json for i in items]
        return items

    @role("admin")
    def r_subtree(self, content_id):
        """all recursively all nodes in the subtree of this object"""
        query = {
            '_ancestors' : content_id
        }
        return self._query_objs(query)

    def r_jsview(self, content_id):
        """return a JSON structure of the most recent item of the given
        type which is passed in as ``jsview_type`` in the request"""
        t = self.request.args.get("jsview_type","status")
        query = {
            '_ancestors' : "0",
            '_type' : t
        }
        return self._query_objs(query)

    @role("admin")
    def r_parents(self, content_id):
        """all recursively all nodes in the subtree of this object"""
        ct = self.settings.contentmanager
        item = ct.get(content_id)
        ancestors = item._ancestors
        res = []
        for a in ancestors:
            res.append(ct.get(a).json)
        return res

    @role("admin")
    def r_children(self, content_id):
        """return all direct children of this object"""
        query = {
            '_parent_id' : content_id
        }
        return self._query_objs(query)

    @role("admin")
    def r_default(self, content_id):
        """return the default representation meaning the actual payload"""
        item = self.settings.contentmanager.get(content_id)
        return item.json

    @json()
    def get(self, content_id, format = None):
        """return an index for the tweets"""
        cm = self.settings.contentmanager
        # retrieve object
        r = self.request.args.get("r","default")
        rname = "r_%s" %r
        m = getattr(self, rname, None)
        if m is not None:
            return {r : m(content_id)}
        return self.error(404, "representation not found")

    @json(content_type="application/json")
    @role("admin")
    def delete(self, content_id, format = None):
        """DELETEing an item"""
        cm = self.settings.contentmanager
        item = self.settings.contentmanager.get(content_id)
        if item is None:
            self.error(404, "item to delete was not found")
        res = self.settings.contentmanager.delete(content_id)
        if res is not None:
            return self.error(500, str(res))
        return {'status' : 'ok'}
    
    @json(content_type="application/json")
    @role("admin")
    def post(self, content_id, format = None):
        """POSTing to an item means creating a new one"""
        d = simplejson.loads(self.request.data)
        d['_parent_id'] = content_id
        _type = d['_type']
        ct = self.settings['content1'][_type]
        for field in ct.required_fields:
            if field not in d.keys():
                return self.error(400, "required field '%s' missing" %field)

        # check if _cid already exists in parent node
        # but only if a _cid is posted 
        if d.has_key("_cid"):
            cids = ct.mgr.collection.find({ 
                    '_cid' : d['_cid'],
                    '_parent_id' : content_id
                }).count()
            if cids>0:
                return self.error(400, "cid already exists")

        # check if subtype is allowed
        content = ct.mgr.get(content_id)
        if content._subtypes is not None:
            if d['_type'] not in content._subtypes:
                return self.error(400, "subtype not allowed")
       
        # create a new tweet and store it
        r = {}
        for a,v in d.items():
            r[str(a)]=v
        item = ct.cls(**r)
        item.oid = unicode(uuid.uuid4())
        i = ct.mgr.put(item)
        item = ct.mgr[i]
        # post the new item back
        return item.json

class Method(Handler):
    """call a method
    """
    
    def __init__(self, **kw):
        """initialize RESTful handler by checking access token and session"""
        super(Method, self).__init__(**kw)
        at = None
        # check header for oauth token
        # TODO
        # check URI parameters
        if self.request.content_type=="application/json":
            d = simplejson.loads(self.request.data)
            at = d.get("oauth_token", None)
        else:
            # TODO: Split GET and POST!
            at = self.request.values.get("oauth_token", None)
        if at is None:
            self.session = None
        else:
            am = self.settings.authmanager
            self.session = am.get(at)
        self.kw = kw

    def handle(self, **m):
        """handle a single request. This means checking the method to use, looking up
        the method for it and calling it. We have to return a WSGI application"""
        http_method = self.request.method.lower()

        rest_method = m['method']
        content_id = m['content_id']
        handler = m['handler']
        del m['method']
        del m['content_id']
        del m['handler']

        # retrieve the object
        cm = self.settings.contentmanager
        item = cm.get(content_id)

        # retrieve the adapter for this object
        _type = item._type
        methods = registry.type_registry.get(_type, {})
        adapter = methods.get(rest_method, None)(item, **self.kw)
        if adapter is None:
            return werkzeug.exceptions.NotFound()
        self.settings.log.debug("found adapter %s" %adapter)

        if hasattr(adapter, http_method):
            self.settings.log.debug("calling HTTP method %s and REST method %s on adapter '%s' " %(http_method, rest_method, adapter))
            return getattr(adapter, http_method)(**m)
        return werkzeug.exceptions.MethodNotAllowed()

