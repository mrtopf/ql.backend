import api
import templates

def setup_handlers(map):
    """setup the handlers"""
    with map.submapper(path_prefix="/1/content") as m:
        m.connect(None, '/{content_id}{.format};{method}', handler=api.Method)
        m.connect(None, '/{content_id}{.format}', handler=api.Item)

