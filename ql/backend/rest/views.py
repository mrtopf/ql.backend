

class View(object):
    """the default view"""

    def __init__(self, handler):
        """initializes the view. This will only be done once per method,
        not once per item. It will use the ``handler`` which called it for further
        reference. In your own variation you can e.g. query further objects
        or do similar initialization. Especially ``handler.settings`` 
        and ``handler.request`` might be useful."""
        self.handler = handler

    def __call__(self, item):
        """call this view with an item to convert. In your own views you probably
        want to overwrite this method. It has to return something which can
        be converted to JSON."""
        return item.json



