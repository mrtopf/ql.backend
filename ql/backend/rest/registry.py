import common
import poll
import reprs

r_common = {
        'subtree' : common.SubTree,
        'query' : common.Query,
        'parents' : common.Parents,
        'children' : common.Children,
        'default' : common.Default,
        'post' : common.Post,
}

type_registry = {
    'status' : r_common,
    'link' : r_common,
    'folder' : r_common,
     
}

__all__ = ['type_registry']
