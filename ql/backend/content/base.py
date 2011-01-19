from quantumcore.storages.mongoobjectstore import MongoObjectStore
import pymongo
import datetime
import copy
import uuid
import types
import dateutil
import processors

class Model(object):
    """a data model based on quantumcore.storages but copied here to make
    it more flexible. We provide the following features:
        
    * a list of basic attributes a type always needs to provide, like
    ** ``_id`` as the unique id in the storage
    ** ``_parent_id`` pointing to a parent node or ``None``
    ** ``_type`` containing the name of the content type
    ** ``_ancestors`` containing a link of all the ancestores (this is implementation dependant though)
    * a list of additional attributes per type
    * a default set for basic and additional attributes
    * making sure that read only attributes are really just read only
    """

    ###
    ### in a subclass you can override these attributes:
    ###

    _attribs = []
    _defaults = {}
    TYPE = "CONTENT"

    ###
    ### do not change things from on here
    ###

    # base attributes we always need
    _base_attribs = ['_id','_type','_parent_id','_ancestors','_subtypes']
    # additional attributes a type can define
    _base_defaults = {
            '_parent_id' : None,
            '_ancestors' : [],
            '_subtypes' : None,
    }

    def __init__(self, _id=None, _store = None, **kwargs):
        """initialize the database object class. """
        data = copy.copy(self._base_defaults)
        for a,v in self._defaults.items():
            if a in self._base_attribs:
                raise KeyError("default contains key %s which is already in base defaults" %a)
            data[a] = v

        # update defaults with kwargs
        data.update(kwargs)

        # store dictionary as attributes
        for a,v in data.items():
            if a in self._attribs+self._base_attribs and a!="_type":
                setattr(self, a, data[a])

        # now some manual storage of internal attributes
        if _id is None:
            _id = unicode(uuid.uuid4())
        self._id = _id
        self._store = _store
        if self._ancestors is None:
            self._ancestors = []

        self._after_init()

    def _after_init(self):
        """hook for updating data after init"""

    def _to_dict(self):
        """serialize this object to a dictionary"""
        d={}
        for attrib in self._attribs+self._base_attribs:
            if attrib=='_id' and self._id is None:
                continue
            d[attrib] = getattr(self, attrib, u'')
        return d
    
    @property
    def json(self):
        """return the JSON representation excluding internal attributes
        TODO: Now what is external and internal?!? Why do we select this here?
        Why not in the RESTful API?
        """
        d={}
        for attrib in self._attribs+['_id','_type','_subtypes']:
            d[attrib] = getattr(self, attrib, u'')
        return self.jsonify(d) # eventually convert data

    def jsonify(self, data):
        """hook for converting a dictionary to valid JSON. Input is a
        dictionary in ``data`` which might contain e.g. datetime elements
        which need to be converted to JSON compatible data.

        This hook should return a new (or updated) dictionary. 
        """
        return data

    @classmethod
    def from_dict(cls, d, store):
        """create an entry from the data given in d"""
        d = dict([(str(a),v) for a,v in d.items()])
        d['_store']=store
        return cls(**d)

    def _get_parent(self):
        """return the parent object if it exists or None"""
        pid = self._parent_id
        return self._store.get(pid)

    def _set_parent(self, parent):
        """set the parent object if it exists or None. It also updates
        the ancestor relationships"""
        if parent is not None:
            self._parent_id = parent._id
        else:
            self._parent_id = None
        
    _parent = property(_get_parent, _set_parent)

    @property
    def _type(self):
        """_type is readonly"""
        return self.TYPE

    @property
    def subtree_ids(self):
        """return recursively all children ids of a subtree starting with this node"""
        cids = [f['_id'] for f in self._store.collection.find( { '_ancestors' : self._id }, '_id')]
        return cids

    @property
    def subtree(self):
        """return recursively all children of a subtree starting with this node"""
        return self._store.find({ '_ancestors' : self._id })

    @property
    def parents(self):
        """return a list of all parent objects 

        TODO: This should not be here! We need a more generic data class
        for this to work because otherwise different objects from different
        types will contain different attributes. As we only need content for
        now this might be ok but should be changed!
        """
        p=[]
        o = self
        while True:
            if o._parent_id == None:
                return p
            o = self._store.get(o._parent_id,None)
            if o is None:
                # TODO: this should not happen, do some error management
                return p
            p.append(o)
        return p

    def set_id(self, id_):
        self._id = id_

    def get_id(self):
        return self._id

    oid = property(get_id, set_id)

