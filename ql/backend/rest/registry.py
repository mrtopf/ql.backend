import common

"""

This module defines a mapping from types to possible representations. Usually
a representation is invoked by appending it to a path: ``/<objid>/<representation>``,
e.g. ``/2762862/children``.

"""

# this is a mapping from representation name to representation handler
# this is the common mapping for all base types and should be supported
# by all addon typed. They can extend this as they wish of course.
r_common = {
        'subtree' : common.SubTree,
        'query' : common.Query,
        'parents' : common.Parents,
        'children' : common.Children,
        'default' : common.Default,
        'post' : common.Post,
}

# this is the registry mapping type names to the representation mapping
representations = {
    'status' : r_common,
    'link' : r_common,
    'folder' : r_common,
}

__all__ = ['representations']
