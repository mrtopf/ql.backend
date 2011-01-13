from quantumlounge.framework import Handler, Application
from quantumlounge.framework.decorators import html

import setup
import rest

class App(Application):

    def setup_handlers(self, map):
        """setup the mapper"""
        with map.submapper(path_prefix=self.settings.virtual_path) as m:
            rest.setup_handlers(m)
    
def main():
    port = 9992
    app = App(setup.setup())
    return webserver(app, port)

def app_factory(global_config, **local_conf):
    settings = setup.setup(**local_conf)
    return App(settings)

def webserver(app, port):
    import wsgiref.simple_server
    wsgiref.simple_server.make_server('', port, app).serve_forever()

if __name__=="__main__":
    main()

