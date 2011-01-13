from base import Status, StatusCollection
from contenttypes import ContentType
import processors

class Folder(Status):
    """a folder"""
    TYPE = "folder"

class FolderCollection(StatusCollection):
    """manages folders"""
    data_class = Folder

class Link(Status):
    """a link object"""
    TYPE = "link"
    _attribs = Status._attribs+['link', 'link_title', 'link_image','link_description']
    _defaults = Status._defaults
    _defaults.update({
        'link' : u'',
        'link_title' : u'',
        'link_image' : u'',
        'link_description' : u'',
        })

    _processors = {
            '_cid' : [processors.EmptyToUUID()],
            'link' : [processors.URL()],
            'publication_date' : [processors.EmptyToNone(),processors.DateParser()],
            'depublication_date' : [processors.EmptyToNone(),processors.DateParser()],
    }

    def _after_init(self):
        """fix data if necessary"""
        super(Link, self)._after_init()
        if self.link_title=="":
            self.link_title = self.link


class LinkCollection(StatusCollection):
    """manages links"""
    data_class = Link


def FolderType(db, coll):
    tm = FolderCollection(db, coll)
    return ContentType(
        u"folder",
        name = u"Folder",
        description = "a folder",
        fields = Folder._attribs,
        required_fields = ['content'],
        mgr = tm,
        cls = Folder,
        reprs = ['default', 'atom'],
        default_repr = "default"
    )


def LinkType(db, coll):
    tm = LinkCollection(db, coll)
    return ContentType(
        u"link",
        name = u"Link",
        description = "a link",
        fields = Link._attribs,
        required_fields = ['content', 'link'],
        mgr = tm,
        cls = Link,
        reprs = ['default', 'atom'],
        default_repr = "default"
    )


