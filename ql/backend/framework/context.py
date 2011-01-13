from quantumcore.storages import AttributeMapper

class PageContext(AttributeMapper):
    """a utility class which holds all necessary information about a request
    and the context of the page for rendering a template. At it's core it's a 
    dictionary extended as ``quantumcore.storages.AttributeMapper``.
    
    Additionally it contains useful functions.
    """
    
