from quantumlounge.framework import RESTfulHandler, json
import pkg_resources
import os

class Template(RESTfulHandler):
    """return a template via JSON or JSONP
    """

    @json(content_type="application/json")
    def get(self, template_id):
        """read the template and return it as a JSON string"""
        path = os.path.join("templates/",template_id)
        tmpl = pkg_resources.resource_string(__name__,path)
        return tmpl
