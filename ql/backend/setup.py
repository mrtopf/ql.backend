import pymongo
import logbook

from quantumcore.storages import AttributeMapper
from content.basetypedefs import StatusType
from content.basetypes import FolderType, LinkType
from content.contenttypes import ContentTypeManager
from content.base import ContentManager

import rest.auth
import rest.registry


def setup(**kw):
    """initialize the setup"""
    settings = AttributeMapper()

    settings.um_client_id = "example_client" # you should change this in settings
    settings.um_client_secret = "ex1" # you should change this in settings
    settings.um_poco_endpoint = "http://localhost:9992/1/users"

    settings.log = logbook.Logger("ql.backend")

    ## our database connection (TODO: should this be overridable?)
    settings.db = db = pymongo.Connection().pm

    # now we create the content type manager and register the content types
    ctm = ContentTypeManager()
    ctm.add(StatusType(db, "contents"))
    ctm.add(FolderType(db, "contents"))
    ctm.add(LinkType(db, "contents"))
    settings.content1=ctm # not sure if this is actually needed (TODO)

    # this is the main database handler. It retrieves and stores objects
    # we initialize it with the database, the collection name and the 
    # root node. 
    settings.contentmanager = ContentManager(db, "contents", ctm, "0")

    # this is the registry containing a mapping from type names to a list
    # of representations available for this type
    # TODO: Should this be part of the content types? Probably, but the question
    # is if we still want to keep python API and RESTful API seperate and this
    # is more a RESTful thing
    settings.representations = rest.registry.representations
    settings.views = rest.registry.views
    
    # the base path under which this application runs, usually on root
    # example: "/myapi"
    settings.virtual_path = ""

    # the auth manager which needs to support the ``get(access_token)`` method
    # which has to return some session object which identifies the user and
    # has a ``roles`` attribute.
    settings.authmanager = rest.auth.Sessions(settings)

    # update the settings with the keywords passed in
    # TODO: enable updating of sub settings via dot notation (pm.client_id)
    settings.update(kw)
    return settings






