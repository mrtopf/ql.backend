import pkg_resources

from paste.urlparser import StaticURLParser
import jinja2


def get_static_urlparser(filepath, cache_max_age = 1):
    return StaticURLParser(filepath, cache_max_age=cache_max_age)


class TemplateHandler(object):
    """a class for caching templates"""

    def __init__(self, base):
        self._cache = {}
        self.base = base

    def get_template(self, filename):
        """retrieve templates and store them inside our PageTemplate cache"""
        #if self._cache.has_key(filename):
            #return self._cache[filename]
        data = pkg_resources.resource_string(self.base, filename)
        t = self._cache[filename] = jinja2.Template(data)
        return t

    __getitem__ = get_template


