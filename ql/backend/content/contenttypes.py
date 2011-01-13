from quantumcore.storages import AttributeMapper
import copy

class ContentType(AttributeMapper):
    """base type for content types. A content type is mostly a dictionary and
    we use this class to define it's attributes"""

    def __init__(self, _id, **data):
        """initialize a content type"""

        default = {
            '_id' : _id,            # required
            'name' : u'',           # human readable name
            'description' : u'',    # human readable description
            'contains' : [],        # list of content type it is allowed to contain or 'all', empty means none
            'fields' : [('title', 'string')],        # list of fields and types this type understands
            'required_fields' : ['title'],          # list of required fields
            'reprs' : ['default', 'contents'],          # list of representations
            'default_repr' : 'default',          # default representation
            'mgr' : None,           # instance of the responsible content manager 
            'cls' : None,           # type implementation
        }

        d = copy.copy(default)
        d.update(data)
        self.update(d)
    @property
    def json(self):
        """return a JSON compatible representation"""
        return {
            '_id' : self._id,
            'name' : self.name,
            'description' : self.description,
        }

class ContentTypeManager(AttributeMapper):
    """a content type manager which is simply a dictionary"""

    def add(self, ct):
        """add a content type"""
        self[ct._id] = ct

    @property
    def json(self):
        """return a list of JSONified types"""
        return [t.json for t in self.values()]

