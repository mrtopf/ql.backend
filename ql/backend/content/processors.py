import formencode
import types
import dateutil.parser
import uuid


class ProcessingError(Exception):
    """exception being raised in case a processor encounters a problem"""
    
    def __init__(self, msg, field=None):
        """initialize the exception with an error message and the field on which it
        was raised."""
        self.msg = msg
        self.field = field
        
    def __repr__(self):
        return "ProcessingError: %s on %s" %(self.msg, self.field)

class Processor(object):
    """generic processor class for processing a value"""
    
    def process(self, value, field=None, **kw):
        """override this method in your own processors and test or convert this value. In
        the case of a success return the eventually converted value (or the original one)
        and in the case of an error raise a ``ProcessingError``
        ``field`` is the optional field instance on which this processor is run. This
        is mainly used for pushing it into the exception.
        Additionally any keyword values passed to the calling ``process()`` methods are
        passed to each processor.
        """
        return value

class ProcessorChain(list):
    """defines a list of processors which are run in sequence. The list of processors
    is given in the constructor, e.g.:

        chain = ProcessorChain( Email(), String() )
        try:
            value = chain.process("my@email.address", field="email")
        except ProcessingError, e:
            print "error %s in field %s" %(e.msg, e.field)
    
    """
    def __init__(self, *args):
        self.data = args

    def process(value, field=None, **kw):
        """process the chain of processors"""
        for processor in self:
            value = processor.process(value, field, **kw)
        return value

###
### predefined processors
###

class DummyState(object):
    """dummy state for formencode validators to not do any translations"""
    
    def _(self, s):
        return s

class FormEncodeProcessor(Processor):
    """a specialized processor for reusing formencode validators"""
    
    validator = None # put the formencode validator class here
    
    def __init__(self, state= DummyState(), *args, **kwargs):
        """initialize the validator with all the arguments. You can optionally pass in
        a state object which can e.g. hold your translation method. Check the ``formencode``
        documentation to learn more about the state object passed to validators."""
        self.v = self.validator(*args, **kwargs)
        self.state = state
    
    def process(self, value, field=None):
        try:
            return self.v.to_python(value, self.state)
        except formencode.Invalid, e:
            raise ProcessingError(str(e), field)
        raise ProcessingError("unkown error")

class Email(FormEncodeProcessor):
    validator = formencode.validators.Email

class URL(FormEncodeProcessor):
    validator = formencode.validators.URL
    
class DateConverter(FormEncodeProcessor):
    validator = formencode.validators.DateConverter

class DateParser(Processor):
    """checks if we can parse a date string into a datetime object.
    If the value is None, nothing is done, if an error occurs we will raise
    a ``ProcessingError``.
    If it's not a String Object, nothing will be done.
    """
    STRINGS = (types.StringType, types.UnicodeType)

    def process(self, value, field=None, **kw):
        """try to convert the string"""
        if type(value) in self.STRINGS:
            try:
                return dateutil.parser.parse(value)
            except ValueError:
                raise ProcessingError("Cannot parse date string", field)
        return value

class EmptyToNone(Processor):
    """converts empty strings to None"""

    def process(self, value, field=None, **kw):
        """try to convert the string"""
        if value=="" or value==u"":
            return None
        return value

class EmptyToUUID(Processor):
    """converts empty strings to a unique uuid"""

    def process(self, value, field=None, **kw):
        """try to convert the string"""
        if value=="" or value==u"":
            return unicode(uuid.uuid4())
        return value

class Int(FormEncodeProcessor):
    validator = formencode.validators.Int

class String(FormEncodeProcessor):
    validator = formencode.validators.String

