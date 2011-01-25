from ql.backend.framework import RESTfulHandler, json
import pkg_resources
import os
import werkzeug

class File(RESTfulHandler):
    """This is a handler which can be used to serve templates or any other files
    in form of JSON or JSONP responses. ``ql.backend`` will not host any files itself
    but will provide this handler under ``/file``.

    To define where files are being searched just put the absolute path to a directory
    info ``settings.files_path`` or as config directive ``files_path`` into the
    paster deployment config.

    TODO: Add some caching strategy? Does this need more work, how does it differ
    from static file serving (except the JSON part)?
    """

    @json(content_type="application/json")
    def get(self, filename):
        """read the file and return it as a JSON string"""
        abspath = self.settings.files_path
        path = os.path.join(abspath,filename)
        if not os.path.exists(path):
            raise werkzeug.exceptions.NotFound()
        with open(path) as fp:
            data = fp.read()
        return data

