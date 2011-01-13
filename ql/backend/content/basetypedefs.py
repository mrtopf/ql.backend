from base import Status, StatusCollection
from contenttypes import ContentType

def StatusType(db, coll):
    tm = StatusCollection(db, coll)
    return ContentType(
        u"status",
        name = u"Status",
        description = "a status message",
        fields = Status._attribs,
        required_fields = ['content', 'user'],
        mgr = tm,
        cls = Status,
        reprs = ['default', 'atom'],
        default_repr = "default"
    )

