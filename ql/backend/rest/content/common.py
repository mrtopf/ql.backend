from quantumlounge.framework import RESTfulHandler, json, html, role, jsonp
import werkzeug
import datetime
import pymongo.code

class MethodAdapter(RESTfulHandler):
    """an adapter for using methods"""

    def __init__(self, item, **kw):
        """initialize this adapter"""
        super(MethodAdapter, self).__init__(**kw)
        self.item = item

class ExtendedMethodAdapter(MethodAdapter):
    """extends the ``MethodAdapter`` with some useful
    methods such as a method for querying objects"""

    def error(self, msg):
        return { 'error' : msg }

    def _query_objs(self, query):
        """perform the query using the sort order etc. passed in to the 
        request and return a list of JSON formatted objects"""
        so = self.request.values.get("so","date") # sort order
        sd = self.request.values.get("sd","down") # sort direction
        try:
            l = int(self.request.values.get("l","30")) # limit
        except:
            return self.error("wrong value for 'l'")
        try:
            o = int(self.request.values.get("o","0")) #offset
        except:
            return self.error("wrong value for 'o'")
    
        items = self.settings.contentmanager.index(
            query = query,
            sort_on = so,
            sort_order = sd,
            limit = l,
            offset = o
        )
        items = [i.json for i in items]
        return items

class SubTree(ExtendedMethodAdapter):
    """all recursively all nodes in the subtree of this object"""

    @json(content_type="application/json")
    @role("admin")
    def get(self, **kw):
        query = {
            '_ancestors' : content_id
        }
        return self._query_objs(query)

class Query(ExtendedMethodAdapter):
    """return a JSON structure of the most recent item of the given
    type which is passed in as ``jsview_type`` in the request"""

    @json()
    def get(self, **kw):
        import registry # here because of loops
        now = datetime.datetime.now()
        t = self.request.args.get("type","status").split(",") # types
        fmt = self.request.args.get("fmt","html") # which repr you want
        recursive = self.request.args.get("recursive","false").lower() == "true"
        s = """
            (this.publication_date < new Date() || !this.publication_date) &&
            (this.depublication_date > new Date() || !this.depublication_date) 
        """
        code=pymongo.code.Code(s)
        query = {
            '_type' : {"$in" : t},
            '$where' : code,
        }
        if recursive:
            query['_ancestors'] = self.item._id
        else:
            query['_parent_id'] = self.item._id
        res = self._query_objs(query) # list of dictionaries
        out = registry.fmt_registry[fmt](res)()
        return out

class Parents(ExtendedMethodAdapter):
    """all recursively all nodes in the subtree of this object"""

    @json(content_type="application/json")
    @role("admin")
    def get(self, **kw):
        ct = self.settings.contentmanager
        ancestors = self.item._ancestors
        res = []
        for a in ancestors:
            res.append(ct.get(a).json)
        return res

class Children(ExtendedMethodAdapter):
    """return all direct children of this object"""

    @json(content_type="application/json")
    @role("admin")
    def get(self, **kw):
        query = {
            '_parent_id' : self.item._id
        }
        return self._query_objs(query)

class Default(ExtendedMethodAdapter):
    """return the default representation meaning the actual payload"""

    @json(content_type="application/json")
    @role("admin")
    def get(self, **kw):
        return self.item.json

