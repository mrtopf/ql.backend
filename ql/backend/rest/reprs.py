import pystache
import pkg_resources
import simplejson
from quantumlounge.framework.decorators import jsonconverter
import os


class Representation(object):
    """view for a type to display in different formats like HTML. JSON etc.

    This follows the adapter mechanism and you have to instantiate it with
    the object in question.

    The object needs to be passed in as a dictionary.
    
    """

    FORMAT = None

    def __init__(self, items=[]):
        self.items = items

    def __call__(self):
        """convert the object to the representation. per default we return JSON.

        We return the content type and the payload
        
        """
        return self.items

class GenericHTML(Representation):
    """generic HTML representation"""

    content_type = "application/json"

    def __call__(self):
        out = []
        for item in self.items:
            t = item['_type']
            # load template for type
            name = "entry.%s.mustache" %t
            path = os.path.join("templates/",name)
            tmpl = pkg_resources.resource_string(__name__,path)
            out.append(pystache.render(tmpl, item))
        data = "".join(out)
        return {'html': data}