class Collection(MongoObjectStore):
    """This is the base content manager from which all other managers should derive."""

    data_class = Model

    def index(self, sort_order="up", **kwargs):
        """return a list of items""" 
        if sort_order == "up":
            sort_order = pymongo.ASCENDING
        else:
            sort_order = pymongo.DESCENDING
        return self.find(sort_order = sort_order, **kwargs)

    def _after_save_hook(self, folder):
        """compute ancestors for a folder and it's children. This needs
        to be done recursively. We also use direct access to the database
        instead of using objects."""
        coll = self.collection
    
        # first compute our own list
        parent = folder._parent
        if parent is None:
            ancestors = folder._ancestors = []
        else:
            ancestors = copy.copy(parent._ancestors)
            ancestors.append(parent._id)
            folder._ancestors = ancestors
        d = folder._to_dict()
        coll.save(d)

        # now go recursively through all child folders. Every child folder gets
        # the ancestors plus this folder's id as ancestors. 
        # Recursively it's own id is added.
        
        def set_ancestors(folder, ancestors):
            new_ancestors = copy.copy(ancestors)
            new_ancestors.append(folder['_id']) # create the new list
            children = coll.find({'_parent_id':folder['_id']})
            for child in children:
                coll.update({'_id': child['_id']}, {'_ancestors' : new_ancestors})
                set_ancestors(child, new_ancestors)
        
        set_ancestors(d, ancestors)


class Status(Model):
    """example content type defining our own base type"""
    TYPE = "status"
    _attribs = ['_cid', 'content','date','user', 'publication_date', 'depublication_date']
    _defaults = {
            '_cid' : u'',               # "filename" inside the container
            'content' : u'',            # main content (status message)
            'date' : None,              # creation date of this item
            'user' : u'',               # owner
            'publication_date' : u'',   # when to publish or None (immediately)
            'depublication_date' : u'', # when to depublish or None (forever)
        }

    _processors = {
            '_cid' : [processors.EmptyToUUID()],
            'publication_date' : [processors.EmptyToNone(),processors.DateParser()],
            'depublication_date' : [processors.EmptyToNone(),processors.DateParser()],
    }

    def process(self):
        """convert and validate data"""
        errors = {}
        for field, procs in self._processors.items():
            v = getattr(self, field, None)
            for p in procs:
                try:
                    v = p.process(v, field)
                except processors.ProcessingError, e:
                    errors[field] = e.msg
                    break
                else:
                    setattr(self, field, v)
        return errors

    def _after_init(self):
        """fix data"""
        t = datetime.datetime.now()
        if type(self.date) in (types.UnicodeType, types.StringType):
            self.date = dateutil.parser.parse(self.date)
        if self.date is None:
            self.date = datetime.datetime.now()
        errors = self.process()
        if errors != {}:
            print "Errors on validation", errors
        # TODO: How to to error handling? We ignore them for now.

    def jsonify(self, data):
        """convert the dictionary to a JSON representation

        # TODO: this should be in the content API, not DB API
        
        """
        return data

class StatusCollection(Collection):
    """manages status messages"""

    data_class = Status

class ContentManager(object):
    """generic content manager

    This manager is able to manage content defined by types derived
    from the above base classes.
    
    """

    def __init__(self, db, collection_name, content_types, root_node=u"0"):
        """initialize the content manager.

        Use the given MongoDB ``db`` and the collection defined by
        ``collection_name`` inside. The ``content_types`` parameter takes the
        actual content type register and the ``root_node`` defines the name of
        the root node.
        
        """
        self.db = db
        self.collection_name = collection_name
        self.collection = db[collection_name]
        self.content_types = content_types
        self.root_node = root_node

    def index(self, sort_order="up", **kwargs):
        """return a list of items""" 
        if sort_order == "up":
            sort_order = pymongo.ASCENDING
        else:
            sort_order = pymongo.DESCENDING
        return self.find(sort_order = sort_order, **kwargs)

    def _to_obj(self, item):
        """convert a dictionary to a content object of the correct type"""
        _type = item['_type']
        ct_obj = self.content_types.get(_type, None)
        cls = ct_obj.cls 
        return cls.from_dict(item, ct_obj.mgr)

    def find(self, query={}, 
                   sort_on=None, 
                   sort_order=pymongo.ASCENDING,
                   limit=10,
                   offset=0):
        """return some entries based on the query"""
        if sort_on is not None:
            results = self.collection.find(query, 
                    skip=offset,
                    limit=limit, 
                    sort = [(sort_on, sort_order)]
                    )
        else:
            results = self.collection.find(query, limit=limit, skip=offset)

        # retrieve the data classes for those items
        objs = []
        for item in results:
            objs.append(self._to_obj(item))
        return objs

    def get(self, oid):
        """return the object with the given object id"""
        d = self.collection.find_one({'_id' : oid})
        return self._to_obj(d)
    
    def delete(self, oid):
        """delete the given object"""
        print "deleting", oid
        try:
            d = self.collection.remove({'_id' : oid}, safe=True)
            print "result",d
            return None
        except pymongo.OperationFailure, e:
            print "fehler", e.error, e.code
            return e.error

    @property
    def root(self):
        """return the root node"""
        return self.get(self.root_node)
