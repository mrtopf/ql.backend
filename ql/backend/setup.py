import pymongo
import logbook

from quantumcore.storages import AttributeMapper
from content.basetypedefs import StatusType
from content.basetypes import FolderType, LinkType
from content.contenttypes import ContentTypeManager
from auth.tokens import AuthorizationManager


def setup(**kw):
    """initialize the setup"""
    settings = AttributeMapper()
    # wo liegt der User Server?
    settings['userserver'] = "http://localhost:9991"

    settings['log'] = logbook.Logger("ql.backend")

    ## content types
    settings.db = db = pymongo.Connection().pm
    ctm = ContentTypeManager()
    ctm.add(StatusType(db, "contents"))
    ctm.add(FolderType(db, "contents"))
    ctm.add(LinkType(db, "contents"))
    settings['content1']=ctm

    settings['authmanager'] = AuthorizationManager(db, "tokens")

    # path
    settings['virtual_path'] = ""

    # update the settings with the keywords passed in
    # TODO: enable updating of sub settings via dot notation (pm.client_id)
    settings.update(kw)
    return settings






